#!/usr/bin/env python3
import os

from flask import Flask, request, flash, redirect, jsonify

from scripts.ocr import select_text

LANGUAGES = ['ru', 'en']
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = '.'
NAME_TEMP_PIC = 'temp_pic'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/text_selection/api/v1.0/detect', methods=['POST'])
def detect_text():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], NAME_TEMP_PIC))
        answer = select_text(os.path.join(app.config['UPLOAD_FOLDER'], NAME_TEMP_PIC))
        return jsonify({"text": answer})


if __name__ == '__main__':
    app.run(debug=True)
