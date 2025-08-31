from pymemcache.client import base
import requests
import json
import time

# record start time
start = time.time()

def do_some_query():
    response_API = requests.get('https://gmail.googleapis.com/$discovery/rest?version=v1')
    data = response_API.text
    parse_json = json.loads(data)
    info = parse_json['description']
    print("Info about API:\n", info)
    key = parse_json['parameters']['key']['description']
    print("\nDescription about the key:\n",key)
    return key


# Don't forget to run `memcached' before running this code
client = base.Client(('localhost', 11211))
result = client.get('some_key')

if result is None:
    # The cache is empty, need to get the value
    # from the canonical source:
    result = do_some_query()

    # Cache the result for next time:
    client.set('some_key', result)

print(result)

# record end time
end = time.time()

# print the difference between start
# and end time in milliseconds
print("The time of execution of above program is :",
      (end-start) * 10**3, "ms")
