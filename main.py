from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.staticfiles import StaticFiles
from starlette.status import HTTP_401_UNAUTHORIZED

from core import scraper, extractor

users_db = {
    "admin": "EoIi9Kw57L5MESCjGcRbIB5RPabjlgSg",
    "a.rafiee": "4uQs9fq4OF7kGTH3wNrNtIw3lYJgITO9"
}

security = HTTPBasic()


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username in users_db:
        correct_password = users_db[credentials.username]
        if credentials.password == correct_password:
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
    return scraper.scrape(body['url'], body['selectors'])


@app.post("/extract")
async def extract(request: Request):
    body = await request.json()
    return extractor.extract(body['start_urls'], body['config'])

app.mount("/", StaticFiles(directory="static", html=True), name="static")
