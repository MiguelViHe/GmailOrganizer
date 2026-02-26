from utils import create_label

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