import os.path
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request

logger = logging.getLogger(__name__)

# SCOPES defines the permissions we request from Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_auth_token(credentials_path, token_path):
	"""Authenticate using OAuth2"""
	creds = None
	
	try:
		# Load token.json if it exists (user has previously authenticated)
		if os.path.exists(token_path):
			creds = Credentials.from_authorized_user_file(token_path, SCOPES)

		# Refresh token if expired
		if creds and creds.expired and creds.refresh_token:
			try:
				creds.refresh(Request())
			except RefreshError:
				logging.warning("Invalid refresh token. New login required.")
				os.remove(token_path)
				creds = None

		# Request login via browser if no valid credentials
		if not creds or not creds.valid:
			flow = InstalledAppFlow.from_client_secrets_file(
				credentials_path, SCOPES)  # Client secrets file downloaded from Google Cloud
			creds = flow.run_local_server(port=0)  # Opens browser to request permissions

			# Save token.json to avoid re-login next time
			with open(token_path, 'w') as token:
				token.write(creds.to_json())

		return creds

	except FileNotFoundError:
		logger.error("credentials.json not found. Please verify the path.")
		raise

	except Exception as e:
		logger.critical(f"Authentication error: {e}")
		raise