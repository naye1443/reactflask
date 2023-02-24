import os
from flask import Flask, redirect, request, send_file, jsonify, render_template, abort

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():
    try:
        # TODO
        # Create hash for image
        # Add owner, image name, image hash to database
        # Add image to database saved as hash.myjpeg

        # Print message to console indicating that the endpoint was hit
        print("POST /upload")

        # Retrieve the file from the POST request, modify the file name to include the ".myjpeg"
        # extension and save to directory
        file = request.files['form_file']
        directory = "./files"
        file_name = f"{file.filename.split('.')[0]}.myjpeg"
        file.save(os.path.join(directory, file_name))

    except Exception as ex:
        # If an exception occurs, print the error message to the console and return an error response
        print(f"Exception occurred: {ex}")
        return {'status': 'error', 'message': str(ex)}

        # If the file was successfully uploaded, return a success response
    return {'status': 'success', 'message': 'File uploaded successfully'}


@app.route('/files', methods=['GET'])
def list_of_files():
    # TODO
    # Get hashes associated to user_name from database and store as a list
    # Foreach image metadata retrieved, set image object to corresponding values

    # Print message to console indicating that the endpoint was hit
    print("GET /files")

    files = os.listdir("./files")
    images = []

    for file in files:
        # Extract information about the image
        name = file.split('.')[0]
        id = hash(file)
        size = os.path.getsize(os.path.join('./files', file))

        # Create a dictionary representing the image
        image_info = {
            'name': name,
            'id': id,
            'size': size,
        }

        # Adds image_info to images list
        images.append(image_info)

    return jsonify(images)


@app.route('/download')
def download():
    # TODO
    # Check database where id == file_id
    # return image in accordance to this

    # Print message to console indicating that the endpoint was hit
    print("GET /download")

    # Extract the value of the 'id' query parameter from the request, and locate the directory if image
    file_id = request.args.get('id')
    directory = './files'
    file_name = f"{file_id}.myjpeg"
    file_path = os.path.join(directory, file_name)

    # Check if the file exists at the given path
    if not os.path.exists(file_path):
        # If the file does not exist, abort the request with a 404 status code and an error message
        abort(404, f"File not found: {file_id}")

    # If the file exists, send the file to the client with the specified file path and filename
    print(f"GET /files/{file_id}")
    return send_file(file_path, as_attachment=True)


@app.route('/delete')
def delete():
    # TODO
    # Delete image where id == file_id
    # Delete row in database where id == file_id

    # Print message to console indicating that the endpoint was hit
    print("GET /delete")

    # Get file ID from query parameter
    file_id = request.args.get('id')

    # Get path to file
    directory = './files'
    file_name = f"{file_id}.myjpeg"
    file_path = os.path.join(directory, file_name)

    # Check if file exists
    if not os.path.exists(file_path):
        abort(404, f"File not found: {file_id}")

    # Delete file
    os.remove(file_path)

    # Return success message
    return "File deleted successfully"


app.run(host='0.0.0.0', port=80)
