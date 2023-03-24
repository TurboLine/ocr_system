import os

import easyocr

LANGUAGE = ['ru', 'en']


def select_text(path_file):
    reader = easyocr.Reader(LANGUAGE)
    result = reader.readtext(path_file, detail=0, paragraph=True)
    os.remove(path_file)
    if result is not None and len(result) > 0:
        return result[0]
    else:
        return 'Not found trext'
