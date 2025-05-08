# Index Codebase Tool（Qdrant版）

コードベース（ソースコード）をチャンクに分割し、ベクトルDB（Qdrant）にインデックス化。
自然言語クエリでコード検索が可能です。
**CLI・GUI（Streamlit）対応。**

---

## 🔧 必要条件

* Python 3.10 以上
* Docker（Qdrantサーバー用）
* 仮想環境（venv推奨）

---

## 📦 インストール手順

```bash
# 仮想環境作成
python3 -m venv venv
source venv/bin/activate

# 必要パッケージインストール
pip install -r requirements.txt
```

---

## 🛣 Qdrant サーバー起動

**docker-compose.yml** を使って起動：

```bash
docker-compose up -d
```

停止：

```bash
docker-compose down
```

※ Qdrantのデータは `qdrant_storage/` フォルダに永続保存されます。

---

## 🗂 インデックス作成（index-codebase）

```bash
index-codebase -s ./YOUR_CODEBASE
```

対象拡張子：`.py` `.js` `.ts` `.java` `.cs` `.go` `.md` `.html`

* ファイルの変更検知
* 新規／変更ファイルのみチャンク登録
* 削除ファイルは自動的にインデックスから削除

---

## 🔍 CLI検索（code-search-cli）

```bash
code-search-cli -q "ユーザー認証処理"
```

オプション：

```bash
code-search-cli -q "認証API" -k 10  # 上位10件取得
```

---

## 🔝 GUI検索（code-search-gui）

```bash
code-search-gui
```

ブラウザが自動起動。
自然言語クエリでコード検索＆結果表示。

---

## 📝 .gitignore 推奨設定

```plaintext
*.egg-info/
dist/
build/
__pycache__/
*.pyc
venv/
qdrant_storage/
file_hashes.json
```

---

## 🔎 Qdrantサーバー状態確認コマンド

**Qdrantコンテナの状態確認：**

```bash
docker-compose ps
```

**登録済みコレクション一覧確認（Pythonから）：**

```python
from qdrant_client import QdrantClient
client = QdrantClient(host="localhost", port=6333)
print(client.get_collections())
```

**→ 'code\_collection' が表示されれば正常。**

---

## 🌐 Qdrantダッシュボード（Web UI）

**Qdrant UI（外部ツール）**
[https://qdrant.github.io/qdrant/redoc/](https://qdrant.github.io/qdrant/redoc/)

または Postman / curl で REST API エンドポイント：

```plaintext
http://localhost:6333/collections
```

---

## 🛐 トラブルシューティング

### ❗ Qdrant 500エラー（No such file or directory）

```plaintext
Service internal error: No such file or directory (os error 2)
```

**原因：**
`qdrant_storage` フォルダが削除された、または権限エラー。

**対処：**

```bash
sudo chown -R ichimaru:ichimaru qdrant_storage
docker-compose down
docker-compose up -d
```

---

### ❗ Streamlit GUI が起動しない／警告が出る

```plaintext
missing ScriptRunContext!
```

**原因：**
streamlit run を使わずにコードを直接実行している。

**対処：**
最新版では `code-search-gui` コマンドで streamlit run が自動呼び出される → **無視してOK**。
または手動実行：

```bash
streamlit run index_codebase_tool/search_gui.py
```

---

### ❗ index-codebase コマンドで更新されない

**原因：**
対象ファイルの内容に変更がない（正常動作）。

変更した場合のみチャンクが更新され、Qdrantに反映されます。

---

## 📅 動作確認環境

* Ubuntu 22.04（WSL2）
* Qdrant 1.7.0（Docker）
* sentence-transformers 2.7.0
* langchain 0.1.14

---

## 🔧 【運用メモ】

* **qdrant\_storage** を消すとインデックスも消える（注意）
* **file\_hashes.json** も各コードベースごとに異なる
* GUI と CLI は仮想環境を有効にしてから使用

---

## 📄 ライセンス

このツールは **MITライセンス** で提供されます。

```plaintext
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

※ フルテキストは `LICENSE` ファイルをご参照ください。

---

## 🌟 貢献・改良

バグ報告・機能提案は歓迎します！
Pull Request や Issue を通じてご連絡ください。

---

## 🔹 補足

「インデックス化＝セマンティック検索可能にする準備」としてチャンク分割＋ベクトル登録を行っています。
