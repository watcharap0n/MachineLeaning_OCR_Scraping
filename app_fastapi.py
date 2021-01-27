from fastapi import FastAPI, Header, Cookie, Form, Request, requests, Body, Response, HTTPException
from fastapi.responses import HTMLResponse
from typing import List, Callable, Optional
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


class Login(BaseModel):
    username: str
    password: str
    checkbox: list


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


@app.get('/')
@app.get('/index')
async def index(request: Request):
    return templates.TemplateResponse('template_fastapi/index.vue', context={'request': request})


@app.get('/login')
async def login(request: Request):
    return templates.TemplateResponse('template_fastapi/login.vue', context={'request': request})


@app.post('/login')
async def login_post(formElements: Login):
    items = formElements.dict()
    return items


@app.get('/dashboard')
async def dashboard(request: Request):
    return templates.TemplateResponse('template_fastapi/dashboard.vue', context={'request': request})


if __name__ == '__main__':
    uvicorn.run('app_fastapi:app', debug=True, port=8080)
