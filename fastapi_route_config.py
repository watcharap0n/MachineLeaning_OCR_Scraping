from fastapi import FastAPI, Header, Cookie, Form, Request, requests, Body, Response, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.testclient import TestClient
from typing import List, Callable
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from starlette.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import time

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
client = TestClient(app)


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = '{}'.format(str(round(process_time, 4)))
    return response


@app.middleware('http')
async def add_process_name(request: Request, call_next):
    response = await call_next(request)
    response.headers['X-Owner-Server'] = 'Kane'
    return response


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
async def member(item: Item, X_Item_ID: str = Header(...)):  # Header
    if X_Item_ID != 'member':
        raise HTTPException(status_code=400, detail="X-Item-ID header invalid")
    return JSONResponse(content={item.name: 'kane', item.price: 123.33})


@app.get('/member/token')
async def member_token(x_token: str = Cookie(None)):
    print(x_token)
    return {'message': f'success cookie {x_token}'}


@app.get('/api_body/{item_id}')  # dynamic route
async def api_body(item_id: str):
    return {'item_id': item_id}


@app.post('/payload_request', response_model=Item, status_code=status.HTTP_201_CREATED)
async def payload_request(item: Item):
    return item


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
@app.get('/index', tags=['dashboard'])
async def index(request: Request):
    return templates.TemplateResponse('template_fastapi/login.vue', context={'request': request})


@app.get("/func_element", response_model=Item, tags=["Description"], deprecated=True)
async def func_element(item: Item):
    """
      Get Data Element:
      - **name**: my_name
      - **price**: price
      """
    return item


@app.post("/func_item", response_model=Item, tags=["Description"], summary="Create an item",
          description="Create an item with all the , name, description, price, tax and a set of unique tags")
async def fuc_item(item: Item):
    update_item = item.dict()
    update_item['name'] = 'kane_ja'
    return update_item


@app.post('/json_response', response_model=Item, tags=['Description'])
async def json_response(item: Item):
    """
    Return JsonResponse
    - **Item**: name
    - **status**: 201
    """
    return JSONResponse(content={item.name: 'kaneeang'}, status_code=201)


if __name__ == '__main__':
    uvicorn.run('fastapi_route_config:app', debug=True, port=8080)
