from fastapi import FastAPI, Header, Cookie, Form, Request, requests, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

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


@app.get('/index')
def index(request: Request):
    return templates.TemplateResponse('template_fastapi/index.html', context={'request': request})


if __name__ == '__main__':
    uvicorn.run('app_fastapi:app', debug=True, port=8080)
