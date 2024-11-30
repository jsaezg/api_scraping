import os
from flask import Flask, request, jsonify
from scrapping_driver.test_url import get_web

app = Flask(__name__)



@app.route('/')
def home():
    return "Hello, Flask is running!"

@app.route('/get_web', methods=['GET'])
def get_web_endpoint():
    url = request.args.get('url', 'https://www.emol.com')  # Leer URL del parámetro de consulta
    html_response = get_web(url)
    return html_response

@app.route('/test')
def test():
    return "This is a test endpoint!"



port = int(os.environ.get("PORT", 5200)) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)