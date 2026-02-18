import io
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

def get_drive_service():
    SERVICE_ACCOUNT_FILE = 'service_account.json'
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    return build('drive', 'v3', credentials=creds)

def download_brochure(file_id, output_path="temp_brochure.pdf"):
    # If the file exists, just return the path
    if os.path.exists(output_path):
        return output_path

    # FIX: Notice there is NO comma here. Just 'service'.
    service = get_drive_service() 
    
    try:
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        
        with open(output_path, 'wb') as f:
            f.write(fh.getvalue())
            
        return output_path
    except Exception as e:
        print(f"Drive Error: {e}")
        return None