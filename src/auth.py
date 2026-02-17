import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request


# SCOPES indica qué permisos vamos a pedir a Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_auth_token(credentials_path, token_path):
	"""autenticación OAuth2"""
	creds = None
	
	try:
		# Si ya existe token.json (usuario ya se autenticó antes), lo cargamos en creds
		if os.path.exists(token_path):
			creds = Credentials.from_authorized_user_file(token_path, SCOPES)
		if creds and creds.expired and creds.refresh_token:
			try:
				creds.refresh(Request())
			except RefreshError:
				print("Refresh token inválido. Se requiere nuevo login.")
				os.remove(token_path)
				creds = None
		# Si no hay credenciales válidas, pedimos login en el navegador
		if not creds or not creds.valid:
			flow = InstalledAppFlow.from_client_secrets_file(
				credentials_path, SCOPES)  # Tu archivo descargado de Google Cloud
			creds = flow.run_local_server(port=0)  # Abre el navegador y pide permisos
			# Guardamos token.json para no pedir login la próxima vez
			with open(token_path, 'w') as token:
				token.write(creds.to_json())
		return creds
	except FileNotFoundError:
		print("No se encontró credentials.json. Verifica la ruta.")
		raise
	except Exception as e:
		print(f"Error durante la autenticación: {e}")
		raise