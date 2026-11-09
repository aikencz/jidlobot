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
                for allergen in name[0].find_all("em"):
                    allergen.extract()
                names.append(" ".join(name[0].get_text(" ", strip=True).split()))
                price = line.select(".cena")
                prices.append(" ".join(price[0].text.split()) if price else "")

        for i in range(len(names)):
            line = "- " + names[i]
            if prices[i]:
                line += " " + prices[i]
            menu += line + "\n"

        if len(menu) > 0:
            return "\n#### " + restaurant + ":\n\n" + menu
        else:
            return ""

    except requests.exceptions.Timeout:
        return "" + url + ": timeout :angry:\n"

    except Exception:
        return "" + url + ": something went wrong :dizzy_face:\n"
