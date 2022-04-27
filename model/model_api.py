from fastapi import FastAPI, File, UploadFile
from typing import List
import uvicorn
import joblib, os
import numpy as np
import librosa
from sklearn.preprocessing import scale
import warnings

warnings.filterwarnings("ignore")

# Models
print(os.getcwd())
model_lgbm = open("model/saved_model/model_lgbm.pkl", "rb")
model = joblib.load(model_lgbm)

# label_info
label = ['anger', 'angry', 'disgust', 'fear', 'happiness', 'neutral', 'sad', 'surprise']

# init app
app = FastAPI()


# ---- 사용자 함수----------------------------------------------------------------------------

# 오디오 데이터 전처리
def audio_preprocessing(UPLOAD_DIRECTORY, filename):
    xf, sr = librosa.load(UPLOAD_DIRECTORY + '/' + filename)
    mfcc_1 = librosa.feature.mfcc(y=xf, sr=16000, n_mfcc=5, n_fft=400, hop_length=160)
    mfcc_1 = scale(mfcc_1, axis=1)
    feature = np.mean(mfcc_1.T, axis=0)
    return [feature]


# 오디오 테스트 데이터 학습
def audio_test(x_test):
    result = model.predict(x_test)
    return result[0].tolist()


# 영화 추천

# ---- API ------------------------------------------------------------------------------------

@app.post('/uploadfiles')
async def create_upload_files(files: List[UploadFile] = File(...)):
    UPLOAD_DIRECTORY = "./backend/tmp/"
    for file in files:
        contents = await file.read()
        with open(os.path.join(UPLOAD_DIRECTORY, file.filename), "wb") as fp:
            fp.write(contents)
        print(file.filename)

    # 오디오 테스트 데이터 전처리
    x_test = audio_preprocessing(UPLOAD_DIRECTORY, file.filename)

    # 오디오 데이터 테스트
    predict_result = audio_test(x_test)

    return {"filenames": [file.filename for file in files],
            "predict_result": label[predict_result]}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8080)
