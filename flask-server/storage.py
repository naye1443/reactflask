from io import BytesIO
from google.cloud import datastore, storage
from PIL import Image
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ".\\keyfile.json"

bucket_dir = "images/"
project_id = "projecttwo-378620"
bucket_name = f"{project_id}-images"

datastore_client = datastore.Client()
storage_client = storage.Client()


def get_image_info(name="user"):
    try:
        print(f"Retrieving user: {name}'s information from database")

        # Defines query to search for images where owner = name
        query = datastore_client.query(kind="images")
        query.add_filter("owner", "=", name)

        # Lopps through query results and adds image information to list
        image_info = []
        for image in query.fetch():
            info = {
                "owner": image["owner"],
                "name": image["name"],
                "id": image["id"],
                "size": round(image["size"] / 1000, 2)
            }

            image_info.append(info)

        print(f"Retrieved user: {name}'s information from database")
        print(image_info)

        return image_info

    except Exception as ex:
        # If an exception occurs, return an error response
        print(f"Exception occurred: {ex}")
        return None


def add_db_entry(owner, image_name, image_id, image_size):
    try:
        print(f"Adding {image_name} to database")

        # Defines a new entity where key = image_id
        entity = datastore.Entity(key=datastore_client.key("images", image_id))

        # Sets values for entity properties
        entity.update({
            'owner': owner,
            'name': image_name,
            'id': image_id,
            'size': image_size
        })

        # Adds entity to database
        datastore_client.put(entity)

        print(f"Added {image_name} to database")

    except Exception as ex:
        # If an exception occurs, return an error response
        print(f"Exception occurred: {ex}")


def remove_db_entry(image_id):
    try:
        print(f"Removing {image_id} from database")

        # Defines the key to be removed from database
        key = datastore_client.key("images", image_id)

        # Deletes the entity with the matching key from database
        datastore_client.delete(key)

        print(f"Removed {image_id} from database")

    except Exception as ex:
        # If an exception occurs, return an error response
        print(f"Exception occurred: {ex}")


def upload_to_bucket(file, blob_name, owner):
    try:
        print(f"Uploading {blob_name} to bucket")

        # Set file pointer to beginning of file
        file.seek(0)

        # Define bucket and blob objects
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # Upload file to blob in the bucket
        blob.upload_from_file(file)

        print(f"Uploaded {blob_name} to bucket")

    except Exception as ex:
        # If an exception occurs, return an error response
        print(f"Exception occurred: {ex}")


def delete_from_bucket(blob_name):
    try:
        print(f"Removing {blob_name} from bucket")
        # Define bucket and blob objects
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # Delete blob from the bucket
        blob.delete()

        print(f"Removed {blob_name} from bucket")

    except Exception as ex:
        # If an exception occurs, return an error response
        print(f"Exception occurred: {ex}")


def download_from_bucket(blob_name):
    try:
        print(f"Downloading {blob_name} from bucket")

        # Define bucket and blob objects and checks if it exists
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # Exits if blob does not exist
        if not blob.exists():
            print(f"Blob {blob_name} does not exist")
            return

        # Download the blob to memory
        content = BytesIO()
        blob.download_to_file(content)

        # Convert the image to JPEG format
        image = Image.open(content)
        image = image.convert('RGB')
        jpeg_data = BytesIO()
        image.save(jpeg_data, format='JPEG')
        jpeg_data.seek(0)

        print(f"Downloaded {blob_name} from bucket")

        return content.getvalue()

    except Exception as ex:
        # If an exception occurs, return an error response
        print(f"Exception occurred: {ex}")
        return None
