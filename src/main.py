import sys
import os
from dotenv import load_dotenv
from auth import get_auth_token
from gmail_service import gmail_api_connection
from organizer import get_actions, apply_actions, extract_mail_data
from utils import create_label

def get_labels_map(service):
	"""Return a dictionary name → id of labels"""
	labels = service.users().labels().list(userId="me").execute().get("labels", [])
	return {label["name"]: label["id"] for label in labels}

def run():
	#Cargamos las variables que tenemos en .env
	load_dotenv()
	credentials_path = os.getenv("CREDENTIALS_PATH", "credentials/credentials.txt")
	token_path = os.getenv("TOKEN_PATH", "credentials/token.json")
	
	# Obtenemos autorización a partir del token obtenido con anterioridad si ya lo obtuvimos o lo solicitamos y guradamos antes de obtener la autorización. 
	creds = get_auth_token(credentials_path, token_path)
	# Conectamos con Gmail API: Creamos el objeto service que nos permite llamar a la API de Gmail.
	service = gmail_api_connection(creds)

	# Pedimos los últimos 10 correos (maxResults=10) o en una query de fecha (newer...)
	date = os.getenv("DATE", "newer_than:7d")
	results = service.users().messages().list(userId='me', q=date).execute()
	# print(results)
	messages = results.get('messages', [])
	# print(messages)
	if not messages:
		print("No emails available.")
	else:
		print("llego")
		labels_map = get_labels_map(service)
		if not labels_map.get("Processed"):
			print("entro")
			create_label("Processed", "show", "labelHide", service, labels_map)
		# print(labels_map)
		for msg in messages:
			try:
				m = service.users().messages().get(userId='me', id=msg['id']).execute()
				mail_data = extract_mail_data(m)
				actions = get_actions(mail_data)
				if actions:
					# print(f"ACTIONS: {actions}")
					# print(f"msg id = {msg["id"]} subject = {mail_data["subject"]}")
					apply_actions(service, msg["id"], actions, mail_data, labels_map)
			except Exception as e:
				print(f"Error readind the message {msg['id']}: {e}")

def main():
	try:
		run()
	except Exception as e:
		print(f"Fatal error: {e}")
		sys.exit(1)

if __name__ == '__main__':
	main()