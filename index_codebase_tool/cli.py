import os
import hashlib
import json
import argparse
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from tqdm import tqdm

def main():
    #########################
    # 引数処理
    #########################
    parser = argparse.ArgumentParser(description="コードベースをQdrantにインデックス化")
    parser.add_argument("-s", "--source", required=True, help="ソースコードディレクトリ")
    args = parser.parse_args()

    SOURCE_DIR = args.source
    TARGET_EXTENSIONS = [".py", ".js", ".ts", ".java", ".cs", ".go", ".md", ".html"]
    HASH_RECORD_FILE = "file_hashes.json"
    COLLECTION_NAME = "code_collection"

    #########################
    # ファイル収集
    #########################
    def get_code_files(source_dir, extensions):
        code_files = []
        for root, _, files in os.walk(source_dir):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    code_files.append(os.path.join(root, file))
        return code_files

    #########################
    # ハッシュ計算
    #########################
    def compute_file_hash(filepath):
        h = hashlib.sha256()
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()

    #########################
    # Qdrantクライアント初期化
    #########################
    qdrant = QdrantClient(host="localhost", port=6333)

    embedder = SentenceTransformer("BAAI/bge-small-en")

    #########################
    # コレクション作成（もし存在しなければ）
    #########################
    existing_collections = [col.name for col in qdrant.get_collections().collections]
    if COLLECTION_NAME not in existing_collections:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        print(f"Qdrant コレクション '{COLLECTION_NAME}' を作成しました。")
    else:
        print(f"Qdrant コレクション '{COLLECTION_NAME}' を使用します。")

    #########################
    # 既存ハッシュの読み込み
    #########################
    if os.path.exists(HASH_RECORD_FILE):
        with open(HASH_RECORD_FILE, 'r') as f:
            existing_hashes = json.load(f)
    else:
        existing_hashes = {}

    #########################
    # コード分割
    #########################
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=50,
        separators=["\nclass ", "\ndef ", "\n\n", "\n", " "]
    )

    #########################
    # ファイル処理
    #########################
    code_files = get_code_files(SOURCE_DIR, TARGET_EXTENSIONS)
    new_hashes = {}
    processed_files = set()

    chunk_count = 0
    updated_files = 0
    skipped_files = 0

    print(f"=== 処理対象ファイル数: {len(code_files)} ===")

    for filepath in tqdm(code_files, desc="ファイル処理中"):
        file_hash = compute_file_hash(filepath)
        new_hashes[filepath] = file_hash
        processed_files.add(filepath)

        if filepath in existing_hashes and existing_hashes[filepath] == file_hash:
            skipped_files += 1
            print(f"[スキップ] {filepath}（変更なし）")
            continue

        updated_files += 1
        print(f"[更新] {filepath}")

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()

        chunks = splitter.split_text(code)

        # 既存チャンク削除
        # Qdrantはidによる削除が可能（存在しない場合もエラーにはならない）
        for i in range(0, 1000):
            point_id = int(abs(hash(f"{filepath}__chunk_{i}")) % (2**63))
            try:
                qdrant.delete(collection_name=COLLECTION_NAME, points_selector={"points": [point_id]})
            except:
                break

        # 新規チャンク登録
        for i, chunk in enumerate(chunks):
            vector = embedder.encode(chunk).tolist()
            point_id = int(abs(hash(f"{filepath}__chunk_{i}")) % (2**63))
            qdrant.upsert(
                collection_name=COLLECTION_NAME,
                points=[
                    PointStruct(
                        id=point_id,
                        vector=vector,
                        payload={"text": chunk, "source_file": filepath, "chunk_index": i}
                    )
                ]
            )
            chunk_count += 1

        print(f" → チャンク登録数: {len(chunks)}")

    #########################
    # ハッシュ保存
    #########################
    with open(HASH_RECORD_FILE, 'w') as f:
        json.dump(new_hashes, f, indent=2)

    #########################
    # 結果出力
    #########################
    print("\n=== 処理完了 ===")
    print(f"変更ファイル: {updated_files}")
    print(f"スキップ（変更なし）: {skipped_files}")
    print(f"新規/更新チャンク: {chunk_count}")

if __name__ == "__main__":
    main()
