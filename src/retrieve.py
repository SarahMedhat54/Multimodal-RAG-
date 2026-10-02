from embed import embed_texts, embed_images
from vector_db import get_collection


def retrieve(query_text=None, query_image=None, k=3):
    """Search with text, image, or both. Returns top texts and top images."""
    vecs = []
    if query_text:
        vecs.append(embed_texts([query_text])[0])
    if query_image:
        vecs.append(embed_images([query_image])[0])
    if not vecs:
        raise ValueError("Give a text, an image, or both")

    # text + image -> average the two vectors, then re-normalize
    n = len(vecs[0])
    q = [sum(v[i] for v in vecs) / len(vecs) for i in range(n)]
    norm = sum(x * x for x in q) ** 0.5
    q = [x / norm for x in q]

    col = get_collection()
    out = {}
    for kind in ("text", "image"):
        res = col.query(query_embeddings=[q], n_results=k, where={"type": kind})
        out[kind] = [
            {"animal": m["animal"], "distance": d, "content": doc}
            for m, d, doc in zip(res["metadatas"][0], res["distances"][0], res["documents"][0])
        ]
    return out


def show(title, results):
    print(f"\n=== {title} ===")
    for kind in ("text", "image"):
        for r in results[kind]:
            label = r["content"] if kind == "image" else r["content"][:60] + "..."
            print(f"  [{kind:<5}] {r['animal']:<10} d={r['distance']:.3f}  {label}")


if __name__ == "__main__":
    show("Text only: 'a big cat with a mane'",
         retrieve(query_text="a big cat with a mane"))

    show("Image only: tiger_1.jpg",
         retrieve(query_image="data/images/tiger_1.jpg"))

    show("Text + Image: 'what does it eat?' + giraffe_1.jpg",
         retrieve(query_text="what does it eat?", query_image="data/images/giraffe_1.jpg"))