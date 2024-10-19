from flask import Flask, render_template, request, jsonify
import threading
import requests
import torch
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/get', methods=['GET', 'POST'])
def chat():
    msg = request.form["msg"]
    input = msg
    return get_Chat_response(input)

def get_Chat_response(text):
    return ("Modify this function to return the response from your model.")

if __name__ == '__main__':
    app.run()