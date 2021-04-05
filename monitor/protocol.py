import datetime
import re

from collections import namedtuple 

def parse_timestamp(format="%y%m%d%H%M%S"):
  def parse(value):
    return datetime.datetime.strptime(value, format)
  return parse

DSMRMessage = namedtuple("DSMRMessage",[ "regexp", "name", "parser" ])

protocol = {
  "0-0:1.0.0"  : DSMRMessage("\(([0-9]+)S\)",       "timestamp", parse_timestamp() ),
  "1-0:1.8.1"  : DSMRMessage("\(([0-9\.]+)\*kWh\)", "in day",    float ),
  "1-0:1.8.2"  : DSMRMessage("\(([0-9\.]+)\*kWh\)", "in night",  float ),
  "1-0:2.8.2"  : DSMRMessage("\(([0-9\.]+)\*kWh\)", "out day",   float ),
  "1-0:2.8.2"  : DSMRMessage("\(([0-9\.]+)\*kWh\)", "out night", float ),
}

# 0-0:96.14.0(0001)           current tarif (1 = dag)
# 1-0:1.7.0(00.000*kW)        current afname
# 1-0:2.7.0(03.987*kW)        current injectie
# 1-0:32.7.0(249.1*V)         spanning fase 1
# 1-0:52.7.0(242.7*V)         spanning fase 2
# 1-0:72.7.0(244.3*V)         spanning fase 3
# 0-1:24.2.3(210405153007S)(00013.114*m3) gas (timestamp YYMMDDhhmmssS) (volume)

def parse(line):
  for header, message in protocol.items():
    if line.startswith(header):
      ( pattern, name, parse ) = message
      pattern = "^" + header + pattern + "$"
      result = re.search(pattern, line)
      if result:
        return name, parse(result.group(1))
  return None, None

if __name__ == "__main__":
  data = """
0-0:1.0.0(210405162433S)
1-0:1.8.1(002273.816*kWh)
1-0:1.8.2(003306.177*kWh)
1-0:2.8.1(002763.402*kWh)
1-0:2.8.2(001010.273*kWh)
  """

  for line in data.split("\n"):
    parse(line)
