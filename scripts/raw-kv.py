"""
Experimental. No production usage allowed.
"""
from tikv_client import RawClient
import sys
scan_begin_key = sys.argv[1]
scan_for_values = sys.argv[2:]
print('Scan start from Key:',scan_begin_key, 'Scan for:', scan_for_values)
client = RawClient.connect(['127.0.0.1:2379','127.0.0.1:2382','127.0.0.1:2384'])

next_scan_begin_key_bytes = scan_begin_key.encode('unicode_escape')
last_scan_begin_key_bytes = None
proceed = True
while proceed:
  print('Scan from key:',next_scan_begin_key_bytes.decode('unicode_escape'))
  response = client.scan(next_scan_begin_key_bytes, b'', 1024, cf='lock')
  last_scan_begin_key_bytes = next_scan_begin_key_bytes
  for r in response:
    next_scan_begin_key_bytes = r[0]
    if last_scan_begin_key_bytes == next_scan_begin_key_bytes:
      proceed = False
    else:
      for value in scan_for_values:
        v = None
        try:
          v = r[1].decode('unicode_escape')
        except UnicodeDecodeError as ex:
          try:
            v = r[1].decode('unicode_escape')
          except UnicodeDecodeError as ex:
            v = '!!!!!!!!!!!!!!!!'
        if value in v:
          print('\tFOUND!','K:',r[0].decode('unicode_escape'),'V:',r[1].decode('unicode_escape'))