import os
import logging
from organizer.classifier import classify_mail
from utils import get_labels_map, create_label

logger = logging.getLogger(__name__)

def job_classify_recent(service):
	"""Job that classifies recent emails based on the CLASSIFY environment variable, (defaulting to "newer_than:1d -label:Processed")"""
	query = os.getenv("CLASSIFY", "newer_than:1d -label:Processed")
	results = service.users().messages().list(userId='me', q=query).execute()
	messages = results.get('messages', [])

	if not messages:
		logger.info("No emails available.")
		return

	# Mapping of labels and creation of "Processed" if it doesn't exist
	labels_map = get_labels_map(service)
	if not labels_map.get("Processed"):
		create_label("Processed", "show", "labelHide", service, labels_map)

	# Process each message
	for msg in messages:
		try:
			full_msg = service.users().messages().get(userId='me', id=msg['id']).execute()
			mail_data = classify_mail(service, full_msg, labels_map)
			if mail_data:
				logger.info(f"Processed msg_id={msg['id']}: {mail_data['subject']} from {mail_data['sender']}")
		except Exception as e:
			logger.error(f"Error processing message {msg['id']}: {e}") 