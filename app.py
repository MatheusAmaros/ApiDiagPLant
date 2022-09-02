from ast import Return
from keras.models import load_model
import numpy as np
import cv2
import urllib
from flask import Flask, request
import base64
from PIL import Image
from io import BytesIO
import math

app = Flask('DiagPlant')
model = load_model('models/keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
classes = ['Black Spot','Cancro', 'Saudável','greening']

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello, World!'

@app.route('/teste', methods=["GET", "POST"])
#img = cv2.imread('models/black.jpg')
def teste():
    
    path = {'path': request.json['path']}
    
    url = path.get('path')
    url_response = urllib.request.urlopen(url)
    img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
    img = cv2.imdecode(img_array, -1)

        
    imgS = cv2.resize(img, (224, 224))
    image_array = np.asarray(imgS)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    indexmaior = np.argmax(prediction)
    prediction[0][indexmaior] = 0
    indexsegundo = np.argmax(prediction)
    
    retorno = {
        "PrimeiroDiagnostico": classes[indexmaior],
        "SegundoDiagnostico": classes[indexsegundo]
    }
    print(retorno)
    return retorno

@app.route('/imagem', methods=["GET", "POST"])
#img = cv2.imread('models/black.jpg')
def uploadImagem():
    imagem = request.files['imagem'] 
    
    img_array = np.array(bytearray(imagem.read()), dtype=np.uint8)
    img = cv2.imdecode(img_array, -1)

        
    imgS = cv2.resize(img, (224, 224))
    image_array = np.asarray(imgS)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    indexmaior = np.argmax(prediction)
    prediction[0][indexmaior] = 0
    indexsegundo = np.argmax(prediction)
    
    retorno = {
        "PrimeiroDiagnostico": classes[indexmaior],
        "SegundoDiagnostico": classes[indexsegundo]
    }
    print(retorno)
    return retorno


@app.route('/base64', methods=["GET", "POST"])
#img = cv2.imread('models/black.jpg')
def uploadImagemBase64():
    imagemBase64 = "/9j/4QCCRXhpZgAATU0AKgAAAAgABQEaAAUAAAABAAAASgEbAAUAAAABAAAAUgEoAAMAAAABAAIAAAITAAMAAAABAAEAAIKYAAIAAAAfAAAAWgAAAAAAAABIAAAAAQAAAEgAAAABKGMpIFJwcm9uZ2phaSB8IERyZWFtc3RpbWUuY29tAAD/7QBGUGhvdG9zaG9wIDMuMAA4QklNBAQAAAAAACocAnQAHihjKSBScHJvbmdqYWkgfCBEcmVhbXN0aW1lLmNvbRwCAAACAAT/4Qx1aHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLwA8P3hwYWNrZXQgYmVnaW49J++7vycgaWQ9J1c1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCc/Pgo8eDp4bXBtZXRhIHhtbG5zOng9J2Fkb2JlOm5zOm1ldGEvJyB4OnhtcHRrPSdJbWFnZTo6RXhpZlRvb2wgMTAuODAnPgo8cmRmOlJERiB4bWxuczpyZGY9J2h0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMnPgoKIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PScnCiAgeG1sbnM6cGx1cz0naHR0cDovL25zLnVzZXBsdXMub3JnL2xkZi94bXAvMS4wLyc+CiAgPHBsdXM6TGljZW5zb3I+CiAgIDxyZGY6U2VxPgogICAgPHJkZjpsaSByZGY6cGFyc2VUeXBlPSdSZXNvdXJjZSc+CiAgICAgPHBsdXM6TGljZW5zb3JVUkw+aHR0cHM6Ly93d3cuZHJlYW1zdGltZS5jb208L3BsdXM6TGljZW5zb3JVUkw+CiAgICA8L3JkZjpsaT4KICAgPC9yZGY6U2VxPgogIDwvcGx1czpMaWNlbnNvcj4KIDwvcmRmOkRlc2NyaXB0aW9uPgoKIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PScnCiAgeG1sbnM6eG1wUmlnaHRzPSd"
    imagemBase64 = imagemBase64.ljust((int)(math.ceil(len(imagemBase64) / 4)) * 4, '=')
    imagem = base64.b64decode(imagemBase64)
    imagem = base64.decodebytes(imagem)
    imagem = Image.open(BytesIO(imagem))
    
    img_array = np.array(bytearray(imagem.read()), dtype=np.uint8)
    img = cv2.imdecode(img_array, -1)
    
    imgS = cv2.resize(img, (224, 224))
    image_array = np.asarray(imgS)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    indexmaior = np.argmax(prediction)
    prediction[0][indexmaior] = 0
    indexsegundo = np.argmax(prediction)
    
    retorno = {
        "PrimeiroDiagnostico": classes[indexmaior],
        "SegundoDiagnostico": classes[indexsegundo]
    }
    print(retorno)
    return retorno

    


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=4000)