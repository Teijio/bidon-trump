import requests
from bs4 import BeautifulSoup


url = "https://www.politico.com/news/donald-trump/1"
headers = {
    "Accept": "*/*",
    "User-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
}
html = requests.get(url, headers=headers)

bs4_object = BeautifulSoup(html.content, "lxml")

f = bs4_object.find_all("article", {"class": "story-frag format-m"})
l = []
for obj in f:
    mm = obj.find("a")
    l.append(mm["href"])

print(l)