import easyocr

LANGUAGE = ['ru', 'en']


def select_text(file: bytes):
    reader = easyocr.Reader(LANGUAGE)
    result = reader.readtext(file)
    if result is not None and len(result) > 0:
        return [eval(str(val[0])) for val in result]
    else:
        return []
