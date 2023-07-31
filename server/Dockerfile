FROM python:3.11.2-buster

WORKDIR /server

COPY ./server .

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

CMD ["python", "main.py"]
