import json
import os.path

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.status import HTTP_401_UNAUTHORIZED

from core import scraper, extractor

security = HTTPBasic()


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    with open('./db/users.json', 'r') as f:
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"]
)

@app.post("/api/scrape")
async def scrape(request: Request):
    body = await request.json()
    products = scraper.scrape(body['urls'], body['selectors'])
    return {'products': products}


@app.post("/api/extract")
async def extract(request: Request):
    body = await request.json()
    product_urls = extractor.extract(body['start_urls'], body['config'])
    return {'product_urls': product_urls}


@app.get("/api/websites")
async def extract(request: Request, username=Depends(authenticate_user)):
    if os.path.exists(f'./db/{username}'):
        websites = [
            file[:-5]
            for file in os.listdir(f'./db/{username}')
            if os.path.isfile(f'./db/{username}/{file}') and file.endswith('.json')
        ]
    else:
        websites = []

    return {'websites': websites}


@app.post("/api/websites/{domain}")
async def save_website(request: Request, domain: str, username=Depends(authenticate_user)):
    body = await request.json()
    body['domain'] = domain
    if not os.path.exists(f'./db/{username}'):
        os.makedirs(f'./db/{username}')

    with open(f'./db/{username}/{domain}.json', 'w') as f:
        json.dump(body, f)

    return {'website': body}


@app.get("/api/websites/{domain}")
async def get_website(request: Request, domain: str, username=Depends(authenticate_user)):
    if os.path.isfile(f'./db/{username}/{domain}.json'):
        with open(f'./db/{username}/{domain}.json', 'r') as f:
            return {
                'website': json.load(f)
            }
    return JSONResponse({'website': None}, status_code=404)

app.mount('/', StaticFiles(directory='static', html=True), name='static')


@app.exception_handler(404)
async def fallback_404(request: Request, exc):
    return FileResponse('static/index.html')
