import os

import easyocr

LANGUAGE = ['ru', 'en']


def select_text(path_file):
    reader = easyocr.Reader(LANGUAGE)
    result = reader.readtext(path_file)
    os.remove(path_file)
    if result is not None and len(result) > 0:
        return [eval(str(val[0])) for val in result]
    else:
        return 'Not found'
