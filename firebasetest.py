
import requests
import json
import base64

firebase_url = 'https://fordeyespi.firebaseio.com'

image = "fordgt.jpg"
messageId = 0
FL = 0
FR = 1
RL = 0
RC = 1
RR = 1
used = 0

with open(image, "rb") as imageFile:
        image64str = base64.b64encode(imageFile.read())
payload = {'picID':image64str}
result = requests.post(firebase_url + '/EyeSPI'+'/picture.json', data = json.dumps(payload))

firebaseId = result.json()['name']

payload = {'id':messageId, 'picID':firebaseId, 'FL': FL, 'FR':FR, 'RL':RL, 'RC':RC, 'RR':RR, 'used':used}
result = requests.post(firebase_url + '/EyeSPI'+'/message.json', data = json.dumps(payload))

print result.status_code


