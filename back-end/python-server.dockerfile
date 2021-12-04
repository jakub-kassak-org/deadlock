FROM        python:3.7-slim

LABEL       autor="Jakub Kaššák"

WORKDIR     /usr/src/app

COPY        ./requirements.txt .

RUN         pip install -r requirements.txt

COPY        . .

RUN         chmod u+x init.sh

ENTRYPOINT  [ "./init.sh" ]