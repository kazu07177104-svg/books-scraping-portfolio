import time
import requests
from bs4 import BeautifulSoup
import pandas as pd


BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/118.0.0.0 Safari/537.36"
    )
}

def fetch_page(page: int) -> BeautifulSoup | None:
    """
    指定ページ番号のHTMLを取得して、BeautifulSoupオブジェクトを返す。
    失敗したら None を返す。
    """
    url = BASE_URL.format(page)
    print(f"[INFO] ページ {page} 取得中: {url}")

    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        # ステータスコードが200番台でなければ例外にする
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] ページ {page} の取得に失敗しました: {e}")
        return None

    return BeautifulSoup(res.text, "html.parser")


def parse_books(soup: BeautifulSoup) -> list[dict]:
    """
    1ページ分のHTMLから、書籍情報をリストとして抽出して返す。
    """
    books = []

    # 各書籍1件分のブロックを取得
    # <article class="product_pod"> ... </article>
    items = soup.select("article.product_pod")

    if not items:
        print("[WARN] 書籍のブロックが見つかりませんでした。セレクタを見直す必要があるかもしれません。")

    for item in items:
        # タイトル
        title_el = item.select_one("h3 a")
        title = title_el.get("title", "").strip() if title_el else ""

        # 価格 (£51.77 のような表示)
        price_el = item.select_one(".price_color")
        price = price_el.get_text(strip=True) if price_el else ""

        # 在庫（In stock 〜）
        stock_el = item.select_one(".instock.availability")
        stock = stock_el.get_text(strip=True) if stock_el else ""

        # 評価（クラスに 'star-rating Three' などが入っている）
        rating_el = item.select_one("p.star-rating")
        rating = ""
        if rating_el and "class" in rating_el.attrs:
            classes = rating_el["class"]
            # 例: ['star-rating', 'Three'] のような構造
            for c in classes:
                if c != "star-rating":
                    rating = c
                    break

        # 詳細ページURL（相対パス → 絶対URLに変換）
        link_el = item.select_one("h3 a")
        detail_url = ""
        if link_el and link_el.has_attr("href"):
            href = link_el["href"]
            detail_url = requests.compat.urljoin("https://books.toscrape.com/catalogue/", href)

        books.append(
            {
                "タイトル": title,
                "価格": price,
                "在庫": stock,
                "評価": rating,
                "詳細URL": detail_url,
            }
        )

    return books


def main():
    all_books: list[dict] = []

    # 1〜5ページ分だけ取得（ポートフォリオ用には十分）
    for page in range(1, 6):
        soup = fetch_page(page)
        if soup is None:
            # 取得に失敗したらそのページはスキップ
            continue

        page_books = parse_books(soup)

        # もし書籍が1件も取れなかったら、それ以降はループ終了
        if not page_books:
            print(f"[INFO] ページ {page} で書籍が見つからなかったため、処理を終了します。")
            break

        all_books.extend(page_books)

        # アクセスしすぎ防止のため待機
        time.sleep(1)

    # DataFrameに変換してCSV保存
    df = pd.DataFrame(all_books)
    output_name = "books_portfolio.csv"
    df.to_csv(output_name, index=False, encoding="utf-8-sig")

    print(f"[DONE] {len(all_books)}件のデータを {output_name} に保存しました。")


if __name__ == "__main__":
    main()
