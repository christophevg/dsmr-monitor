import datetime
import re

from collections import namedtuple 

def parse_timestamp(format="%y%m%d%H%M%S"):
  def parse(value):
    return datetime.datetime.strptime(value, format)
  return parse

DSMRMessage = namedtuple("DSMRMessage",[ "pattern", "name", "parser" ])

protocol = {
  "0-0:1.0.0"  : DSMRMessage("\(([0-9]+)S\)",       "timestamp",   parse_timestamp() ),
  "1-0:1.8.1"  : DSMRMessage("\(([0-9\.]+)\*kWh\)", "in day",      float ),
  "1-0:1.8.2"  : DSMRMessage("\(([0-9\.]+)\*kWh\)", "in night",    float ),
  "1-0:2.8.1"  : DSMRMessage("\(([0-9\.]+)\*kWh\)", "out day",     float ),
  "1-0:2.8.2"  : DSMRMessage("\(([0-9\.]+)\*kWh\)", "out night",   float ),
  "0-0:96.14.0": DSMRMessage("\(([0-9]+)\)",        "tarif",       int),
  "1-0:1.7.0"  : DSMRMessage("\(([0-9\.]+)\*kW\)",  "in current",  float),
  "1-0:2.7.0"  : DSMRMessage("\(([0-9\.]+)\*kW\)",  "out current", float),
  "1-0:32.7.0" : DSMRMessage("\(([0-9\.]+)\*V\)",   "out phase 1", float),
  "1-0:52.7.0" : DSMRMessage("\(([0-9\.]+)\*V\)",   "out phase 2", float),
  "1-0:72.7.0" : DSMRMessage("\(([0-9\.]+)\*V\)",   "out phase 3", float),
  "0-1:24.2.3" : DSMRMessage("\([0-9]+S\)\(([0-9\.]+)\*m3\)", "gas", float)
}

regs = {
  header : re.compile("^" + header + message.pattern + "$") \
  for header, message in protocol.items()  
}

def parse(line):
  for header, message in protocol.items():
    if line.startswith(header):
      result = regs[header].search(line)
      if result:
        return message.name, result.group(1)
  return None, None

if __name__ == "__main__":
  # TODO move this to unit tests ;-)
  data = """
0-0:1.0.0(210405162433S)
1-0:1.8.1(002273.816*kWh)
1-0:1.8.2(003306.177*kWh)
1-0:2.8.1(002763.402*kWh)
1-0:2.8.2(001010.273*kWh)
  """

  for line in data.split("\n"):
    print(parse(line))
