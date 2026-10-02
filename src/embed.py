import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

MODEL_NAME = "openai/clip-vit-base-patch32"

device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained(MODEL_NAME).to(device).eval()
processor = CLIPProcessor.from_pretrained(MODEL_NAME)


def _normalize(x: torch.Tensor) -> torch.Tensor:
    # normalize so cosine similarity works properly
    return x / x.norm(dim=-1, keepdim=True)


def _to_tensor(out):
    # newer transformers versions may return an object instead of a tensor
    return out if isinstance(out, torch.Tensor) else out.pooler_output


@torch.no_grad()
def embed_texts(texts: list[str]) -> list[list[float]]:
    inputs = processor(
        text=texts, return_tensors="pt", padding=True,
        truncation=True, max_length=77,  # CLIP limit
    ).to(device)
    feats = _to_tensor(model.get_text_features(**inputs))
    return _normalize(feats).cpu().tolist()


@torch.no_grad()
def embed_images(paths: list[str]) -> list[list[float]]:
    images = [Image.open(p).convert("RGB") for p in paths]
    inputs = processor(images=images, return_tensors="pt").to(device)
    feats = _to_tensor(model.get_image_features(**inputs))
    return _normalize(feats).cpu().tolist()


if __name__ == "__main__":
    from ingest import load_chunks

    chunks = load_chunks()

    # quick test: text vs image similarity
    text_vecs = embed_texts([c["text"] for c in chunks])
    img_paths = [c["images"][0] for c in chunks]
    img_vecs = embed_images(img_paths)

    print(f"Text vector size: {len(text_vecs[0])}")
    print(f"Image vector size: {len(img_vecs[0])}\n")

    # does each animal's first image match its own text best?
    t = torch.tensor(text_vecs)
    i = torch.tensor(img_vecs)
    sims = i @ t.T  # rows = images, cols = texts

    correct = 0
    for idx, c in enumerate(chunks):
        best = sims[idx].argmax().item()
        ok = best == idx
        correct += ok
        print(f"{'✅' if ok else '❌'} image of {c['animal']:<13} -> best text: {chunks[best]['animal']}")

    print(f"\nAccuracy: {correct}/{len(chunks)}")