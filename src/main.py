import sys
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from dotenv import load_dotenv
from auth import get_auth_token
from gmail_service import gmail_api_connection
from organizer import get_actions, apply_actions, extract_mail_data
from utils import create_label

logger = logging.getLogger(__name__)

def setup_logging():
	"""Load environment variables from .env and configure logging"""

	# Load environment variables from .env
	load_dotenv()

	# Global logger
	root_logger = logging.getLogger()  # Receives all messages (DEBUG, INFO, etc.)
	if not root_logger.handlers:  # Prevent reconfiguring handlers if already set
		root_logger.setLevel(logging.DEBUG)  # Minimum global level: receives all messages

		# Configure multiple handlers for the global logger
		# Handlers are independent. Logger sends all messages to all handlers,
		# but each handler decides which messages to accept.

		# File handler (for cron / production)
		log_level = os.getenv("LOG_LEVEL", "INFO").upper()
		file_handler = TimedRotatingFileHandler(
			'/home/miguel/gmail_organizer_logs/gmail_organizer.log',
			when="midnight",   # Rotate at midnight
			interval=1,        # Every 1 day
			backupCount=4,     # Keep last 5 files
			encoding="utf-8"
		)
		file_handler.setLevel(getattr(logging, log_level, logging.INFO))
		file_formatter = logging.Formatter(
			'%(asctime)s - %(name)s - %(levelname)s - %(message)s',
			datefmt='%Y-%m-%d %H:%M:%S'
		)
		file_handler.setFormatter(file_formatter)
		root_logger.addHandler(file_handler)

		# Console handler (for development / DEBUG)
		console_handler = logging.StreamHandler(sys.stdout)
		if os.getenv("DEBUG") == "1":
			console_handler.setLevel(logging.DEBUG)  # Show DEBUG on console
		else:
			console_handler.setLevel(logging.INFO)
		console_formatter = logging.Formatter(
			'%(asctime)s - %(name)s - %(levelname)s - %(message)s',
			datefmt='%Y-%m-%d %H:%M:%S'
		)
		console_handler.setFormatter(console_formatter)
		root_logger.addHandler(console_handler)

		# Silence external libraries (only WARNING+)
		logging.getLogger("googleapiclient").setLevel(logging.WARNING)
		logging.getLogger("google.auth").setLevel(logging.WARNING)
		logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)

def get_labels_map(service):
	"""Return a dictionary mapping label names to their IDs"""
	labels = service.users().labels().list(userId="me").execute().get("labels", [])
	return {label["name"]: label["id"] for label in labels}

def run():
	credentials_path = os.getenv("CREDENTIALS_PATH", "credentials/credentials.txt")
	token_path = os.getenv("TOKEN_PATH", "credentials/token.json")
	
	# Obtain authorization using the previously stored token if available,
	# otherwise request login and save token for future use.
	creds = get_auth_token(credentials_path, token_path)
	
	# Connect to the Gmail API by creating the service object
	service = gmail_api_connection(creds)

	# Fetch the latest 10 emails (maxResults=10) or using a date query (newer...)
	date = os.getenv("DATE", "newer_than:1d -label:Processed")
	results = service.users().messages().list(userId='me', q=date).execute()
	logger.debug(results) 
	messages = results.get('messages', [])
	logger.debug(messages)
	
	if not messages:
		logger.info("No emails available.")
	else:
		labels_map = get_labels_map(service)
		if not labels_map.get("Processed"):
			create_label("Processed", "show", "labelHide", service, labels_map)
		logger.debug(labels_map)
		
		for msg in messages:
			try:
				m = service.users().messages().get(userId='me', id=msg['id']).execute()
				mail_data = extract_mail_data(m)
				actions = get_actions(mail_data)
				if actions:
					logger.debug(f"ACTIONS: {actions}")
					apply_actions(service, msg["id"], actions, mail_data, labels_map)
					logger.info(f"Applied actions to msg_id={msg['id']} {mail_data['sender']}: {mail_data['subject']}")
			except Exception as e:
				logger.error(f"Error reading message {msg['id']}: {e}")

def main():
	setup_logging()
	try:
		run()
	except Exception as e:
		logger.critical(f"Fatal error: {e}")
		sys.exit(1)

if __name__ == '__main__':
	main()