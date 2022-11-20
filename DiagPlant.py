from ast import Return
from keras.models import load_model
import numpy as np
import cv2
import urllib
from flask import Flask,jsonify ,request
import base64
from PIL import Image
from io import BytesIO
import math
from flask_ngrok import run_with_ngrok
from pyngrok import ngrok
import json

app = Flask(__name__)
run_with_ngrok(app)
ngrok.set_auth_token('2EIz2ZMt4BiMBSB8lgtG7w3x3F8_E6SBYNTeFb1bhXqtwka')

model = load_model('/home/ubuntu/api/ApiDiagPLant/keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
classes = ['Mancha Preta', 'Saudável','Cancro cítrico','Greening']
descricoes = [
    "A mancha preta dos citros (CBS) é uma doença dos citros causada pelo fungo Phyllosticta citricarpa (anteriormente conhecido como Guignardia citricarpa). Este fungo afeta plantas cítricas em climas subtropicais, reduzindo tanto a quantidade quanto a qualidade dos frutos.",
    "",
    "O cancro cítrico, causado pela bactéria Xanthomonas citri subsp. citri, ocasiona lesões locais em folhas, frutos e ramos.",
    "O greening ou huanglongbing é uma doença causada pelas bactérias Candidatus Liberibacter spp, Candidatus Liberibacter africanus, Candidatus Liberibacter asiaticus e Candidatus Liberibacter americanus que afeta os citrus, deixando suas folhas amareladas e mosqueadas. "
]
tratamentos = [
    "Remoção dos frutos temporãos infectados antes do início da florada.",
    "",
    "Como não existe método curativo para a doença, a única forma de eliminar o cancro cítrico é por erradicação do material contaminado. No entanto, só a erradicação das árvores contaminadas não garante a eliminação da bactéria causadora do cancro cítrico.",
    "O controle do greening exige o plantio de mudas sadias, a eliminação das plantas doentes e o controle do psilídeo. A eliminação das plantas é obrigatória por lei. "
]
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
    porcentoIndexmaior = prediction[indexmaior]
    prediction[0][indexmaior] = 0
    indexsegundo = np.argmax(prediction)
    porcentoIndexsegundo = prediction[indexsegundo]
    
    retorno = {
        "PrimeiroDiagnostico": {
            "doenca":classes[indexmaior],
            "probabilidade":porcentoIndexmaior,
            "descricao":descricoes[indexmaior],
            "tratamento":tratamentos[indexmaior]
        },
        "SegundoDiagnostico": {
            "doenca":classes[indexsegundo],
            "probabilidade": porcentoIndexsegundo,
            "descricao": descricoes[indexsegundo],
            "tratamento":tratamentos[indexsegundo]
        }
    }
    print(retorno)
    return retorno

def predict(model, img):
    img_array = tf.keras.preprocessing.image.img_to_array(images[i].numpy())
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array)

    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = round(100 * (np.max(predictions[0])), 2)
    return predicted_class, confidence

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
    porcentoIndexmaior = prediction[0][indexmaior]
    prediction[0][indexmaior] = 0
    indexsegundo = np.argmax(prediction)
    porcentoIndexsegundo = prediction[0][indexsegundo]
    return jsonify({
        "PrimeiroDiagnostico": {
            "doenca":classes[indexmaior],
            "probabilidade": str(porcentoIndexmaior),
            "descricao":descricoes[indexmaior],
            "tratamento":tratamentos[indexmaior]
        },
        "SegundoDiagnostico": {
            "doenca":classes[indexsegundo],
            "probabilidade": str(porcentoIndexsegundo),
            "descricao": descricoes[indexsegundo],
            "tratamento":tratamentos[indexsegundo]
        }
    })




if __name__ == '__main__':
  app.run(port=1000)
