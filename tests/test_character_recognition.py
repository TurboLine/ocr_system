import requests
URL_1 = 'http://127.0.0.1:5000/character_recognition/api/v1.0/read_text'
PATH_TEST_FILE_1 = 'tests/test_pic_1.jpg'


def test_1():
    fp = open(PATH_TEST_FILE_1, 'rb')
    # помещаем объект файла в словарь
    # в качестве значения с ключом 'file'
    files = {'file': fp}
    # передаем созданный словарь аргументу `files`
    resp = requests.post(URL_1, files=files)
    fp.close()
    print(resp.text)


if __name__ == '__main__':
    test_1()
