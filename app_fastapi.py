from fastapi import FastAPI, Header, Cookie, Form, Request, requests, Body, Response, HTTPException
from fastapi.responses import HTMLResponse
from typing import List, Callable, Optional
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from pydantic import BaseModel
import uvicorn


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


@app.get('/index', tags=['Page'])
async def index(request: Request):
    return templates.TemplateResponse('template_fastapi/index.vue', context={'request': request})


@app.get('/dashboard', tags=['Page'])
async def dashboard(request: Request):
    return templates.TemplateResponse('template_fastapi/dashboard.vue', context={'request': request})


@app.get('/', summary='First Page')
@app.get('/login', tags=['Page'], summary='Login', description='Page Login', response_model=Login)
async def login(request: Request):
    return templates.TemplateResponse('template_fastapi/login.vue', context={'request': request})


@app.post('/login', tags=['Security'], response_model=Login)
async def login_post(formElements: Login):
    """
    POST LOGIN
    - **email**: your email here.
    - **password**: your password here.
    - **checkbox**: your remember
    """
    items = formElements.dict()
    return items


if __name__ == '__main__':
    uvicorn.run('app_fastapi:app', debug=True, port=8888)
