from rules import RULES

def get_actions_for_sender(sender):
	"""
	Devuelve la primera acción que coincida con el remitente.
	sender: string, el correo o dominio del remitente
	retorna: dict con las acciones o None si no coincide ninguna
	"""
	for rule in RULES:
		for pattern in rule["condition"].get("sender_contains", []):
			if pattern.lower() in sender.lower():
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
