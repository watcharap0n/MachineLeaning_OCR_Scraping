from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/movies')
def movies():
    return jsonify({'message': [{'movies': 'TENET', 'fov': 'titanic'}]})


if __name__ == '__main__':
    app.run(debug=True, port=5050)
