import os

from flask import Flask, render_template, request, redirect, url_for, flash
from fer import FER
import cv2
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './static/upload/'
ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '' :
            flash("Файл не выбран!")
            redirect(request.url)
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            url_pict = url_for('static', filename='upload/' + filename)
            result = face_recognithion(file)
        return render_template("result.html", angry=result[0]['emotions']['angry']*100, sad=result[0]['emotions']['sad']*100, happy= result[0]['emotions']['happy']*100, neutral=result[0]['emotions']['neutral']*100, surprise=result[0]['emotions']['surprise']*100, fear=result[0]['emotions']['fear']*100, disgust=result[0]['emotions']['disgust']*100, pict=url_pict)
    else:
        return render_template("index.html")


@app.route('/about')
def about():
    return render_template("index.html")


def face_recognithion(file):
    img = cv2.imread(app.config['UPLOAD_FOLDER'] + file.filename)
    emo_detector = FER(mtcnn=True)
    ready = emo_detector.detect_emotions(img)
    return ready

if __name__ == "__main__":
    app.run(debug=True)





