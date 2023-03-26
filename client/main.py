import os
from datetime import datetime

from flask import Flask, request, flash, redirect, jsonify, abort
from werkzeug.utils import secure_filename

from classes.picture import Picture
from classes.pictures import Pictures

LANGUAGES = ['ru', 'en']
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = '.'
NAME_TEMP_PIC = 'temp_pic'

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/client/api/v1.0/recognize', methods=['POST'])
def recognize():
    """
    Метод POST /recognize анализирует изображение и записывает
    результаты в БД. Процесс выглядит так: получаем картинку,
    достаем оттуда координаты текстбоксов с помощью сервиса
    выделения текста, обрезаем текстбоксы, обрезанные текстбоксы
    отправляем на сервис распознавания, получаем ответ и
    записываем в бд.
    """
    if not request.json:
        abort(400)
    if 'nickname' not in request.json and type(request.json['nickname'] is not str):
        abort(400)
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        pic = Picture(
            nickname=request.json['nickname'],
            time_application=datetime.now(),
            file_name=filename,
            file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        )
        pic.get_text_selection()
        pic.get_text()
        id_pic = pic.db_save()
        return jsonify({'id_picture': id_pic})


@app.route('/client/api/v1.0/get_texts', methods=['GET'])
def get_texts():
    """
    Метод GET /get_texts получает из бд тексты из выбранной
    картинки.
    """
    pictures = Pictures()
    pictures.db_load_all()
    answer_json = pictures.get_pictures()
    return jsonify(answer_json)


@app.route('/client/api/v1.0/get_texts/<int:pic_id>', methods=['GET'])
def get_task(pic_id):
    pic = Picture.db_load(pic_id)
    if pic is None:
        abort(404)
    return jsonify(pic.get_picture())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
