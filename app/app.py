import uvicorn
from fastapi import Depends, FastAPI
from routers import peoples
from internal import admin
from dependencies import get_token_header, get_query_token

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(
    admin.router,
    prefix='/admin',
    tags=['admin'],
    dependencies=[Depends(get_token_header)],
    responses={418: {'description': "failed"}}
)

app.include_router(
    peoples.router,
    prefix='/users',
    tags=['peoples'],
    dependencies=[Depends(get_token_header)],
    responses={404: {'description': 'Not found'}}
)


@app.get('/')
async def root():
    return {'message': 'Hello FastAPI'}


@app.get('/index', deprecated=True)
async def index():
    return {'message': 'Index'}


if __name__ == '__main__':
    uvicorn.run('app:app', port=8888, debug=True)
