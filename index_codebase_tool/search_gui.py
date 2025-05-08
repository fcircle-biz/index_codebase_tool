import streamlit as st
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

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
# Streamlitアプリ
#########################
st.title("コードベース検索（Qdrant版）")

query = st.text_input("検索クエリ（自然言語）", "")
top_k = st.slider("表示件数", 1, 20, 5)

if st.button("検索") and query:
    query_vector = embedder.encode(query).tolist()

    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k
    )

    if results:
        for point in results:
            payload = point.payload
            st.markdown(f"### スコア: {point.score:.4f}")
            st.markdown(f"**ファイル**: {payload.get('source_file', '不明')} （チャンク: {payload.get('chunk_index', '?')})")
            st.code(payload.get('text', '（テキスト無し）'), language="plaintext")
            st.markdown("---")
    else:
        st.info("一致するコードは見つかりませんでした。")

def main():
    import os
    import sys
    # Streamlitアプリを起動
    os.system(f"streamlit run {os.path.abspath(__file__)} {' '.join(sys.argv[1:])}")

if __name__ == "__main__":
    main()
