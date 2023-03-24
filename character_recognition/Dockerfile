FROM python:3.10.6

WORKDIR /app
EXPOSE 5000
COPY . /app
RUN pip install -r /app/requirements.txt

CMD ["python3", "main.py"]