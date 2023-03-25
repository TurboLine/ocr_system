from dataclasses import dataclass, field
from typing import List

import psycopg2

from client.classes.picture import Picture
from client.scripts.connect_db import PG_CONNECT

SQL_SELECT_PICTURES =\
    "SELECT id, nickname, time_application, file_name, file_path FROM pictures;"
SQL_SELECT_PICTURE =\
    "SELECT id, nickname, time_application, file_name, file_path FROM pictures WHERE id = %s;"
SQL_SELECT_TEXTS =\
    "SELECT text_from_picture FROM texts_from_pictures WHERE id_picture = %s;"


@dataclass
class Pictures:
    pictures_list: List[Picture] = field(default_factory=list)

    @staticmethod
    def db_load_one():
        pic = None
        con = psycopg2.connect(**PG_CONNECT)
        try:
            cur = con.cursor()
            cur.execute(SQL_SELECT_PICTURES)
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

    def db_load_all(self):
        con = psycopg2.connect(**PG_CONNECT)
        try:
            cur = con.cursor()
            cur.execute(SQL_SELECT_PICTURES)
            db_answer = cur.fetchall()
            for pic_list in db_answer:
                cur.execute(SQL_SELECT_TEXTS, pic_list[0])
                text_list = cur.fetchall()
                self.pictures_list.append(
                    Picture(
                        id=pic_list[0],
                        nickname=pic_list[1],
                        time_application=pic_list[2],
                        file_name=pic_list[3],
                        file_path=pic_list[4],
                        text_list=text_list
                    )
                )
        except psycopg2.Error as error:
            print(error)
        finally:
            if con is not None:
                con.commit()
                con.close()

    def get_pictures(self):
        answer_list = []
        for pic in self.pictures_list:
            answer_list.append(pic.get_picture())
        return answer_list