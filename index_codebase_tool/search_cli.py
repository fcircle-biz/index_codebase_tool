import argparse
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

def main():
    #########################
    # 引数処理
    #########################
    parser = argparse.ArgumentParser(description="コードベース（Qdrant）を自然言語で検索")
    parser.add_argument("-q", "--query", required=True, help="検索クエリ（自然言語）")
    parser.add_argument("-k", "--top_k", type=int, default=5, help="取得する上位件数（デフォルト5件）")
    args = parser.parse_args()

    query = args.query
    top_k = args.top_k

    #########################
    # Qdrant接続
    #########################
    COLLECTION_NAME = "code_collection"
    qdrant = QdrantClient(host="localhost", port=6333)

    #########################
    # 埋め込みモデル
    #########################
    embedder = SentenceTransformer("BAAI/bge-small-en")

    #########################
    # クエリのベクトル化
    #########################
    query_vector = embedder.encode(query).tolist()

    #########################
    # Qdrantで類似検索
    #########################
    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k
    )

    #########################
    # 結果表示
    #########################
    print(f"【検索クエリ】 {query}")
    print("===================================")

    if results:
        for point in results:
            payload = point.payload
            print(f"スコア: {point.score:.4f}")
            print(f"ファイル: {payload.get('source_file', '不明')} （チャンク: {payload.get('chunk_index', '?')})")
            print(payload.get('text', '（テキスト無し）'))
            print("-----------------------------------")
    else:
        print("一致するコードは見つかりませんでした。")

if __name__ == "__main__":
    main()
