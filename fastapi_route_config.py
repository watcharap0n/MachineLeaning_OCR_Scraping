from fastapi import FastAPI, Header, Cookie, Form, Request, requests, Body, Response, HTTPException
from fastapi.responses import HTMLResponse
from typing import List, Callable
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from pydantic import BaseModel
import uvicorn

payloads = {
    'peoples': [
        {
            'firstname': 'watcharapon',
            'lastname': 'weeraborirak',
            'age': '24',
            'city': 'bangkok'
        },
        {
            'firstname': 'somsak',
            'lastname': 'tamjai',
            'age': '22',
            'city': 'bangkok'
        },
        {
            'firstname': 'rakkana',
            'lastname': 'meejai',
            'age': '66',
            'city': 'outcast'
        },
    ]
}


class Item(BaseModel):
    name: str
    price: float


class ValidationError(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def customer_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {'error': exc.errors(), 'body': body.decode()}
                raise HTTPException(status_code=200, detail=detail)

        return customer_route_handler


app = FastAPI()
app.router.route_class = ValidationError
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


@app.post('/items')
async def base_model(item: Item):
    item_dict = item.dict()
    return {'message': item_dict}


@app.put('/items/{item_id}')
async def item_id(item_id: int, item: Item):
    return {'item_id': item_id, **item.dict()}


@app.get('/peoples')
async def fetch_movies(query: str = None):  # query param string
    payload = [p[query] for p in payloads['peoples']]
    return payload


@app.get('/member')
async def member(NewHeader: str = Header(...)):  # Header
    return {'message': f'It is Header your put {NewHeader}'}


@app.get('/member/token')
async def member_token(x_token: str = Cookie(None)):
    print(x_token)
    return {'message': f'success cookie {x_token}'}


@app.get('/api_body/{item_id}')  # dynamic route
async def api_body(item_id: str):
    return {'item_id': item_id}


@app.post('/payload_request')
async def payload_request(request: Request):
    return await request.json()


@app.post("/payload_json")
async def create_item(payload: dict = Body(...)):
    print(payload)
    return payload


@app.post('/form_data')
async def form_data(password: str = Form(...), username: str = Form(...)):
    return {'message': {'user': username, 'pwd': password}}


@app.post('/cookies')
async def cookies(response: Response):
    response.set_cookie(key='foo', value='value')
    return {'message': 'cookies darken'}


@app.get('/')
@app.get('/index')
async def index(request: Request):
    return templates.TemplateResponse('template_fastapi/login.vue', context={'request': request})


if __name__ == '__main__':
    uvicorn.run('app_fastapi:app', debug=True, port=8080)
