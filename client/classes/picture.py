import io
from datetime import datetime
from dataclasses import dataclass, field
from os import environ
from typing import Optional, List

import psycopg2
import requests
from PIL import Image

from scripts.connect_db import PG_CONNECT

SQL_INSERT_PICTURE = \
    "INSERT INTO pictures (nickname, time_application, file_name, file_path) VALUES (%s, %s, %s, %s) RETURNING id;"
SQL_INSERT_TEXT = \
    "INSERT INTO pictures (id_picture, text_from_picture) VALUES (%s, %s);"
SQL_SELECT_PICTURE =\
    "SELECT id, nickname, time_application, file_name, file_path FROM pictures WHERE id = %s;"
SQL_SELECT_TEXTS =\
    "SELECT text_from_picture FROM texts_from_pictures WHERE id_picture = %s;"


@dataclass
class Picture:
    nickname: str
    time_application: datetime
    file_name: str
    file_path: str
    id: Optional[int] = None
    text_selection_list: List[list] = field(default_factory=list)
    text_list: List[str] = field(default_factory=list)

    @staticmethod
    def db_load():
        pic = None
        con = psycopg2.connect(**PG_CONNECT)
        try:
            cur = con.cursor()
            cur.execute(SQL_SELECT_PICTURE)
            db_answer = cur.fetchone()
            for pic_list in db_answer:
                cur.execute(SQL_SELECT_TEXTS, pic_list[0])
                text_list = cur.fetchall()
                pic = Picture(
                    id=pic_list[0],
                    nickname=pic_list[1],
                    time_application=pic_list[2],
                    file_name=pic_list[3],
                    file_path=pic_list[4],
                    text_list=text_list
                )
        except psycopg2.Error as error:
            print(error)
        finally:
            if con is not None:
                con.commit()
                con.close()
        return pic

    def get_data_for_db_table_pictures(self):
        return (
            self.nickname,
            self.time_application,
            self.file_name,
            self.file_path
        )

    def get_text_selection(self):
        fp = open(self.file_path, 'rb')
        files = {'file': fp}
        r = requests.post(environ.get("URL_TEXT_SELECTION"), files=files)
        if r.ok:
            r_dict = r.json()
            if r_dict.get("code") == 200:
                answer = r_dict.get("data")
                if 'text_boxes' in answer:
                    self.text_selection_list = answer.get('text_boxes')
                    return self.text_selection_list

    def get_text(self):
        if self.text_selection_list is not None and len(self.text_selection_list) > 0:
            for text_box in self.text_selection_list:
                img = Image.open(self.file_path, mode='r')
                img_crop = img.crop((text_box[0][0], text_box[0][1], text_box[2][0], text_box[2][1]))
                img_crop_byte = io.BytesIO()
                img_crop.save(img_crop_byte)
                r = requests.post(environ.get('URL_CHARACTER_RECOGNITION'), files=img_crop_byte.getvalue())
                if r.ok:
                    r_dict = r.json()
                    if r_dict.get("code") == 200:
                        answer = r_dict.get("data")
                        if 'text' in answer:
                            self.text_selection_list = answer.get('text')
                            return self.text_list

    def db_save(self):
        con = psycopg2.connect(**PG_CONNECT)
        try:
            cur = con.cursor()
            cur.execute(SQL_INSERT_PICTURE, self.get_data_for_db_table_pictures())
            self.id = cur.fetchone()[0]
            for text in self.text_list:
                cur.execute(SQL_INSERT_TEXT, (self.id, text))
        except psycopg2.Error as error:
            print(error)
        finally:
            if con is not None:
                con.commit()
                con.close()
        return self.id

    def get_picture(self):
        return {
            "id": self.id,
            "nickname": self.nickname,
            "time_application": self.time_application,
            "file_name": self.file_name,
            "text_list": self.text_list
        }
