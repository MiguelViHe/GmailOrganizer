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

def get_labels_map(service):
	"""Return a dictionary mapping label names to their IDs"""
	labels = service.users().labels().list(userId="me").execute().get("labels", [])
	return {label["name"]: label["id"] for label in labels}