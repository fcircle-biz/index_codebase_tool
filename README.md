了解しました！
**Qdrant対応版・CLIとGUIすべて含めた最新版 README.md** を作成します。

---

## ✅ 【README.md（最新版）】

````markdown
# Index Codebase Tool（Qdrant版）

コードベース（ソースコード）をチャンクに分割し、ベクトルDB（Qdrant）にインデックス化。  
自然言語クエリでコード検索が可能です。  
**CLI・GUI（Streamlit）対応。**

---

## 🔧 必要条件

- Python 3.10 以上
- Docker（Qdrantサーバー用）
- 仮想環境（venv推奨）

---

## 📦 インストール手順

```bash
# 仮想環境作成
python3 -m venv venv
source venv/bin/activate

# 必要パッケージインストール
pip install -r requirements.txt
````

---

## 🐳 Qdrant サーバー起動

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

## 🖥 GUI検索（code-search-gui）

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

## 💡 補足

* ベクトル埋め込みモデル：`BAAI/bge-small-en`
* チャンクサイズ：512文字（重複50文字）
* LangChain & QdrantClient 使用

---

## ✅ 動作確認環境

* Ubuntu 22.04（WSL2）
* Qdrant 1.7.0（Docker）
* sentence-transformers 2.7.0
* langchain 0.1.14

```

---

## ✅ 【次のアクション】

この README.md を **プロジェクトルートの README.md** に保存すれば準備完了！

---

もしご希望なら、この README.md の **Qdrantサーバーの状態確認コマンド** や **トラブルシューティング（よくあるエラー例）** も追記できます。  

**追記しますか？（はい／いいえ）**
```
