FROM python:3.7-slim

#RUN python -m pip uninstall pip

#RUN python -m ensurepip

#RUN python -m pip install -U pip

#RUN python -m pip install --default-timeout=200 future

RUN python -m pip install tensorflow==2.7.0

RUN python -m pip install rasa

WORKDIR /app
ENV HOME=/app
COPY . .

RUN rasa train nlu

# set the user to run, don't run root
USER 10001

# set the entry point for interactive shells
ENTRYPOINT ["rasa"]

# command to run when container is called to run
CMD ["run", "--enable-api", "--port", "8080"]