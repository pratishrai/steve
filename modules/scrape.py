from bs4 import BeautifulSoup
import requests


def search(query: str):
    search_response = requests.get(
        f"https://minecraft.gamepedia.com/Special:Search/Articles?fulltext=1&query={query}&scope=internal&limit=10"
    ).text
    search_source = BeautifulSoup(search_response, "lxml")
    search_results = []
    for ultag in search_source.find_all("ul", {"class": "unified-search__results"}):
        for litag in ultag.find_all("li"):
            for links in litag.find_all("a", {"class": "unified-search__result__link"}):
                search_results.append(links)

    return search_results[0]["href"]


def scrape(url: str):
    scrape_response = requests.get(url).text
    scrape_source = BeautifulSoup(scrape_response, "lxml")
    paras = []
    for divs in scrape_source.find_all(
        "div", {"class": "mw-parser-output"}
    ):  # the main div tag with all the content needed
        for para in divs.find_all("p"):
            paras.append(para.text)
    return paras


query = search("iron ingot")
paras = scrape(query)
file = open("iron.py", "w", newline="")
file.write(f"{paras}")
file.close()
