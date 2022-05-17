from flask import Flask, render_template, request, redirect
from fer import FER
import cv2

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        return render_template("result.html", angry=30, sad=10, happy= 30, neutral=0,surprise=10,fear=10, disgust =0)
            #str(face_recognithion(file))
    else:
        return render_template("index.html")


@app.route('/about')
def about():
    return render_template("index.html")


def face_recognithion(file):
    img = cv2.imread(file.filename)
    emo_detector = FER(mtcnn=True)
    ready = emo_detector.detect_emotions(img)
    return ready

if __name__ == "__main__":
    app.run(debug=True)





