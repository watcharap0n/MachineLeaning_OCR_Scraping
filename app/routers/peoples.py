from fastapi import APIRouter, HTTPException

router = APIRouter()

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


@router.get('/')
async def read_users():
    return payloads


@router.get('/{user_id}')
async def read_user(user_id: str):
    lst = []
    for val in payloads['peoples']:
        if user_id not in val:
            raise HTTPException(status_code=404, detail='User not found')
        lst.append(val[user_id])
    return {'message': lst}

