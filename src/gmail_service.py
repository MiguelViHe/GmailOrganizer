from googleapiclient.discovery import build

def gmail_api_connection(creds):
	"""conexión con Gmail API"""

	# Conectamos con Gmail API: Creamos el objeto service que nos permite llamar a la API de Gmail.
	return build('gmail', 'v1', credentials=creds)