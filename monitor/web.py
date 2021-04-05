from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

import datetime
import time

import threading

from monitor.monitor import stream

app = Flask(__name__)

@app.route('/')
def default(name=None):
  return render_template("index.html")

socketio = SocketIO(app)

def publish(packet):
  try:
    packet["timestamp"] = str(packet["timestamp"])
    socketio.emit("update", packet)
  except Exception as e:
    print("ERROR", str(e))

stream.subscribe(publish)

@socketio.on('connect')
def on_connect():
  print("client connected")

@socketio.on('disconnect')
def on_disconnect():
  print("client disconnected")
