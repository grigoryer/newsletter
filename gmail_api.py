import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from google_apis import create_service

def init_gmail_service(client_file, api_name='gmail', api_version='v1', scopes=['https://mail.google.com/']):
    return create_service(client_file, api_name, api_version, scopes)

def send_email(service, to_list, subject, body, body_type, attachment_paths=None):
    message = MIMEMultipart()
    message['bcc'] = ', '.join(to_list)
    message['subject'] = subject

    if body_type.lower() not in ['plain', 'html']:
        raise ValueError("body_type must be either 'plain' or 'html'")

    message.attach(MIMEText(body, body_type.lower()))

    if attachment_paths:
        for attachment_path in attachment_paths:
            if os.path.exists(attachment_path):
                filename = os.path.basename(attachment_path)

                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())

                encoders.encode_base64(part)

                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={filename}",
                )

                message.attach(part)
            else:
                raise FileNotFoundError(f"File not found - {attachment_path}")

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    sent_message = service.users().messages().send(
        userId='me', 
        body={'raw': raw_message}
    ).execute()

    print(f"Message sent to {len(to_list)} recipients.")
    return sent_message
