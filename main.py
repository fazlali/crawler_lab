import json
import os.path

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import FileResponse
from starlette.responses import JSONResponse
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
    products = scraper.scrape(body['urls'], body['selectors'])
    return {'products': products}


@app.post("/extract")
async def extract(request: Request):
    body = await request.json()
    product_urls = extractor.extract(body['start_urls'], body['config'])
    return {'product_urls': product_urls}


@app.post("/websites/{domain}")
async def extract(request: Request, domain, username=Depends(authenticate_user)):
    body = await request.json()
    body['domain'] = domain
    if not os.path.exists(f'./db/{username}'):
        os.makedirs(f'./db/{username}')
        with open(f'/db/{username}/{domain}.json', 'w') as f:
            json.dump(body, f)

    return {'website': body}


@app.get("/websites/{domain}")
async def extract(request: Request, domain: str, username=Depends(authenticate_user)):
    if os.path.isfile(f'./db/{username}/{domain}.json'):
        with open(f'./db/{username}/{domain}.json', 'r') as f:
            return {
                'website': json.load(f)
            }
    return JSONResponse({'website': None}, status_code=404)


@app.get('/')
async def index(request: Request):
    return FileResponse('static/index.html')

