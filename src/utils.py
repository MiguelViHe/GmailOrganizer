def create_label(name, messageListVisibility, labelListVisibility, service, labels_map):
	"""
	Create "name" label if it doesn't exist
	Return the label_id of the created label.
	"""
	new_label = {
		"name": name,
		"messageListVisibility": messageListVisibility,
		"labelListVisibility": labelListVisibility,
	}
	created_label = service.users().labels().create(userId="me", body=new_label).execute()
	label_id = created_label["id"]
	labels_map[name] = label_id
	return label_id