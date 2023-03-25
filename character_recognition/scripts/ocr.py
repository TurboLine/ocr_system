import easyocr

LANGUAGE = ['ru', 'en']


def select_text(file: bytes):
    reader = easyocr.Reader(LANGUAGE)
    result = reader.readtext(file, detail=0, paragraph=True)
    if result is not None and len(result) > 0:
        return result[0]
    else:
        return 'Not found text'
