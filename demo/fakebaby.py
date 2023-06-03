import requests
import random
import time


url = "https://iom7vetorqgo7rg77bo5o2mmee0vcpgy.lambda-url.eu-central-1.on.aws/create-measurement"

def create_measurement():
  body = {
    "cryDetected": random.choice([True, False]),
    "soundDetected": random.choice([True, False]),
    "movementDetected": random.choice([True, False]),
    "shouldNotifyClient": random.choice([True, False]),
    "lastUpdate": 0,
    "userId": "test_baby"
    }
  return body

while True:
  print("Making new fake measurement")
  x = requests.put(url, json = create_measurement())
  print(x.text)
  time.sleep(10)



  

