from fastapi import FastAPI, Header, Cookie, Form, Request, requests, Body
from fastapi.templating import Jinja2Templates
import uvicorn
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory='templates/')


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


data_query = {
    'titanic': 'jack',
    'tenet': 'star',
    'hello': 'world',
    'world': 'people'
}


@app.get('/movies')
async def fetch_movies(query: str = None):  # query param string
    return {'message': data_query[query]}


@app.get('/member')
async def member(x_user: str = Header(...)):  # Header
    return {'message': f'It is Header your put {x_user}'}


@app.get('/member/token')
async def member_token(x_token: str = Cookie(None)):
    print(x_token)
    return {'message': f'success cookie {x_token}'}


@app.get('/api_body/{item_id}')  # dynamic route
async def api_body(item_id: str):
    return {'item_id': item_id}


@app.post('/payload_request')
async def payload_request(r: Request):
    return await r.json()


@app.post("/payload_json")
async def create_item(payload: dict = Body(...)):
    print(payload)
    return payload


@app.get('/form')
def form(r: Request):
    return templates.TemplateResponse('form.html', context={'request': r})


if __name__ == '__main__':
    uvicorn.run('app_fastapi:app', debug=True, port=8080)
