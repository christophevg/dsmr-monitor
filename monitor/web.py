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

clients = []

def publish_stream():
  for packet in stream():
    if len(clients) == 0: return
    packet["timestamp"] = str(packet["timestamp"])
    packet["clients"] = len(clients)
    socketio.emit("update", packet)

@socketio.on('connect')
def on_connect():
  clients.append(request.sid)
  if len(clients) == 1:
    threading.Thread(target=publish_stream).start()

@socketio.on('disconnect')
def on_disconnect():
  clients.remove(request.sid)
