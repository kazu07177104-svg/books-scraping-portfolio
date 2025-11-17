# 📚 Books Scraping Portfolio  
Python（requests / BeautifulSoup4 / pandas）を使用して、  
公開されている練習用サイト **Books to Scrape** から  
複数ページの商品データを自動で取得し、CSV形式で保存するプロジェクトです。

---

## 🚀 使用技術
- Python 3.x  
- requests  
- BeautifulSoup4  
- pandas  

---

## 📁 概要  
対象サイト：https://books.toscrape.com/  
（スクレイピング学習用に公開されているサイトで、利用が許可されています）

取得する情報：
- タイトル  
- 価格  
- 在庫状況  
- 評価（星の数）  
- 詳細ページURL  

5ページ分の書籍を取得し、最終的に  
**books_portfolio.csv** に出力します。

---

## 🔍 処理の流れ
1. requests によるHTML取得  
2. BeautifulSoup によるHTML解析  
3. 商品ブロック（`article.product_pod`）から情報抽出  
4. ページネーション（複数ページ対応）  
5. pandas DataFrame で整形  
6. CSVとして保存  

---

## 📦 実行方法
```bash
python3 books_scrape.py
