from google.cloud import datastore, storage
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = '../auth/projecttwo_token.json'

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

bucket_dir = "images/"
bucket_name = "projecttwo-378620-images"

datastore_client = datastore.Client(credentials.project_id,None,credentials)
storage_client = storage.Client(credentials.project_id, None,credentials)

def get_image_info(name="test"):
    query = datastore_client.query(name=name)

    for image in query.fetch():
        print(image.items())


def add_db_entry(owner, image_name, image_id):
    entity = datastore.Entity(key=datastore_client.key('images'))
    entity.update({
        'owner': owner,
        'image_name': image_name,
        'image_id': image_id,
    })
    datastore_client.put(entity)


def upload_to_bucket(file_path, blob_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(file_path)
