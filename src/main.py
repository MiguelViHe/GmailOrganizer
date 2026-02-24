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
	"""Load the variables in .env and setup the logging"""

	# Load env variables from .env
	load_dotenv()

	# Logger global
	root_logger = logging.getLogger() # recibe todos los mensajes (DEBUG, INFO, etc.)
	if not root_logger.handlers: #Si ya hay handlers configurados no se vuelven a configurar
		root_logger.setLevel(logging.DEBUG)  # Nivel mínimo global. Recibe todos los mensajes

		# Configuramos varios handlers dentro del global 
		# Los handlers son independientes. El logger “manda” todos los mensajes a todos los handlers,
		#  pero cada handler decide qué acepta.

		# Handler para fichero (cron / producción) Lo
		log_level = os.getenv("LOG_LEVEL", "INFO").upper()
		file_handler = TimedRotatingFileHandler(
			'/home/miguel/gmail_organizer_logs/gmail_organizer.log',
			when="midnight",	# Rota a medianoche
			interval=1,			# Cada 1 día
			backupCount=4,		# Mantener los últimos 5 archivos
			encoding="utf-8"
		)
		file_handler.setLevel(getattr(logging, log_level, logging.INFO))
		file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
											datefmt='%Y-%m-%d %H:%M:%S')
		file_handler.setFormatter(file_formatter)
		root_logger.addHandler(file_handler)

		# Handler para consola (desarrollo / DEBUG)
		console_handler = logging.StreamHandler(sys.stdout)
		if os.getenv("DEBUG") == "1":
			console_handler.setLevel(logging.DEBUG)  # DEBUG visible en pantalla
		else:
			console_handler.setLevel(logging.INFO)
		console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
												datefmt='%Y-%m-%d %H:%M:%S')
		console_handler.setFormatter(console_formatter)
		root_logger.addHandler(console_handler)

		# Silenciamos librerias externas (Solo WARNING+)
		logging.getLogger("googleapiclient").setLevel(logging.WARNING)
		logging.getLogger("google.auth").setLevel(logging.WARNING)
		logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)

def get_labels_map(service):
	"""Return a dictionary name → id of labels"""
	labels = service.users().labels().list(userId="me").execute().get("labels", [])
	return {label["name"]: label["id"] for label in labels}

def run():
	credentials_path = os.getenv("CREDENTIALS_PATH", "credentials/credentials.txt")
	token_path = os.getenv("TOKEN_PATH", "credentials/token.json")
	
	# Obtenemos autorización a partir del token obtenido con anterioridad si ya lo obtuvimos o lo solicitamos y guradamos antes de obtener la autorización. 
	creds = get_auth_token(credentials_path, token_path)
	# Conectamos con Gmail API: Creamos el objeto service que nos permite llamar a la API de Gmail.
	service = gmail_api_connection(creds)

	# Pedimos los últimos 10 correos (maxResults=10) o en una query de fecha (newer...)
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
				logger.error(f"Error readind the message {msg['id']}: {e}")

def main():
	setup_logging()
	try:
		run()
	except Exception as e:
		logger.critical(f"Fatal error: {e}")
		sys.exit(1)

if __name__ == '__main__':
	main()