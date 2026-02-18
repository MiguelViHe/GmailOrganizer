from rules import RULES

def get_body(message):
	import base64

	payload = message.get("payload", {})

	# Caso multipart
	if "parts" in payload:
		for part in payload["parts"]:
			if part["mimeType"] == "text/plain":
				data = part["body"].get("data")
				if data:
					return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

	# Caso simple
	data = payload.get("body", {}).get("data")
	if data:
		return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

	return ""


def extract_mail_data(message):
	"""Extrae el sender el subject y el body de un mensaje y lo devuelve como un diccionario junto con los label_ids"""
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
	"""Descripción de la función"""
	# sender_contains
	if "sender_contains" in block:
		print(f"		sender = {mail_data["sender"]}")
		if any(pattern.lower() in mail_data["sender"].lower() for pattern in block.get("sender_contains", [])):
			print(f"		pattern coincidente in sender")
			return True

	# subject_contains
	if "subject_contains" in block:
		print(f"		subject = {mail_data["subject"]}")
		if any(pattern.lower() in mail_data["subject"].lower() for pattern in block.get("subject_contains", [])):
			print(f"		pattern coincidente in subject")
			return True

	# body_contains
	if "body_contains" in block:
		print("		body... ")
		if any(pattern.lower() in mail_data["body"].lower() for pattern in block.get("body_contains", [])):
			print(f"		pattern coincidente in body")
			return True

	# has_unsubscribe_header
	if "has_unsubscribe_header" in block:
		if block.get("has_unsubscribe_header"):
			if mail_data["list_unsubscribe"]:
				print(f"		has_unsubscribe_header SI")
				return True

	return False

def matches_rule(mail_data, rule):
	"""Descripción de la función"""
	for block in rule.get("conditions", []):
		print(f"	mail= {mail_data["subject"]}, block = {block}")
		if matches_condition_block(mail_data, block):
			return True
	return False

def get_actions(mail_data):
	for rule in RULES:
		print(f"rule_name={rule["name"]}")
		if matches_rule(mail_data, rule):
			print(f"matched rule: {rule["name"]}")
			return rule["actions"]
	return None

	

def apply_actions(service, msg_id, actions):
	"""Aplica acciones sobre un mensaje: añadir etiqueta, archivar, marcar como leído"""
	
	body = {
		"addLabelIds": [],
		"removeLabelIds": []
	}

	if "add_label" in actions:
		label_name = actions["add_label"]
		labels = service.users().labels().list(userId="me").execute().get('labels', [])
		label_id = None
		for l in labels:
			if l["name"] == label_name:
				label_id = l["id"]
				break
		if not label_id:
			new_label = {
				"name": label_name,
				"messageListVisibility": "show",
				"labelListVisibility": "labelShow",
			}
			created_label = service.users().labels().create(userId="me", body=new_label).execute()
			label_id = created_label["id"]
		body["addLabelIds"].append(label_id)
		if actions.get("archive"):
			body["removeLabelIds"].append("INBOX")
		if actions.get("mark_as_read"):
			body["removeLabelIds"].append("UNREAD")
		#Aplicamos los cambios
		service.users().messages().modify(userId="me", id=msg_id, body=body).execute()
