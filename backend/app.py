from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/', methods=['GET'])
def get_data_route():
    return jsonify({'data': 'Hello, World!'})

if __name__ == '__main__':
    app.run(debug=True)