import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"

def scrape_amazon_demo():
    products = []

    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.select(".thumbnail")

    for item in items[:20]:  # 最初の20件だけ取得
        title_tag = item.select_one(".title")
        price_tag = item.select_one(".price")
        link_tag = item.select_one("a")

        title = title_tag.text.strip() if title_tag else ""
        price = price_tag.text.strip() if price_tag else ""
        detail_url = "https://webscraper.io" + link_tag["href"] if link_tag else ""
        stock = "N/A"  # デモサイトには在庫がないため

        products.append({
            "title": title,
            "price": price,
            "stock": stock,
            "detail_url": detail_url
        })

    # CSVに保存
    df = pd.DataFrame(products)
    df.to_csv("amazon_demo_products.csv", index=False, encoding="utf-8")
    return df


if __name__ == "__main__":
    df = scrape_amazon_demo()
    print(df.head())

