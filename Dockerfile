FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN pip install python-dotenv

COPY .env .env
ENV PYTHONUNBUFFERED=1  
RUN bash -c "source .env"

COPY run.sh run.sh
RUN chmod +x run.sh

CMD ["/bin/sh", "run.sh"]