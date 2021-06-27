from __future__ import print_function
import os.path
import pickle
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
from base64 import urlsafe_b64encode

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from mimetypes import guess_type as guess_mime_type

from bd.kioscomongo import Kiosco

class Correo():
    def __init__(self, pathconfig):
        fconfig = open(pathconfig)
        config = json.load(fconfig)

        # si se modificaron los 'scopes', entonces hay q eliminar 'tokens.pickle' para q se vuelva a generar.
        self.scopes = [config['correo']['scope']]
        self.credenciales = config['correo']['credenciales']
        self.token = config['correo']['token']
        self.cuenta = config['correo']['cuenta']
        self.auth(self.scopes, self.credenciales, self.token)

    def auth(self, scopes, credenciales, token):
        creds = None

        # si existe info del token, se levanta. sino, hay que generarlo (en teoria por primera y unica vez).
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        
        # si no hay credenciales, hacer que se logee desde el navegador
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credenciales, scopes)
                creds = flow.run_local_server(port=0)
            # save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)
        self.servicio = build('gmail', 'v1', credentials=creds)

    def armar_mensaje(self, destinatario, titulo, texto, adjuntos=[]):
        if not adjuntos: # no attachments given
            mensaje = MIMEText(texto)
            mensaje['content_type'] = 'text/html'
            mensaje['to'] = destinatario
            mensaje['from'] = self.cuenta
            mensaje['subject'] = titulo
        else:
            mensaje = MIMEMultipart()
            mensaje['content_type'] = 'text/html'
            mensaje['to'] = destinatario
            mensaje['from'] = self.cuenta
            mensaje['subject'] = titulo
            mensaje.attach(MIMEText(texto))
            for filename in adjuntos:
                self.agregar_adjunto(mensaje, filename)
        return {'raw': urlsafe_b64encode(mensaje.as_bytes()).decode()} 

    def agregar_adjunto(self, mensaje, filename):
        content_type, encoding = guess_mime_type(filename)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(filename, 'rb')
            msg = MIMEText(fp.read().decode(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(filename, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(filename, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(filename, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()
        filename = os.path.basename(filename)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        mensaje.attach(msg)

    def enviar(self, destinatario, titulo, texto, adjuntos=[]):
        return self.servicio.users().messages().send(
            userId="me",
            body=self.armar_mensaje(destinatario, titulo, texto, adjuntos)).execute()
