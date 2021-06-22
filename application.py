from flask import Flask, flash, request, redirect, url_for, render_template
import os
import cv2
from werkzeug.utils import secure_filename

application = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

application.secret_key = "secret key"
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route('/')
def home():
    return render_template('index.html')


@application.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
        print(filename)
        image = cv2.imread("./static/uploads/" + filename)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        thresh, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        name = './static/changed/' + filename
        cv2.imwrite(name, binary)
        flash('Image after successful uploading and being binarized!!')
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


@application.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='changed/' + filename), code=301)


if __name__ == "__main__":
    application.run()
