FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN pip install python-dotenv


COPY run.sh run.sh
RUN chmod +x run.sh

CMD ["/bin/sh", "run.sh"]