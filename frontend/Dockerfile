FROM node AS base

WORKDIR /app

COPY package*.json .
RUN npm install

COPY . .
RUN npm run build

FROM ubuntu/nginx

COPY --from=base /app/public/ /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/nginx.conf
