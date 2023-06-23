import time
import aiohttp
import asyncio

import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

from mongo_db import insert_data
from mongo_db_async import insert_data_async

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
}

COLLECTIONS = {
    "bidon_cnn": "bidon_cnn",
    "trump_cnn": "trump_cnn",
    "bidon_politico": "bidon_politico",
    "trump_politico": "trump_politico",
}

SEARCH_TERM = {"bidon": "joe-biden", "trump": "donald-trump"}

TRUMP_QUERY = ("article", {"class": "story-frag format-m"})
BIDEN_QUERY = ("p", {"class": "story-full"})

START_PAGE = 99
TARGET_PAGE = 200

LINK_FILTER = "https://www.politico.com/news/"

URL = f"https://www.politico.com/news/{SEARCH_TERM.get('trump')}/"

CLASS_TAGS = [
    "story-text__paragraph",
    "story-text__heading-medium has-bottom-margin",
]


def get_links_per_page(url, headers, query):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        titles = soup.find_all(*query)
        links = [
            title.find("a").get("href")
            for title in titles
            if title.find("a").get("href").startswith(LINK_FILTER)
        ]
        links.pop()
        return links
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while retrieving links: {e}")
        return []


def save_to_file(links):
    with open("data/links.txt", "a") as file:
        file.writelines(link + "\n" for link in links)


def parse(url, headers):
    html_page = requests.get(url, headers=headers)
    soup = BeautifulSoup(html_page.text, "lxml")
    soup_title = soup.find("h2", {"class": "headline"})
    soup_pub_date = soup.find("p", {"class": "story-meta__timestamp"})
    soup_description = soup.find_all(["p", "h3"], {"class": CLASS_TAGS})
    description = "\n".join(post.text.strip() for post in soup_description)
    title = soup_title.text
    pub_date = soup_pub_date.text
    return (title, pub_date, description)


async def parse_async(url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response_text = await response.text()

            soup = BeautifulSoup(response_text, "lxml")
            soup_title = soup.find("h2", {"class": "headline"})
            soup_pub_date = soup.find("p", {"class": "story-meta__timestamp"})
            soup_description = soup.find_all(
                ["p", "h3"], {"class": CLASS_TAGS}
            )
            description = "\n".join(
                post.text.strip() for post in soup_description
            )
            title = soup_title.text
            pub_date = soup_pub_date.text

    return title, pub_date, description


async def main():
    progress_bar = tqdm(total=TARGET_PAGE - START_PAGE + 1, unit="page")
    for page in range(START_PAGE, TARGET_PAGE):
        url = f"{URL}{page}"
        links = get_links_per_page(url, HEADERS, TRUMP_QUERY)
        save_to_file(links)
        progress_bar.update(1)
        progress_bar.set_description(f"Processing page {page}")
    progress_bar.close()

    with open("data/links.txt", "r") as file:
        lines = file.readlines()
        total_lines = len(lines)
        lines_progress = tqdm(lines, total=total_lines, unit="line")
        for url in lines_progress:
            title, pub_date, description = parse(url, HEADERS)
            await insert_data_async(
                title, pub_date, description, COLLECTIONS["trump_politico"]
            )
            lines_progress.set_description(
                f"In process... {lines_progress.n}/{total_lines} lines"
            )

        lines_progress.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

# def main():
#     progress_bar = tqdm(total=TARGET_PAGE - START_PAGE + 1, unit="page")
#     for page in range(START_PAGE, TARGET_PAGE):
#         url = f"{URL}{page}"
#         links = get_links_per_page(url, HEADERS, TRUMP_QUERY)
#         time.sleep(1)
#         save_to_file(links)
#         progress_bar.update(1)
#         progress_bar.set_description(f"Processing page {page}")
#     progress_bar.close()

#     with open("data/links.txt", "r") as file:
#         lines = file.readlines()
#         total_lines = len(lines)
#         lines_progress = tqdm(lines, total=total_lines, unit="line")
#         for url in lines_progress:
#             title, pub_date, description = parse_async(url, HEADERS)
#             insert_data(
#                 title, pub_date, description, COLLECTIONS["trump_politico"]
#             )
#             lines_progress.set_description(
#                 f"In process... {lines_progress.n}/{total_lines} lines"
#             )

#         lines_progress.close()


# if __name__ == "__main__":
#     main()
