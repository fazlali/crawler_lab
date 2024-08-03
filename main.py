import json

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import FileResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from core import scraper, extractor

security = HTTPBasic()


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    with open('./users.json', 'r') as f:
        users = json.load(f)
    if credentials.username in users:
        password = users[credentials.username]
        if credentials.password == password:
            return credentials.username

    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


app = FastAPI(dependencies=[Depends(authenticate_user)])


@app.post("/scrape")
async def scrape(request: Request):
    body = await request.json()
    return scraper.scrape([body['url']], body['selectors'])[0]


@app.post("/extract")
async def extract(request: Request):
    body = await request.json()
    return extractor.extract(body['start_urls'], body['config'])


@app.get('/')
async def index(request: Request):
    return FileResponse('static/index.html')

