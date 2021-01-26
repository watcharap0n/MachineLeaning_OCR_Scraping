from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

payload = {
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




if __name__ == '__main__':
    app.run(debug=True, port=5050)
