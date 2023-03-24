import os
from datetime import datetime

from flask import Flask, request, flash, redirect, jsonify, abort
from werkzeug.utils import secure_filename

from client.classes.picture import Picture

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
    if not 'nickname' in request.json and type(request.json['nickname'] is str):
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
            file_url=os.path.join(app.config['UPLOAD_FOLDER'], filename),
            text_list=[],
        )
        return jsonify()


@app.route('/client/api/v1.0/get_texts', methods=['GET'])
def get_texts():
    """
    Метод GET /get_texts получает из бд тексты из выбранной
    картинки. В БД должна записаться информация: пользователь
    (Авторизация не подразумевается, присылать вместе с запросом),
    время обращения, имя файла и выделенные тексты (учтите,
    на картинке может быть больше одного текста), картинки можно
    хранить на диске, тогда в бд должен лежать путь до картинки.
    """
    pass


