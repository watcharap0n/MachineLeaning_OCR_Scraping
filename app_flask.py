from flask import Flask, jsonify, request
import os

app = Flask(__name__)

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


@app.route('/api/payload')
def api_payload():
    req = request.args.get('hello')
    if req:
        try:
            payload = [x[req] for x in payloads['peoples']]
            return jsonify({'message': payload})
        finally:
            return jsonify({'error': req})
    return jsonify({'message': payloads})


@app.route('/api/form', methods=['POST'])
def api_form():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    age = request.form['age']
    city = request.form['city']
    results = {
        'firstname': firstname,
        'lastname': lastname,
        'city': city,
        'age': age,
    }
    insert_data = payloads['peoples']
    insert_data.append(results)
    return jsonify({'message': payloads})


@app.route('/api/update/<int:id>', methods=['POST'])
def aip_update(id):
    change_data = request.get_json()
    payloads['peoples'][id] = change_data
    return jsonify(payloads)


@app.route('/api/delete/<int:id>')
def api_delete_id(id):
    del payloads['peoples'][id]
    return jsonify({'message': payloads})


@app.route('/api/delete_name/<string:name>')
def api_delete_name(name):
    for idx, fname in enumerate(payloads['peoples']):
        if fname['firstname'] == name:
            del payloads['peoples'][idx]
    return jsonify({'message': payloads})


@app.route('/post_data', methods=['POST'])
def post_data():
    data = request.get_json()
    return jsonify({'message': data})


@app.route('/api/form_file', methods=['POST'])
def api_form_file():
    file = request.files['image_file']
    uploads_dir = os.path.join(app.instance_path, 'image_upload')
    file.save(os.path.join(uploads_dir, file.filename))
    return jsonify({'message': 'success'})


if __name__ == '__main__':
    app.run(debug=True)
