import sys
import os
import argparse
import logging
from logging.handlers import TimedRotatingFileHandler
from dotenv import load_dotenv
from auth import get_auth_token
from gmail_service import gmail_api_connection
from jobs.job_classify_recent import job_classify_recent
from jobs.job_mark_old_as_read import job_mark_old_as_read

logger = logging.getLogger(__name__)

def get_args():
	"""Parse command line arguments"""
	parser = argparse.ArgumentParser(description="Gmail Organizer")
	parser.add_argument("job", type=str, help="Job to run (valid options: [classify_recent])")
	return parser.parse_args()

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

def run(args):
	credentials_path = os.getenv("CREDENTIALS_PATH", "credentials/credentials.txt")
	token_path = os.getenv("TOKEN_PATH", "credentials/token.json")
	
	# Obtain authorization using the previously stored token if available,
	# otherwise request login and save token for future use.
	creds = get_auth_token(credentials_path, token_path)
	# Connect to the Gmail API by creating the service object
	service = gmail_api_connection(creds)

	if args.job == "classify_recent":
		job_classify_recent(service)
	elif args.job == "mark_old_as_read":
		job_mark_old_as_read(service)
	else:
		logger.warning(f"Unknown job: {args.job}")

def main():
	setup_logging()
	args = get_args()
	try:
		run(args)
	except Exception as e:
		logger.critical(f"Fatal error: {e}")
		sys.exit(1)

if __name__ == '__main__':
	main()