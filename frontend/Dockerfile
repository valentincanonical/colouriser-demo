FROM node AS base

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

###
FROM ubuntu/nginx

COPY --from=base /app/public/ /usr/share/nginx/html/
COPY ./nginx.conf /etc/nginx/templates/default.conf.template

ENV DOLLAR='$'
ENV PORT='3000'
ENV BACKEND_HOSTNAME='127.0.0.1'
ENV BACKEND_PORT='8080'
