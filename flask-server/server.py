import uuid

from flask import Flask, redirect, request, send_file, jsonify, render_template, abort
#import storage

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
        user = request.form['user']

        # Create id for image
        image_id = str(uuid.uuid4().hex)
        image_size = len(file.read())

        # Add owner, image_name, and image_id to database
        storage.add_db_entry(user, file.filename.split('.')[0], image_id, image_size)

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

    # Gets user paramater from get request and queries database for images pertaining to user
    user = request.args.get('user')
    images = storage.get_image_info(user)

    return jsonify(images)


@app.route('/download', methods=['GET'])
def download():
    # Print message to console indicating that the endpoint was hit
    print("GET /download")

    try:
        # Extract the value of the 'id' query parameter from the request, and locate the directory if image
        user = request.args.get('user')
        file_id = request.args.get('id')

        # Creates file name and downloads from bucket
        file_name = f"{file_id}.myjpeg"
        result = storage.download_from_bucket(file_name, user)

        if result is None:
            print("File not found")
            return 404

        return send_file(result, as_attachment=True, mimetype='image/jpeg', download_name=file_id)

    except Exception as ex:
        # If an exception occurs, return an error response
        print(f"Exception occurred: {ex}")

        return {'status': 'error', 'message': str(ex)}


@app.route('/delete', methods=['GET'])
def delete():
    # Print message to console indicating that the endpoint was hit
    print("GET /delete")

    try:
        # Extract the value of the 'id' and 'user' query parameter from the request
        user = request.args.get('user')
        file_id = request.args.get('id')

        # Creates file name and removes from database and bucket
        file_name = f"{file_id}.myjpeg"
        storage.remove_db_entry(file_id)
        storage.delete_from_bucket(file_name, user)

        return {'status': 'success', 'message': 'File deleted successfully'}

    except Exception as ex:
        # If an exception occurs, return an error response
        print(f"Exception occurred: {ex}")

        return {'status': 'error', 'message': str(ex)}


@app.route('/login', methods=['POST'])
def login():
    try:
        print("POST /login")

        # Gets user information from post request
        email = request.form['email']
        password = request.form['password']

        # Authenticates user information
        result = storage.authenticate_account(email, password)

        result_message = "failed"

        # If account was authenticated, return success else return failed
        if result is True:
            result_message = "success"
            print("Successfully authenticated account")

        print("User not authenticated")

        return jsonify(result_message)

    except Exception as ex:
        # If an exception occurs, return an error response
        print(f"Exception occurred: {ex}")
        result_message = "failed"

        return jsonify(result_message)


@app.route('/register', methods=['POST'])
def register():
    try:
        print("POST /register")

        # Gets user information from post request
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # Stores account information in database
        storage.create_account(email, password, first_name, last_name)

        print("Successfully registered account")

        return jsonify("success")

    except Exception as ex:
        # If an exception occurs, return an error response
        print(f"Exception occurred: {ex}")

        return jsonify("failed")


app.run(host='0.0.0.0', port=80)
