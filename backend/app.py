import os

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import joblib
import numpy as np
import librosa
from sklearn.preprocessing import scale
import warnings

warnings.filterwarnings("ignore")

model = joblib.load(open("../model/saved_model/model_lgbm.pkl", "rb"))
label = ['anger', 'angry', 'disgust', 'fear', 'happiness', 'neutral', 'sad', 'surprise']

UPLOAD_DIRECTORY = './tmp/'

if not os.path.exists(UPLOAD_DIRECTORY):
    os.mkdir(UPLOAD_DIRECTORY)

app = Flask(__name__)


def audio_preprocessing(filename):
    xf, sr = librosa.load(UPLOAD_DIRECTORY + filename)
    mfcc_1 = librosa.feature.mfcc(y=xf, sr=16000, n_mfcc=5, n_fft=400, hop_length=160)
    mfcc_1 = scale(mfcc_1, axis=1)
    feature = np.mean(mfcc_1.T, axis=0)
    return [feature]


# 오디오 테스트 데이터 학습
def audio_test(x_test):
    result = model.predict(x_test)
    return result[0].tolist()


@app.route('/receive', methods=['POST'])
def form():
    """Get wav file"""
    file = request.files['file']
    if file.filename is not None:
        filename = secure_filename(filename=file.filename)
        file.save(os.path.join(UPLOAD_DIRECTORY, filename))
        x_test = audio_preprocessing(file.filename)
        predict_result = audio_test(x_test)
        return jsonify({'status': 'success', "result": label[predict_result]})
    else:
        return jsonify({'status': 'fail'})


@app.route('/', methods=['GET'])
def hello():
    """Render html"""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
