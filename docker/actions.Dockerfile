FROM rasa/rasa-sdk:3.1.1

WORKDIR /app
USER root
COPY ./bot/actions /app/actions

RUN python3 -m pip install pymongo 
RUN python3 -m pip install "pymongo[srv]"
RUN python3 -m pip install python-dotenv

USER 1001