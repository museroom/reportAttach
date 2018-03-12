from __future__ import print_function
import httplib2
import os
import io
import base64

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaIoBaseDownload

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


def get_filelist(service, parent_id, page_size):
    results = service.files().list(
        pageSize=400,
        # fields="nextPageToken, files(id, name)",
        # fields="files(parents,id,name)",
        # q='\'1oCeUMjXlyCE5yydNUOCb1TZ3K66uE6P5\' in parents',
        q="parents = '{}'".format(parent_id)
    ).execute()
    items = results.get('files', [])
    return items


def download_htmls(service, items, store_dir):
    if not os.path.exists(store_dir):
        os.mkdir(store_dir)

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for i, item in enumerate(items, 1):
            if not any(ext in item['name'] for ext in ['docx']):
                continue
            print('{0} ({1})'.format(item['name'], item['id']))

            request = service.files().export(
                fileId=item['id'],
                # mimeType='application/pdf',
                mimeType='application/zip'
            ).execute()

            try:
                # data = request['data']
                filename = item['name'].replace('docx','zip')
                # file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                file_data = request
                path = os.path.join(store_dir,filename)

                if not os.path.exists(store_dir):
                    os.mkdir(store_dir)
                with open(path, 'wb') as f:
                    f.write(file_data)
                print('success save {}'.format(filename))
            except Exception as e:
                print( 'error save {}'.format(e))

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    items = get_filelist(
        service,
        '1oCeUMjXlyCE5yydNUOCb1TZ3K66uE6P5',
        400
    )

    store_dir = os.path.join('.', 'assets')

    download_htmls(service, items, store_dir)


if __name__ == '__main__':
    main()
