import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# SCOPES indica qué permisos vamos a pedir a Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
	creds = None

	# Si ya existe token.json (usuario ya se autenticó antes), lo usamos
	if os.path.exists('credentials/token.json'):
		creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)

	# Si no hay credenciales válidas, pedimos login en el navegador
	if not creds or not creds.valid:
		flow = InstalledAppFlow.from_client_secrets_file(
			'credentials/credentials.json', SCOPES)  # Tu archivo descargado de Google Cloud
		creds = flow.run_local_server(port=0)  # Abre el navegador y pide permisos
		# Guardamos token.json para no pedir login la próxima vez
		with open('credentials/token.json', 'w') as token:
			token.write(creds.to_json())

	# Conectamos con Gmail API: Creamos el objeto service que nos permite llamar a la API de Gmail.
	service = build('gmail', 'v1', credentials=creds)

	# Pedimos los últimos 10 correos
	results = service.users().messages().list(userId='me', maxResults=10).execute()
	messages = results.get('messages', [])

	if not messages:
		print("No hay correos.")
	else:
		print("Últimos 10 correos:")
		for msg in messages:
			m = service.users().messages().get(userId='me', id=msg['id']).execute()
			subject = ''
			for header in m['payload']['headers']:
				if header['name'] == 'From':
					sender = header['value']
				elif header['name'] == 'Subject':
					subject = header['value']
			print(f"- {subject} from {sender}")

if __name__ == '__main__':
	main()
