FROM node:14

WORKDIR /var/www
COPY ./web /var/www

RUN npm install
ENTRYPOINT ["node", "server.js"]