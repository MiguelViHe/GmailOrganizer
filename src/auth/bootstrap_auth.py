
import os
import logging
from google_auth_oauthlib.flow import InstalledAppFlow

logger = logging.getLogger(__name__)

# SCOPES defines the permissions we request from Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def interactive_login(credentials_path):
	"""Manual OAuth login (bootstrap step)"""
	flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)  # Client secrets file downloaded from Google Cloud
	creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")  # Opens browser to request permissions
	return creds

def run_bootstrap():
	"""Run the bootstrap authentication process"""
	credentials_path = os.getenv("CREDENTIALS_PATH", "credentials/credentials.json")
	token_path = os.getenv("TOKEN_PATH", "credentials/token.json")
	
	creds = interactive_login(credentials_path)

	# Save token.json to avoid re-login next time
	with open(token_path, 'w') as token:
		token.write(creds.to_json())

	logger.info("Bootstrap completed. token.json generated.")

if __name__ == "__main__":
	run_bootstrap()