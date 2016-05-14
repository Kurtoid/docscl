"""
Program to edit Google Docs in editors like Vim
"""
from __future__ import print_function
import httplib2

from apiclient import discovery
from apiclient.http import MediaIoBaseDownload
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
#    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    PARSER = argparse.ArgumentParser(parents=[tools.argparser])
    PARSER.add_argument('key')
    flags = PARSER.parse_args()
except ImportError:
    flags = None
import sys
import io
import os

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
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
                                   'drive-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    """
    main method
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    """
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))
    """
    items = getId(service, sys.argv[1])
    if not items:
        print('No files found')
        exit()
    else:
        print('files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))
        if items.length > 1:
            print('First file selected')
    item = items[0]
    request = service.files.export_media(fileId=item['id'],
                                         mimeType='text/plain')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    fileText = fh.getvalue()
    file = open(item['name']+'.txt', 'w')
    file.write(fileText)
    file.close()
    """
    file_id = getId(service, sys.argv[1])
    request = service.files().export_media(fileId=file_id,
                                           mimeType='text/plain')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    print(fh.getvalue())
    """

#    request = service.files.export_media(

nofileselectedid = "1Jvoj6-OtmnWMRLyEmK2YeyRvAEC5yQ7HNGDwcdGleZw"


def getId(service, filename=nofileselectedid):
    results = service.files().list(q="name = '" + filename + "' and mimeType = 'application/vnd.google-apps.document'", ).execute()
    items = results.get('files', [])
    if not items:
        print('No files found')
        return
    return items

if __name__ == "__main__":
    print("Running!")
    main()
