from google.cloud import datastore, storage
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ".\\keyfile.json"

bucket_dir = "images/"
project_id = "projecttwo-378620"
bucket_name = f"{project_id}-images"

datastore_client = datastore.Client()
storage_client = storage.Client()


def get_image_info(name="test"):
    query = datastore_client.query(name=name)

    for image in query.fetch():
        print(image.items())


def add_db_entry(owner, image_name, image_id):
    entity = datastore.Entity(key=datastore_client.key('images'))
    entity.update({
        'owner': owner,
        'name': image_name,
        'id': image_id,
    })
    datastore_client.put(entity)


def upload_to_bucket(file, blob_name, owner):
    file = file.read()
    file_path = f"{owner}/{file}"
    print(file)
    print(blob_name)

    bucket = storage_client.bucket(bucket_name)
    print("set bucket name")
    blob = bucket.blob(blob_name)
    print("set blob name")
    blob.upload_from_filename(file_path)
    print("uploaded to bucket")
