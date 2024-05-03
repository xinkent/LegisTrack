import os
from google.cloud import storage as gcs
from google.oauth2.service_account import Credentials


class CloudStorageClient:
    BUCKET_NAME = 'bill_of_low'

    def __init__(self):
        env = os.environ["ENV"]
        PROJECT_ID = os.environ['PROJECT_ID']
        if env=="local":
            cred = Credentials.from_service_account_info({
                "type": "service_account",
                "project_id": os.environ["PROJECT_ID"],
                "private_key_id": os.environ["PRIVATE_KEY_ID"],
                "private_key": os.environ["PRIVATE_KEY"].replace("\\n", "\n"),
                "client_email": os.environ["CLIENT_MAIL"],
                "client_id": os.environ["CLIENT_ID"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": os.environ["CLIENT_X509_CERT_URL"]
            })
            self.client = gcs.Client(credentials=cred)
        else:
            self.client = gcs.Client(PROJECT_ID)

    def upload_csv(self, contents: str, filename: str):
        bucket = self.client.get_bucket(CloudStorageClient.BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(contents)
