FROM python:3.6-slim

EXPOSE 5031

RUN apt-get update
RUN apt-get -y install apt-transport-https ca-certificates curl gnupg2 software-properties-common
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"

RUN apt-get update
RUN apt-get -y install docker-ce

COPY ./app.py /app/app.py
COPY ./Pipfile* /app/

RUN pip install pipenv
RUN cd /app && pipenv lock --requirements > requirements.txt
RUN pip install -r /app/requirements.txt

CMD ["python", "/app/app.py"]
