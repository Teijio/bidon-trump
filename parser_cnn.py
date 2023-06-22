import requests
import json
from pprint import pprint

url = "https://search.api.cnn.com/content"

querystring = {
    "q": "trump",
    "size": "2",
    "from": "0",
    "page": "1",
    "sort": "newest",
}

payload = ""
response = requests.request("GET", url, data=payload, params=querystring)

with open("test123.txt", "w") as file:
    file.write(response.text)

txt = response.text
js = json.loads(txt)
pprint(js["result"])

# with open("test123.txt") as f:
#     json_data = json.load(f)

# lt = json_data.get("result")
# for i in lt:
#     d = i.get("body")
#     print(d[:100])