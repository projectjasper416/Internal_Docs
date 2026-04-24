import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import PyPDF2
from docx import Document
from bs4 import BeautifulSoup
import tempfile
import shutil
from app.utils.text_processor import TextProcessor

class GoogleDriveService:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
        self.credentials = None
        self.service = None
        self.text_processor = TextProcessor()
        
    def authenticate(self):
        """Authenticate with Google Drive API"""
        creds = None
        
        # Check if credentials file exists
        if os.path.exists('credentials.json'):
            creds = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', self.SCOPES).run_local_server(port=8080)
        else:
            # For development, create a mock service
            print("Warning: credentials.json not found. Using mock service for development.")
            return None

        return build('drive', 'v3', credentials=creds)
    
    def list_documents(self):
        """List all documents from Google Drive"""
        if not self.service:
            self.service = self.authenticate()
            if not self.service:
                return []
        
        try:
            # Query for supported file types
            query = "mimeType='application/vnd.google-apps.document' or " \
                   "mimeType='application/vnd.google-apps.spreadsheet' or " \
                   "mimeType='application/pdf' or " \
                   "mimeType='text/plain' or " \
                   "mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document'"
            
            results = self.service.files().list(
                q=query,
                pageSize=100,
                fields="nextPageToken, files(id, name, mimeType, modifiedTime)"
            ).execute()
            # files = results.get('files', [])
            # print(f"📄 Total files found: {len(files)}")
            # for file in files:
            #     print(f"📌 {file['name']} | MIME: {file['mimeType']} | ID: {file['id']}")

            return results.get('files', [])
            
        except Exception as e:
            print(f"Error listing documents: {e}")
            return []
    
    def extract_text_from_google_doc(self, file_id):
        """Extract text from Google Doc"""
        try:
            file = self.service.files().export(
                fileId=file_id,
                mimeType='text/html'
            ).execute()
            
            # Parse HTML and extract text
            soup = BeautifulSoup(file, 'html.parser')
            text = soup.get_text()
            return text
            
        except Exception as e:
            print(f"Error extracting text from Google Doc {file_id}: {e}")
            return ""
    
    def extract_text_from_google_sheet(self, file_id):
        """Extract text from Google Sheet"""
        try:
            file = self.service.files().export(
                fileId=file_id,
                mimeType='text/csv'
            ).execute()
            
            return file.decode('utf-8')
            
        except Exception as e:
            print(f"Error extracting text from Google Sheet {file_id}: {e}")
            return ""
    
    def extract_text_from_pdf(self, file_id):
        """Extract text from PDF"""
        try:
            request = self.service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            
            fh.seek(0)
            
            # Read PDF
            pdf_reader = PyPDF2.PdfReader(fh)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text
            
        except Exception as e:
            print(f"Error extracting text from PDF {file_id}: {e}")
            return ""
    
    def extract_text_from_docx(self, file_id):
        """Extract text from DOCX"""
        try:
            request = self.service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            
            fh.seek(0)
            
            # Read DOCX
            doc = Document(fh)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text
            
        except Exception as e:
            print(f"Error extracting text from DOCX {file_id}: {e}")
            return ""
    
    def extract_text_from_plain_text(self, file_id):
        """Extract text from plain text file"""
        try:
            request = self.service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            
            fh.seek(0)
            return fh.read().decode('utf-8')
            
        except Exception as e:
            print(f"Error extracting text from plain text {file_id}: {e}")
            return ""
    
    def extract_text_from_file(self, file_id, mime_type):
        """Extract text from file based on MIME type"""
        if mime_type == 'application/vnd.google-apps.document':
            return self.extract_text_from_google_doc(file_id)
        elif mime_type == 'application/vnd.google-apps.spreadsheet':
            return self.extract_text_from_google_sheet(file_id)
        elif mime_type == 'application/pdf':
            return self.extract_text_from_pdf(file_id)
        elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            return self.extract_text_from_docx(file_id)
        elif mime_type == 'text/plain':
            return self.extract_text_from_plain_text(file_id)
        else:
            print(f"Unsupported MIME type: {mime_type}")
            return ""
    
    def index_documents(self):
        """Index all documents from Google Drive"""
        documents = self.list_documents()
        indexed_docs = []
        
        for doc in documents:
            try:
                text = self.extract_text_from_file(doc['id'], doc['mimeType'])
                if text.strip():
                    # Process and chunk the text
                    chunks = self.text_processor.chunk_text(text)
                    
                    for i, chunk in enumerate(chunks):
                        indexed_docs.append({
                            'id': f"{doc['id']}_{i}",
                            'content': chunk,
                            'source': doc['name'],
                            'file_id': doc['id'],
                            'mime_type': doc['mimeType'],
                            'modified_time': doc['modifiedTime']
                        })
                        
            except Exception as e:
                print(f"Error processing document {doc['name']}: {e}")
                continue
        
        # Store in vector database (this will be handled by RAG service)
        return {
            'total_documents': len(documents),
            'indexed_chunks': len(indexed_docs),
            'documents': indexed_docs
        } 