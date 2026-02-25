import logging
from rules import RULES
from utils import create_label

logger = logging.getLogger(__name__)

def get_body(message):
	import base64

	payload = message.get("payload", {})

	# Multipart case
	if "parts" in payload:
		for part in payload["parts"]:
			if part["mimeType"] == "text/plain":
				data = part["body"].get("data")
				if data:
					return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

	# Simple case
	data = payload.get("body", {}).get("data")
	if data:
		return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

	return ""


def extract_mail_data(message):
	"""Extract the sender, subject, and body from a message, returning a dictionary along with label IDs"""
	sender = ""
	subject = ""
	body = ""
	list_unsubscribe = False
	headers = message["payload"].get("headers", [])
	
	for header in headers:
		if header["name"] == "From":
			sender = header["value"]
		if header["name"] == "Subject":
			subject = header["value"]
		if header["name"] == "List-Unsubscribe":
			list_unsubscribe = True

	body = get_body(message)

	return {
		"sender": sender,
		"subject": subject,
		"body": body,
		"list_unsubscribe": list_unsubscribe,
		"labels_ids": message.get("labelIds", [])
	}


def matches_condition_block(mail_data, block):
	"""Check if a mail_data matches a single condition block"""
	
	# sender_contains
	if "sender_contains" in block:
		logger.debug(f"    sender = {mail_data['sender']}")
		if any(pattern.lower() in mail_data["sender"].lower() for pattern in block.get("sender_contains", [])):
			logger.debug("    matching pattern found in sender")
			return True

	# subject_contains
	if "subject_contains" in block:
		logger.debug(f"    subject = {mail_data['subject']}")
		if any(pattern.lower() in mail_data["subject"].lower() for pattern in block.get("subject_contains", [])):
			logger.debug("    matching pattern found in subject")
			return True

	# body_contains
	if "body_contains" in block:
		logger.debug("    checking body...")
		if any(pattern.lower() in mail_data["body"].lower() for pattern in block.get("body_contains", [])):
			logger.debug("    matching pattern found in body")
			return True

	# has_unsubscribe_header
	if "has_unsubscribe_header" in block:
		if block.get("has_unsubscribe_header") and mail_data["list_unsubscribe"]:
			logger.debug("    has_unsubscribe_header = YES")
			return True

	return False


def matches_rule(mail_data, rule):
	"""Check if mail_data matches any condition block in the rule"""
	for block in rule.get("conditions", []):
		logger.debug(f"    mail={mail_data['subject']}, block={block}")
		if matches_condition_block(mail_data, block):
			return True
	return False


def get_actions(mail_data):
	"""Return a list of actions to apply based on matched rules"""
	matched_rules = []
	top_rules_actions = []

	for rule in RULES:
		logger.debug(f"rule_name={rule['name']}")
		if matches_rule(mail_data, rule):
			logger.debug(f"MATCHED RULE: {rule['name']}")
			matched_rules.append(rule)

	if matched_rules:
		max_priority = max(rule.get("priority", 0) for rule in matched_rules)
		top_rules_actions = [r.get("actions") for r in matched_rules if r.get("priority", 0) == max_priority]

	return top_rules_actions


def apply_actions(service, msg_id, actions, mail_data, labels_map):
	"""Apply actions to a message: add label, archive, mark as read, etc."""
	add_labels = set()
	remove_labels = set()

	for action in actions:
		if "add_label" in action:
			label_name = action["add_label"]
			label_id = labels_map.get(label_name)

			if not label_id:
				label_id = create_label(label_name, "show", "labelShow", service, labels_map)
			add_labels.add(label_id)

		if action.get("archive") and "INBOX" in mail_data["labels_ids"]:
			remove_labels.add("INBOX")
		if action.get("mark_as_read") and "UNREAD" in mail_data["labels_ids"]:
			remove_labels.add("UNREAD")
		if "Processed" not in mail_data["labels_ids"]:
			add_labels.add(labels_map.get("Processed"))

	body = {
		"addLabelIds": list(add_labels),
		"removeLabelIds": list(remove_labels)
	}

	# Apply the label modifications
	service.users().messages().modify(userId="me", id=msg_id, body=body).execute()
