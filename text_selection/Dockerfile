FROM python:3.10.6

WORKDIR /app
#EXPOSE 5000
COPY . /app
RUN pip install -r /app/requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 5000

CMD ["python3", "main.py"]