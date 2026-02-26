import base64
from organizer.rule_engine import get_actions
from organizer.actions import apply_actions

def get_body(message):
	"""Extract plain text body from a Gmail message"""
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

def classify_mail(service, message, labels_map):
    """Top-level function to classify a Gmail message"""
    mail_data = extract_mail_data(message)
    actions = get_actions(mail_data)
    if actions:
        apply_actions(service, message["id"], actions, mail_data, labels_map)