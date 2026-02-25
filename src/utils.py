def create_label(name, messageListVisibility, labelListVisibility, service, labels_map):
	"""
	Create a label with the given name if it doesn't exist.
	Returns the label_id of the created label.
	"""
	new_label = {
		"name": name,
		"messageListVisibility": messageListVisibility,
		"labelListVisibility": labelListVisibility,
	}

	# Create the label via Gmail API
	created_label = service.users().labels().create(userId="me", body=new_label).execute()

	# Store the label_id in the labels_map for future reference
	label_id = created_label["id"]
	labels_map[name] = label_id

	return label_id