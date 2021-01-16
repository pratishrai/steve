from bs4 import BeautifulSoup
import requests


def search(query: str):
    search_response = requests.get(
        f"https://minecraft.gamepedia.com/Special:Search/Articles?fulltext=1&query={query}&scope=internal&limit=5"
    ).text
    search_source = BeautifulSoup(search_response, "lxml")
    search_results = []
    for ul_tag in search_source.find_all("ul", {"class": "unified-search__results"}):
        for li_tag in ul_tag.find_all("li"):
            for links in li_tag.find_all(
                "a", {"class": "unified-search__result__link"}
            ):
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
    for divs in scrape_source.find_all("div", {"class": "mw-parser-output"}):
        image = divs.find("img")
        for para in divs.find_all("p"):
            paras.append(para.text)
    return title, paras, image["src"]


def scrape_crafting(query: str):
    crafting_response = requests.get(
        f"https://www.minecraftcraftingguide.net/search/?s={query}"
    ).text
    crafting_source = BeautifulSoup(crafting_response, "lxml")
    image = None
    info = None
    ingredients = None
    for table in crafting_source.find_all("table", {"class": "craftingTable"}):
        image = table.find("img")["src"]
        info = table.find("span")
        ingredients = info.findNext("td")
    return image, info.text, ingredients.text


def tips_tricks():
    tt_response = requests.get("https://minecraft.fandom.com/wiki/Minecraft_Tips").text
    tt_source = BeautifulSoup(tt_response, "lxml")
    tt_div = tt_source.find("div", {"class": "mw-parser-output"})
    tt_list = []
    for litag in tt_div.find_all("li"):
        tt_list.append(litag.text)
    return tt_list[5:]
