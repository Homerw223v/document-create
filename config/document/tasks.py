"""Tasks for document project."""
from celery import shared_task
from google.oauth2 import service_account as service_acc
from googleapiclient.discovery import Resource, build
from rest_framework import status

credentials: service_acc.Credentials = service_acc.Credentials.from_service_account_file('client_secrets.json')


@shared_task
def create_document(data: dict):
    """Task that create a document in Google Drive, add permissions and return a link to this file.

    Args:
        data (dict): Dictionary with name of the document, and it's content.

    Returns:
        dict(): Return status code and link to document.

    """
    try:
        service_docs: Resource = build('docs', 'v1', credentials=credentials)
        service_drive: Resource = build('drive', 'v3', credentials=credentials)
    except Exception:
        return {'error': 'Something went wrong. Try again later.'}
    else:
        document: dict = service_docs.documents().create(body={'title': data['name']}).execute()
        document_id: str = document['documentId']
        text_content: list = [
            {
                'insertText': {
                    'location': {
                        'index': 1,
                    }, 'text': data['data'],
                },
            },
        ]
        service_docs.documents().batchUpdate(
            documentId=document_id, body={'requests': text_content},
        ).execute()
        permission: dict = {
            'type': 'anyone',
            'role': 'reader',
            'value': 'anyoneWithLink',
        }
        service_drive.permissions().create(fileId=document_id, body=permission).execute()
        return {'status': status.HTTP_201_CREATED, 'link': f'https://drive.google.com/file/d/{document_id}/edit'}

