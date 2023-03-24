CREATE DATABASE ocr_db;

CREATE TABLE pictures
(
    id                  BIGSERIAL       PRIMARY KEY,
    nickname            VARCHAR(255),
    time_application    TIMESTAMP,
    file_name           VARCHAR(255),
    file_url            VARCHAR(255)
);

CREATE TABLE texts_from_pictures
(
    id                  BIGSERIAL       PRIMARY KEY,
    id_pictures         BIGSERIAL       REFERENCES pictures ON DELETE CASCADE,
    text_from_pictures  NVARCHAR
);