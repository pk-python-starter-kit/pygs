#!/usr/bin/env python
import httplib2
import os
import string
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import datetime


service_dict = {
    'service': None,
    'last_updated': None
}

def _initializeService(initializing=None):
    global service_dict
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    APPLICATION_NAME = 'PYGS - Python for Google Sheets'
    
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    client_secret_dir = os.path.join(home_dir, 'clientsecrets')
    
    if not os.path.exists(client_secret_dir):
        os.makedirs(client_secret_dir)
        
    CLIENT_SECRET_FILE = os.path.join(client_secret_dir, 'client_secret.json')

    
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    
    credential_path = os.path.join(credential_dir,'sheets.googleapis.com-pygs-api-auth.json')

    store = Storage(credential_path)
    
    credentials = store.get()
    
    if not credentials or credentials.invalid:
        print "Credentials need to be created. Please allow access on the next screen and then re-run the command."
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        flags = tools.argparser.parse_args(args=[])
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)

    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    
    if initializing:
        service_dict['service'] = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
        service_dict['last_updated'] = datetime.datetime.now()
    else:
        return discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    

def _getService():
    global service_dict
    #get a new service every 30 minutes
    outdated = False
    if datetime.datetime.now() > service_dict['last_updated'] +  datetime.timedelta(minutes=1):
        outdated = True

    if service_dict['service'] == None or outdated:
        service_dict['service'] = _initializeService()
        return service_dict['service']
    else:
        return service_dict['service']