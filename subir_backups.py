import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    creds = Credentials.from_authorized_user_file('/home/ubuntu/keys/token.json', SCOPES)
    service = build('drive', 'v3', credentials=creds)

    string_ayer = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    # subo noticias de ayer
    name = 'backups_dlm/noticias/' + string_ayer + '.json'
    path = '/home/ubuntu/backups_dlm/diarios/noticias/' + string_ayer + '.json'
    metadata = {'name': name}
    media = MediaFileUpload(path, mimetype='text/json')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # subo frecuencias de ayer
    name = 'backups_dlm/frecuencias/' + string_ayer + '.json'
    path = '/home/ubuntu/backups_dlm/diarios/noticias/' + string_ayer + '.json'
    metadata = {'name': name}
    media = MediaFileUpload(path, mimetype='text/json')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

if __name__ == '__main__':
    main()