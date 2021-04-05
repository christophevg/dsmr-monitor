import serial
from monitor.protocol import parse

ser = serial.Serial()
 
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS
ser.parity   = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.xonxoff  = 0
ser.rtscts   = 0
ser.timeout  = 12
ser.port     = "/dev/ttyUSB0"

def stream():
  previous = {}
  packet   = {}
  try:
    ser.close()
    ser.open()
    while True:
      line = ser.readline()
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
        yield packet
        packet = {}
  except KeyboardInterrupt:
    pass

  ser.close()
