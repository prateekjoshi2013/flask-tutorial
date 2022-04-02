from flask import Flask,jsonify

app=Flask(__name__)

@app.get("/")
def index():
    return "hello world"

@app.get("/hello")
def say_index():
    return jsonify({'message' :"hello world"})

