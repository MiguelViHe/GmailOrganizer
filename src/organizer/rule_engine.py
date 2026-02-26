import logging
from rules import RULES

logger = logging.getLogger(__name__)

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

	for rule in RULES:
		logger.debug(f"rule_name={rule['name']}")
		if matches_rule(mail_data, rule):
			logger.debug(f"MATCHED RULE: {rule['name']}")
			matched_rules.append(rule)

	if not matched_rules:
		return []
	
	max_priority = max(rule.get("priority", 0) for rule in matched_rules)
	top_rules_actions = [r.get("actions") for r in matched_rules if r.get("priority", 0) == max_priority]

	return top_rules_actions