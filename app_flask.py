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
            'firstname': 'thiphaporn',
            'lastname': 'raktuam',
            'age': '22',
            'city': 'bangkok'
        },
        {
            'firstname': 'prayut',
            'lastname': 'chanocha',
            'age': '66',
            'city': 'outcast'
        },
    ]
}


@app.route('/api/param')
def api_param():
    req = request.args.get('data')
    if req:
        print(req)
        return jsonify({'message': payload[req]})
    return jsonify({'message': payload})


if __name__ == '__main__':
    app.run(debug=True, port=5050)
