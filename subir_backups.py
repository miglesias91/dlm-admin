import os.path
import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    creds = Credentials.from_authorized_user_file('/home/ubuntu/keys/token.json', SCOPES)
    service = build('drive', 'v3', credentials=creds)

    string_ayer = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    # abro config
    fconfig = open('config.json')
    config = json.load(fconfig)
    id_carpeta_noticias = config['ids_carpetas']['noticias']
    id_carpeta_frecuencias = config['ids_carpetas']['frecuencias']

    # subo noticias de ayer
    name = string_ayer + '.json'
    path = '/home/ubuntu/backups_dlm/diarios/noticias/' + string_ayer + '.json'
    metadata = {'name': name, 'parents' : [ id_carpeta_noticias ]}
    media = MediaFileUpload(path, mimetype='text/json')
    file = service.files().create(body=metadata, media_body=media, fields='id').execute()

    # subo frecuencias de ayer
    name = string_ayer + '.json'
    path = '/home/ubuntu/backups_dlm/diarios/noticias/' + string_ayer + '.json'
    metadata = {'name': name, 'parents' : [ id_carpeta_frecuencias ]}
    media = MediaFileUpload(path, mimetype='text/json')
    file = service.files().create(body=metadata, media_body=media, fields='id').execute()

if __name__ == '__main__':
    main()