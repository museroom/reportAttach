from __future__ import print_function
import httplib2
import os
import io
import base64
import re

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaIoBaseDownload, MediaFileUpload

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.readonly',
]
CLIENT_SECRET_FILE = 'client_secret_forgot.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-forgot.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def upload_doc(service, filename):
    file_metadata = {
        'name': filename.replace('docx', 'gdoc'),
        'mimeType': 'application/vnd.google-apps.document'
    }
    media = MediaFileUpload(
        filename,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id').execute()
    # print('File ID: %s' % file.get('id'))
    print('success upload {}'.format(filename))


def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    # list dir in attachment
    source_dir = os.path.join('.', 'attachments')
    file_list = []
    for file in os.listdir(source_dir):
        res = re.search(r'201.*docx', file)
        if res:
            file_list.append(file)

    for file in file_list:
        filename = os.path.join(
            'attachments',
            file,
        )
        upload_doc(service, filename)


if __name__ == '__main__':
    main()
