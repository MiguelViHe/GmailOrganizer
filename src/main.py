import sys
import os
from dotenv import load_dotenv
from auth import get_auth_token
from gmail_service import gmail_api_connection

def run():
	#Cargamos las variables que tenemos en .env
	load_dotenv()
	credentials_path = os.getenv("CREDENTIALS_PATH", "credentials/credentials.txt")
	token_path = os.getenv("TOKEN_PATH", "credentials/token.json")
	
	# Obtenemos autorización a partir del token obtenido con anterioridad si ya lo obtuvimos o lo solicitamos y guradamos antes de obtener la autorización. 
	creds = get_auth_token(credentials_path, token_path)
	# Conectamos con Gmail API: Creamos el objeto service que nos permite llamar a la API de Gmail.
	service = gmail_api_connection(creds)

	# Pedimos los últimos 10 correos
	results = service.users().messages().list(userId='me', maxResults=10).execute()
	messages = results.get('messages', [])
	if not messages:
		print("No emails available.")
	else:
		print("Últimos 10 correos:")
		for msg in messages:
			try:
				m = service.users().messages().get(userId='me', id=msg['id']).execute()
				subject = ''
				sender = ''
				for header in m['payload']['headers']:
					if header['name'] == 'From':
						sender = header['value']
					elif header['name'] == 'Subject':
						subject = header['value']
				print(f"- {subject} from {sender}")
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