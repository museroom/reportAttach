# from __future__ import print_function
import httplib2
import os
import base64

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient import errors


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret_sc.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


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
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
      print('Labels:')
      for label in labels:
        print(label)
        if 'Daily Report' in label['name']:
            label_id = print(label['id'])

    results = service.users().messages().list(userId='me',labelIds=label_id).execute()
    print(results)

    message = service.users().messages().get(userId='me',id='1620ac31c0adbc42').execute()
    store_dir = os.path.join('.','attachments')

    try:
        attach_id = message['payload']['parts'][1]['body']['attachmentId']
        attach = service.users().messages().attachments().get(
            userId='me',messageId='1620ac31c0adbc42',id=attach_id
        ).execute()
        data = attach['data']
        file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
        path = os.path.join(store_dir,message['payload']['parts'][1]['filename'])

        with open(path, 'wb') as f:
            f.write(file_data)
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

if __name__ == '__main__':
    main()