import chromadb
from ingest import load_chunks
from embed import embed_texts, embed_images

DB_PATH = "chroma_db"
COLLECTION = "zoo"


def get_collection():
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_or_create_collection(
        name=COLLECTION,
        metadata={"hnsw:space": "cosine"},  # CLIP vectors are normalized
    )


def build_index():
    chunks = load_chunks()
    client = chromadb.PersistentClient(path=DB_PATH)

    # rebuild from scratch so we never get duplicates
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    col = client.get_or_create_collection(
        name=COLLECTION, metadata={"hnsw:space": "cosine"}
    )

    # 1) text items
    texts = [c["text"] for c in chunks]
    col.add(
        ids=[c["id"] for c in chunks],
        embeddings=embed_texts(texts),
        documents=texts,
        metadatas=[{"type": "text", "animal": c["animal"], "page": c["page"]} for c in chunks],
    )

    # 2) image items
    img_paths, img_meta = [], []
    for c in chunks:
        for p in c["images"]:
            img_paths.append(p)
            img_meta.append({"type": "image", "animal": c["animal"], "path": p})

    col.add(
        ids=[f"img_{i}" for i in range(len(img_paths))],
        embeddings=embed_images(img_paths),
        documents=img_paths,  # for images we store the file path
        metadatas=img_meta,
    )

    print(f"Indexed {len(chunks)} texts + {len(img_paths)} images")
    print(f"Total items in DB: {col.count()}")


if __name__ == "__main__":
    build_index()

    # quick test: search by text
    col = get_collection()
    q = "a big cat with a mane"
    res = col.query(query_embeddings=embed_texts([q]), n_results=4)

    print(f"\nQuery: '{q}'")
    for meta, dist in zip(res["metadatas"][0], res["distances"][0]):
        print(f"  [{meta['type']:<5}] {meta['animal']:<10} (distance {dist:.3f})")