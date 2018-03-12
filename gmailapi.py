# from __future__ import print_function
import httplib2
import os
import base64

import logging

logger = logging.getLogger('gmail')

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
        logger.info('Storing credentials to ' + credential_path)
    return credentials

def get_message_lists( service, label_filter, max_page=10):
    messages = []

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        logger.info('No labels found.')
    else:
        for label in labels:
            if label_filter in label['name']:
                label_id = logger.info(label['id'])

    results = service.users().messages().list(userId='me',labelIds=label_id).execute()
    messages.extend(results['messages'])
    logger.info('Getting gmail label {}:'.format(label_filter))
    for i in range(0,max_page):
        logger.info(i)
        nextpage = results.get('nextPageToken', None)
        if nextpage:
            results = service.users().messages().list(userId='me',labelIds=label_id,pageToken=nextpage).execute()
            messages.extend(results['messages'])
        else:
            logger.warning( 'End of pages')
            break

    return messages

def get_message( service, message_id ):
    attach_ids = []

    try:
        message = service.users().messages().get(
            userId = 'me', id=message_id
        ).execute()
        for part in message['payload']['parts']:
            if part['filename']:
                if any(item in part['filename'].lower() for item in ['jpg', 'emz', 'png']):
                    continue
                attach_ids.append( {
                    'id':part['body']['attachmentId'],
                    'filename': part['filename']
                })
    except Exception as e:
        logger.error( 'Error get message:{}'.format(e))

    return attach_ids

def save_attachment( service, attach_id, message_id, store_dir, filename):
    try:
        # attach_id = message['payload']['parts'][1]['body']['attachmentId']
        attach_id = attach_id
        attach = service.users().messages().attachments().get(
            userId='me',messageId=message_id,id=attach_id
        ).execute()
        data = attach['data']
        file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
        path = os.path.join(store_dir,filename)

        if not os.path.exists(store_dir):
            os.mkdir(store_dir)
        with open(path, 'wb') as f:
            f.write(file_data)
        logger.info('success save {}'.format(filename))
    except errors.HttpError as error:
        logger.error('An error occurred: %s' % error)

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    messages = get_message_lists(
        service, 'Daily Report', max_page=50
    )

    store_dir = os.path.join('.','attachments')

    logger.info( 'get total messages: {:,}'.format(
        len(messages),
    ))

    for message in messages:
        attach_ids = get_message( service, message['id'])
        for attach_id in attach_ids:
            save_attachment(
                service,
                attach_id['id'],
                message['id'],
                store_dir,
                attach_id['filename']
            )


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG
    )
    logging.getLogger('googleapiclient').setLevel(logging.CRITICAL)
    main()
