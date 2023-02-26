import uuid

from flask import Flask, redirect, request, send_file, jsonify, render_template, abort
import storage

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")


@app.route("/upload", methods=['POST'])
def upload():
    print("POST /upload")

    try:
        # Retrieve the file from the POST request
        file = request.files['form_file']
        #user = request.files['user']
        user = "user"

        # Create id for image
        image_id = str(uuid.uuid4().hex)
        image_size = len(file.read())

        # Add owner, image_name, and image_id to database
        storage.add_db_entry(user, file.filename.split('.')[0], image_id, image_size)
        print("added to db")

        # Upload the file to the bucket
        blob_name = f"{image_id}.myjpeg"
        storage.upload_to_bucket(file, blob_name, user)
        print("added to bucket")

        # Return a success response
        return {'status': 'success', 'message': 'File uploaded successfully'}

    except Exception as ex:
        # If an exception occurs, return an error response
        print(f"Exception occurred: {ex}")

        return {'status': 'error', 'message': str(ex)}


@app.route('/files', methods=['GET'])
def get_images():
    # Print message to console indicating that the endpoint was hit
    print("GET /files")

    images = storage.get_image_info("user")

    return jsonify(images)


@app.route('/download')
def download():
    # Print message to console indicating that the endpoint was hit
    print("GET /download")

    try:
        # Extract the value of the 'id' query parameter from the request, and locate the directory if image
        file_id = request.args.get('id')
        file_name = f"{file_id}.myjpeg"
        result = storage.download_from_bucket(file_name)

        if result is None:
            print("File not found")
            return 404

        return send_file(result, as_attachment=True, mimetype='image/jpeg', download_name=file_id)

    except Exception as ex:
        # If an exception occurs, return an error response
        print(f"Exception occurred: {ex}")

        return {'status': 'error', 'message': str(ex)}


@app.route('/delete')
def delete():
    # Print message to console indicating that the endpoint was hit
    print("GET /delete")

    try:
        # Extract the value of the 'id' query parameter from the request, and locate the directory if image
        file_id = request.args.get('id')
        directory = './owner/files'
        file_name = f"{file_id}.myjpeg"
        storage.remove_db_entry(file_id)
        storage.delete_from_bucket(file_name)

        return {'status': 'success', 'message': 'File deleted successfully'}

    except Exception as ex:
        # If an exception occurs, return an error response
        print(f"Exception occurred: {ex}")

        return {'status': 'error', 'message': str(ex)}


app.run(host='0.0.0.0', port=80)
