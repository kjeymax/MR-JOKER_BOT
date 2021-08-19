FROM python:3.9.1-buster

WORKDIR /root/mrjoker

COPY . .

RUN pip install -U -r requirements.txt

CMD ["python3","-m","mrjoker"]
