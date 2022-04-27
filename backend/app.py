import os

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

UPLOAD_DIRECTORY = './tmp/'

if not os.path.exists(UPLOAD_DIRECTORY):
    os.mkdir(UPLOAD_DIRECTORY)

app = Flask(__name__)


@app.route('/receive', methods=['POST'])
def form():
    """Get wav file"""
    file = request.files['file']
    if file.filename is not None:
        filename = secure_filename(filename=file.filename)
        file.save(os.path.join(UPLOAD_DIRECTORY, filename))
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})


@app.route('/', methods=['GET'])
def hello():
    """Render html"""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
