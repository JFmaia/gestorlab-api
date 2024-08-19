FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Define as variáveis de ambiente a partir de valores fixos
ENV DATABASE_PORT=5432
ENV POSTGRES_USER=gestorlab_user
ENV POSTGRES_PASSWORD=g3st0rL4b
ENV POSTGRES_DB=gestorlab_db_dev
ENV DATABASE_HOST=labens.dct.ufrn.br

ENV EMAIL_USER=admin@gmail.com
ENV PASSWORD_USER=admin1234@   

ENV JWT_SECRET=mVvrh7Q5iGAko2xH1-mrAWH0jeZCpMjAo4_BjdljDTH
ENV API_V1_STR=/gestorlab
ENV SECRET_KEY=nitvcsdojiqimkaz

COPY run.sh run.sh
RUN chmod +x run.sh

CMD ["/bin/sh", "run.sh"]