from googleapiclient.discovery import build

def gmail_api_connection(creds):
    """Connect to the Gmail API"""

    # Connect to the Gmail API by creating the service object,
    # which allows us to make Gmail API calls.
    return build('gmail', 'v1', credentials=creds)