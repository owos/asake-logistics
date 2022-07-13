FROM rasa/rasa:3.1.0-full

WORKDIR /app
USER root
COPY ./bot /app

# Importante treinar o modelo dentro do container!
RUN python3 -m pip install python-dotenv

RUN rasa train 

USER 1001 