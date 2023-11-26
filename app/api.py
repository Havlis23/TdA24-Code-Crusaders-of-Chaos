# app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def greet():
    return jsonify({'secret': 'The cake is a lie'})

if __name__ == '__main__':
    app.run(debug=True)
