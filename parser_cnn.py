import requests
import json
from pprint import pprint

url = "https://search.api.cnn.com/content"



def parse(q):
    payload = ""
    response = requests.request("GET", url, data=payload, params=q)

    with open("test123.txt", "w") as file:
        file.write(response.text)

    txt = response.text
    js = json.loads(txt)
    pprint(js["result"])
page = 0

for i in range(10, 1500, 10):
    querystring = {
        "q": "trump",
        "size": "10",
        "from": i,
        "page": page + 1,
        "sort": "newest",
    }
    print(i)

# with open("test123.txt") as f:
#     json_data = json.load(f)

# lt = json_data.get("result")
# for i in lt:
#     d = i.get("body")
#     print(d[:100])