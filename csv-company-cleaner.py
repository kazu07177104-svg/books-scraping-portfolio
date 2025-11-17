import pandas as pd
import unicodedata
import re

def normalize_text(text):
    """空白除去 & 全角→半角 正規化"""
    if pd.isna(text):
        return ""
    text = str(text).strip()
    text = unicodedata.normalize("NFKC", text)
    return text

def clean_phone(phone):
    """電話番号を半角数字とハイフンだけに整形"""
    if pd.isna(phone):
        return ""
    phone = unicodedata.normalize("NFKC", str(phone))
    phone = re.sub(r"[^0-9\-]", "", phone)
    return phone

def clean_address(address):
    """住所の空白除去 / 全角→半角"""
    return normalize_text(address)

def remove_duplicates(df):
    """会社名で重複削除"""
    if "company_name" in df.columns:
        df = df.drop_duplicates(subset=["company_name"])
    return df

def clean_csv(input_path, output_path):
    print("CSV読み込み中:", input_path)
    df = pd.read_csv(input_path)

    # 全列共通のクレンジング
    for col in df.columns:
        df[col] = df[col].apply(normalize_text)

    # 住所クリーニング
    if "address" in df.columns:
        df["address"] = df["address"].apply(clean_address)

    # 電話番号クリーニング
    if "phone" in df.columns:
        df["phone"] = df["phone"].apply(clean_phone)

    # 重複削除
    df = remove_duplicates(df)

    # 出力
    df.to_csv(output_path, index=False)
    print("クリーン済みCSVを保存:", output_path)


# ------------------------
# 実行例（ローカルで動かす場合）
# ------------------------
if __name__ == "__main__":
    clean_csv(
        input_path="input.csv",
        output_path="cleaned_output.csv"
    )

