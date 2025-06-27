import os

from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions, ContentSettings
from dotenv import load_dotenv
from datetime import datetime, timedelta
from app.image.storage.image_storage import ImageStorage

load_dotenv()

CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")
ACCOUNT_KEY = os.getenv("AZURE_CONTAINER_ACCOUNT_KEY")

blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)


class AzureBlobStorage(ImageStorage):

    def upload_file(self, contents, filename):
        try:
            blob_client = container_client.get_blob_client(filename)

            blob_client.upload_blob(
                contents,
                overwrite=True,
                content_settings=ContentSettings(
                    content_type="image/jpeg",
                    content_disposition="inline"
                )
            )

            blob_url = self.generate_sas_url(blob_client)
            return blob_url
        except Exception as ex:
            print(f"Upload Error : {ex}")
            raise ex

    @staticmethod
    def generate_sas_url(blob_client):
        sas_token = generate_blob_sas(
            account_name=blob_client.account_name,
            account_key=ACCOUNT_KEY,
            container_name=blob_client.container_name,
            blob_name=blob_client.blob_name,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(days=10),
        )
        sas_url = f"{blob_client.url}?{sas_token}"
        return sas_url
