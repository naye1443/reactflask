from io import BytesIO
from PIL import Image
from google.cloud import datastore, storage
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ".\\keyfile.json"

bucket_dir = "images/"
project_id = "projecttwo-378620"
bucket_name = f"{project_id}-images"

datastore_client = datastore.Client()
storage_client = storage.Client()


def get_image_info(name="user"):
    try:
        print(f"Retrieving user: {name}'s images from database")

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

        print(f"Retrieved user: {name}'s images from database")
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
        print(f"Uploading {owner}/{blob_name} to bucket")

        # Set file pointer to beginning of file
        file.seek(0)

        # Define bucket and blob objects
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(f"{owner}/{blob_name}")

        # Create owner subdirectory if it doesn't exist
        if not bucket.blob(f"{owner}").exists():
            sub_blob = bucket.blob(f"{owner}")
            sub_blob.create_resumable_upload_session()

        # Upload file to blob in the bucket
        blob.upload_from_file(file)

        print(f"Uploaded {owner}/{blob_name} to bucket")

    except Exception as ex:
        # If an exception occurs, return an error response
        print(f"Exception occurred: {ex}")


def delete_from_bucket(blob_name, owner="user"):
    try:
        print(f"Removing {owner}/{blob_name} from bucket")
        # Define bucket and blob objects
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(f"{owner}/{blob_name}")

        # Delete blob from the bucket
        blob.delete()

        print(f"Removed {owner}/{blob_name} from bucket")

    except Exception as ex:
        # If an exception occurs, return an error response
        print(f"Exception occurred: {ex}")


def download_from_bucket(blob_name, owner="user"):
    try:
        print(f"Downloading {owner}/{blob_name} from bucket")

        # Define bucket and blob objects
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(f"{owner}/{blob_name}")

        # Exits if blob does not exist
        if not blob.exists():
            print(f"Blob {owner}/{blob_name} does not exist")
            return

        # Download the blob to memory
        in_mem_file = BytesIO()
        blob.download_to_file(in_mem_file)
        in_mem_file.seek(0)

        # Open the image file and convert it to JPEG
        with Image.open(in_mem_file) as img:
            img = img.convert('RGB')
            out_mem_file = BytesIO()
            img.save(out_mem_file, format='JPEG')
            out_mem_file.seek(0)

        print(f"Downloaded {owner}/{blob_name} from bucket")

        return out_mem_file

    except Exception as ex:
        # If an exception occurs, return an error response
        print(f"Exception occurred: {ex}")
        return None


def create_account(email, password, first_name, last_name):
    try:
        print(f"Adding {email} to database")

        # Defines a new entity where key = email
        entity = datastore.Entity(key=datastore_client.key("users", email))

        # Sets values for user account
        entity.update({
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name
        })

        # Adds user to database
        datastore_client.put(entity)

        print(f"Added {email} to database")

    except Exception as ex:
        # If an exception occurs, return an error response
        print(f"Exception occurred: {ex}")


def authenticate_account(email, password):
    try:
        print(f"Authenticating {email}")

        # Queries for users information and fetches first match
        query = datastore_client.query(kind="users")
        query.add_filter("email", "=", email)
        query.add_filter("password", "=", password)
        result = query.fetch(1)
        user = list(result)

        # Returns False if user is not found,
        if not user:
            return False

        # elif user is found, return True
        elif user[0]["email"] == email:
            print(f"User found in database")
            return True

    except Exception as ex:
        # If an exception occurs, return an error response
        print(f"Exception occurred: {ex}")
        return False
