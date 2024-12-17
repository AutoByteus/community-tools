from googleapiclient.discovery import build

from autobyteus_community_tools.google.slides.google_slides_auth import GoogleSlidesAuth

class GoogleSlidesPresentation:
    def __init__(self):
        self.auth = GoogleSlidesAuth()
        self.service = build('slides', 'v1', credentials=self.auth.authenticate())
        self.presentation_id = None

    def create_presentation(self, title):
        presentation = self.service.presentations().create(body={'title': title}).execute()
        self.presentation_id = presentation.get('presentationId')
        return self.presentation_id

    def add_slide(self, layout):
            requests = [
                {
                    'createSlide': {
                        'slideLayoutReference': {
                            'predefinedLayout': layout
                        },
                        'placeholderIdMappings': [
                            {
                                'layoutPlaceholder': {
                                    'type': 'TITLE'
                                },
                                'objectId': 'TITLE'
                            },
                            {
                                'layoutPlaceholder': {
                                    'type': 'BODY'
                                },
                                'objectId': 'BODY'
                            }
                        ]
                    }
                }
            ]
            response = self.service.presentations().batchUpdate(
                presentationId=self.presentation_id,
                body={'requests': requests}
            ).execute()
            slide_id = response.get('replies')[0].get('createSlide').get('objectId')
            return slide_id, 'TITLE', 'BODY'

    def add_text_to_slide(self, slide_id, title_id, body_id, title, content):
        requests = [
            {
                'insertText': {
                    'objectId': title_id,
                    'insertionIndex': 0,
                    'text': title
                }
            },
            {
                'insertText': {
                    'objectId': body_id,
                    'insertionIndex': 0, 
                    'text': content
                }
            }
        ]
        self.service.presentations().batchUpdate(
            presentationId=self.presentation_id,
            body={'requests': requests}
        ).execute()

    def open_presentation(self, presentation_id):
        self.presentation_id = presentation_id