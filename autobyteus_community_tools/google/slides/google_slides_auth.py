import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

class GoogleSlidesAuth:
    """Singleton class to handle Google Slides API authentication."""

    _instance = None
    SCOPES = ['https://www.googleapis.com/auth/presentations']

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GoogleSlidesAuth, cls).__new__(cls)
            cls._instance.creds = None
            cls._instance.credentials_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json')
            cls._instance.token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'token.pickle')
        return cls._instance

    def authenticate(self):
        """Authenticate and return credentials for Google Slides API."""
        if self.creds and self.creds.valid:
            return self.creds

        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open(self.token_path, 'wb') as token:
                pickle.dump(self.creds, token)

        return self.creds

    def load_credentials(self):
        """Load credentials from the token file if it exists."""
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                self.creds = pickle.load(token)