from fastapi import HTTPException, Header


async def get_token_header(x_token: str = Header(...)):
    if x_token != 'secret-token':
        raise HTTPException(status_code=400, detail='X-Token Header invalid')


async def get_query_token(token: str = None):
    if token != 'watcharapon':
        raise HTTPException(status_code=400, detail='No token provided')
