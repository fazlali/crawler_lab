FROM node:lts-alpine AS build-panel-stage
WORKDIR /app
COPY ./panel/package.json ./panel/package-lock.json ./
RUN npm i
COPY ./panel .
RUN npm run build

FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
COPY --from=build-panel-stage /app/dist /app/static
#VOLUME /app/db
EXPOSE 80

CMD python3 -m gunicorn main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:80 --workers ${SERVER_WORKERS:-1}
