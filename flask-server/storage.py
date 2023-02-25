from google.cloud import datastore, storage

bucket_dir = "images/"
bucket_name = "projecttwo-378620-images"

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
        'image_name': image_name,
        'image_id': image_id,
    })
    datastore_client.put(entity)


def upload_to_bucket(file_path, blob_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(file_path)
