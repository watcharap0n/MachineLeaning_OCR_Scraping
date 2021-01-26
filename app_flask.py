from flask import Flask, jsonify

app = Flask(__name__)





if __name__ == '__main__':
    app.run(debug=True, port=5050)
