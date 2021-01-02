from bs4 import BeautifulSoup
import requests
from markdownify import markdownify as md


def search(query: str):
    search_response = requests.get(
        f"https://minecraft.gamepedia.com/Special:Search/Articles?fulltext=1&query={query}&scope=internal&limit=10"
    ).text
    search_source = BeautifulSoup(search_response, "lxml")
    search_results = []
    for ul_tag in search_source.find_all("ul", {"class": "unified-search__results"}):
        for li_tag in ul_tag.find_all("li"):
            for links in li_tag.find_all("a", {"class": "unified-search__result__link"}):
                search_results.append(links)
    return search_results[0]["href"]


def scrape_about(url: str):
    scrape_response = requests.get(url).text
    scrape_source = BeautifulSoup(scrape_response, "lxml")
    if scrape_source.table is not None:
        scrape_source.table.decompose()
    title = scrape_source.title.text
    paras = []
    image = None
    for divs in scrape_source.find_all(
        "div", {"class": "mw-parser-output"}
    ):  # the main div tag with all the content needed
        image = divs.find("img")
        for para in divs.find_all("p"):
            paras.append(para.text)
    return title, paras, image["src"]


def scrape_table(url: str):
    table_response = requests.get(url).text
    table_source = BeautifulSoup(table_response, "lxml")
    table_title = table_source.title.text
    info_table = None
    image = None
    for divs in table_source.find_all("div", {"class": "mw-parser-output"}):
        image = divs.find("img")
        info_table = divs.find("table")
    markdown = md(f"{info_table}", strip=["a"])
    return table_title, markdown, image["src"]
