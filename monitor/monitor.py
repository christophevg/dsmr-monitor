import serial
from serial import Serial
from monitor.protocol import parse

from threading import Thread


class ReadLine:
  '''
  This wrapper avoids the native readline method to hog the CPU.
  credits: https://github.com/pyserial/pyserial/issues/216#issuecomment-369414522
  On a RPI this dropped the CPU usage from ±20% to about 1% :-)
  '''
  def __init__(self, s):
    self.buf = bytearray()
    self.s = s
  
  def readline(self):
    i = self.buf.find(b"\n")
    if i >= 0:
      r = self.buf[:i+1]
      self.buf = self.buf[i+1:]
      return r
    while True:
      i = max(1, min(2048, self.s.in_waiting))
      data = self.s.read(i)
      i = data.find(b"\n")
      if i >= 0:
        r = self.buf + data[:i+1]
        self.buf[0:] = data[i+1:]
        return r
      else:
        self.buf.extend(data)
  
  def open(self):
    self.s.open()
  
  def close(self):
    self.s.close()

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
    self.ser = ReadLine(self.ser)
    print("serial stream initialized")
  
  def subscribe(self, callback):
    self.subscribers.append(callback)

  def run(self):
    previous = {}
    packet   = {}
    self.ser.close()
    self.ser.open()
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
            subscriber(packet)
          except:
            print("failed, removing subscriber")
            self.subscribers.remove(subscriber)
        packet = {}
      
    self.ser.close()

stream = SerialStream()
stream.start()
