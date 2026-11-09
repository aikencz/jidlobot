from bs4 import BeautifulSoup
import requests


def numbered_list(items):
    return "\n".join("  {}. {}".format(i + 1, item) for i, item in enumerate(items)) + "\n"


def fetch(url, config):
    menu = ""
    polevky = []
    jidla = []

    try:
        result = requests.get(url, timeout=config["HTTP_TIMEOUT"])
        html = BeautifulSoup(result.content, "html5lib")
        day = html.find_all("div", {"class": "menicka"})[0]
        restaurant = " ".join(html.select(".profile .line1 h1")[0].text.split())

        for line in day.select("li"):
            name = line.select(".polozka")
            if len(name) > 0:
                for extra in name[0].find_all(["em", "span"]):
                    extra.extract()
                text = " ".join(name[0].get_text(" ", strip=True).split())
                text = text.lstrip("*").strip()
                if not text:
                    continue
                if len(text) >= 200 and text[-1] not in ".!?…":
                    text += " …"
                price = line.select(".cena")
                if price:
                    text += " " + " ".join(price[0].text.split())
                if "polevka" in (line.get("class") or []):
                    polevky.append(text)
                else:
                    jidla.append(text)

        if polevky:
            menu += "- Polévky:\n"
            menu += numbered_list(polevky)
        if jidla:
            if menu:
                menu += "\n"
            menu += "- Hlavní jídla:\n"
            menu += numbered_list(jidla)

        if len(menu) > 0:
            return "\n#### " + restaurant + ":\n\n" + menu
        else:
            return ""

    except requests.exceptions.Timeout:
        return "" + url + ": timeout :angry:\n"

    except Exception:
        return "" + url + ": something went wrong :dizzy_face:\n"
