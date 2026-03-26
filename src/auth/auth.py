import logging
import os.path

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

logger = logging.getLogger(__name__)

# SCOPES defines the permissions we request from Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def load_token(token_path):
	"""Load credentials from token.json if it exists
	if not, return None to trigger re-authentication"""
	if not os.path.exists(token_path):
		return None
	return Credentials.from_authorized_user_file(token_path, SCOPES)

def refresh_token(creds, token_path):
	"""Try to refresh credentials if possible"""
	if not creds or not creds.expired or not creds.refresh_token:
		return creds
	try:
		creds.refresh(Request())

		# Save the refreshed token back to token.json
		with open(token_path, "w") as token:
			token.write(creds.to_json())
		logger.info("Token refreshed successfully.")
		
		return creds
	except RefreshError:
		logger.critical("Invalid refresh token. Manual re-authentication required.")
		return None

def get_auth_token(token_path):
	"""Authenticate using OAuth2, returning valid credentials or None if authentication fails"""
	try:
		# Load token.json. It will return None if it doesn't exist, which will trigger the interactive login flow. 
		creds = load_token(token_path)

		# Refresh token if expired. If not valid, trigger re-authentication
		creds = refresh_token(creds, token_path)

		if not creds:
			logger.critical("No valid credentials. Run: python auth/bootstrap_auth.py")
			return None
		return creds

	except Exception as e:
		logger.critical(f"Authentication error: {e}")
		raise