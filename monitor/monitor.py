import serial
from serial import Serial
from monitor.protocol import parse

from threading import Thread

class SerialStream(Thread):
  def __init__(self):
    super().__init__()
    self.subscribers = []

    self.ser = Serial()
    self.ser.baudrate = 115200
    self.ser.bytesize = serial.EIGHTBITS
    self.ser.parity   = serial.PARITY_NONE
    self.ser.stopbits = serial.STOPBITS_ONE
    self.ser.xonxoff  = 0
    self.ser.rtscts   = 0
    self.ser.timeout  = 12
    self.ser.port     = "/dev/ttyUSB0"
    print("serial stream initialized")
  
  def subscribe(self, callback):
    self.subscribers.append(callback)

  def run(self):
    print("starting serial stream thread")
    previous = {}
    packet   = {}
    self.ser.close()
    self.ser.open()
    try:
      while True:
        line = self.ser.readline()
        line = line.decode("ascii").strip()
        name, value = parse(line)
        if name:
          try:
            change = round(value - previous[name], 4)
          except:
            change = None
          previous[name] = value
          packet[name]   = value
          if not change is None:
            packet[name + " change"] = change
  
        if line.startswith("!"):
          checksum_found = True
          for subscriber in self.subscribers[:]:
            try:
              print("notifyinbg subscriber")
              subscriber(packet)
            except:
              print("failed, removing subscriber")
              self.subscribers.remove(subscriber)
          packet = {}
    except:
      pass
    self.ser.close()

stream = SerialStream()
stream.start()
