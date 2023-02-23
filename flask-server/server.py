import os
from flask import Flask, redirect, request, send_file, jsonify

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload():
    try:
        print("POST /upload")
        file = request.files['form_file']
        file.save(os.path.join("./files", file.filename))

    except Exception as ex:
        print(f"Exception occured: {ex}")

    return redirect('/')


@app.route('/files')
def list_of_files():
    print("GET /files")

    files = os.listdir("./files")

    images = []

    for file in files:
        if file.endswith(".jpeg"):
            images.append(file)

    data = {
        'name': 'Test Image',
        'id': '123123',
        'size': '7.5',
    }

    return jsonify(data)


@app.route('/files/<filename>')
def get_file(filename):
    directory = './files'

    print(f"GET /files/{filename}")
    return send_file(f"{directory}/{filename}")


app.run(host='0.0.0.0', port=8080)
