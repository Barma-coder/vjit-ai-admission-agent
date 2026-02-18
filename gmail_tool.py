import os
import base64
import pickle
from email.message import EmailMessage
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def get_gmail_service():
    SCOPES = ['https://www.googleapis.com/auth/gmail.compose']
    creds = None
    if os.path.exists('gmail_token.pickle'):
        with open('gmail_token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('gmail_token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            
    return build('gmail', 'v1', credentials=creds)

def create_gmail_draft(user_query, ai_response, recipient_email):
    try:
        # FIX: We call our own local service function
        service = get_gmail_service()

        message = EmailMessage()
        message.set_content(ai_response)
        message['To'] = recipient_email
        message['Subject'] = f"Regarding: {user_query[:30]}"
        
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'message': {'raw': encoded_message}}
        
        draft = service.users().drafts().create(userId="me", body=create_message).execute()
        print(f"✅ Draft created! ID: {draft['id']}")
    except Exception as e:
        print(f"❌ Gmail Error: {e}")