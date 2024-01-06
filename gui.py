import socket
import threading
from flask import Flask, render_template, jsonify
from server import start_server, get_temperature, get_humidity, get_last_humidity

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/humidity', methods=['GET'])
def humidity():
    data = get_humidity()
    data.to_html('templates/humidity.html', index=False)
    return render_template('humidity.html')
   
@app.route('/gethumidity', methods=['GET'])
def get_last_humidity1():
    data = get_last_humidity()
    data.to_html('templates/last_humidity.html', index=False)
    return render_template('last_humidity.html')
   
@app.route('/temperature', methods=['GET'])
def temperature():
    # Sample data to return in response to a GET request
    data = get_temperature()
    data.to_html('templates/temperature.html', index=False)
    return render_template('temperature.html')
if __name__ == "__main__":


    
    # Run the Flask app on port 8080
    app.run(host="localhost", debug=False, port=8081)
