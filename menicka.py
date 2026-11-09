from bs4 import BeautifulSoup
import requests


def fetch(url, config):
    menu = ""
    names = []
    prices = []

    try:
        result = requests.get(url, timeout=config["HTTP_TIMEOUT"])
        html = BeautifulSoup(result.content, "html5lib")
        day = html.find_all("div", {"class": "menicka"})[0]
        restaurant = " ".join(html.select(".profile .line1 h1")[0].text.split())

        for line in day.select("li"):
            name = line.select(".polozka")
            if len(name) > 0:
                names.append(" ".join(name[0].text.split()))
                prices.append(" ".join(name[0].next_sibling.next_sibling.text.split()))

        for i in range(len(names)):
            line = "- " + names[i] + " " + prices[i]
            menu += line + "\n"

        if len(menu) > 0:
            return "\n#### " + restaurant + ":\n\n" + menu
        else:
            return ""

    except requests.exceptions.Timeout:
        return "" + url + ": timeout :angry:\n"

    except Exception:
        return "" + url + ": something went wrong :dizzy_face:\n"
