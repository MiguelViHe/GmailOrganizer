import os
import logging

logger = logging.getLogger(__name__)

def job_mark_old_as_read(service):
	"""Job that marks old emails as read based on a query defined in the environment variable OLD_EMAIL_READ (defaulting to "older_than:30d label:Processed")"""
	query = os.getenv("OLD_EMAIL_READ", "older_than:30d label:Processed label:Promos is:unread")
	results = service.users().messages().list(userId='me', q=query).execute()
	messages = results.get('messages', [])

	if not messages:
		logger.info("No emails older than 30 days to mark as read available.")
		return

	message_ids = [msg["id"] for msg in messages]

	try:
		service.users().messages().batchModify(
			userId="me",
			body={
				"ids": message_ids,
				"removeLabelIds": ["UNREAD"]
			}
		).execute()

		logger.info(f"Marked {len(message_ids)} messages as read using query: {query}")
	except Exception as e:
		logger.error(f"Error marking messages as read: {e}")