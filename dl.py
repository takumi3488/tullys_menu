import requests
from bs4 import BeautifulSoup
import csv
import re


def make_soup(url: str) -> BeautifulSoup:
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    return BeautifulSoup(res.text, "html.parser")


def main():
    BASE_URL = "https://www.tullys.co.jp"
    soup = make_soup("https://www.tullys.co.jp/menu/drink/")
    item_a_list = soup.select("ul.item_list a")
    links: list[str] = []
    for item_a in item_a_list:
        links.append(f'{BASE_URL}{item_a.attrs["href"]}')
    items: list[dict[str, str | int]] = []
    ptn = re.compile(r"\d{1,4}")
    for link in links:
        soup = make_soup(link)
        name = soup.select_one(".title-text")
        if name is None:
            raise RuntimeError(".title-text")
        name = name.text
        sizes = soup.select("ul.price_list>li>strong")
        prices = soup.select("ul.price_list>li>span:not(.tax_text)")
        if len(sizes) != len(prices):
            raise RuntimeError("sizes and prices")
        for i in range(len(sizes)):
            searcher = ptn.search(prices[i].text)
            if searcher is None:
                raise RuntimeError("searcher")
            price = int(searcher.group())
            item: dict[str, str | int] = {
                "商品名": name, "サイズ": sizes[i].text.strip(), "価格": price}
            items.append(item)
    with open("prices.csv", "w") as f:
        writer = csv.DictWriter(f, ["商品名", "サイズ", "価格"])
        writer.writeheader()
        writer.writerows(items)


if __name__ == "__main__":
    main()
