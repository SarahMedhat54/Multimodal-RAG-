from pathlib import Path
import fitz  # PyMuPDF

PDF_PATH = Path("data/zoo_animals.pdf")
IMAGES_DIR = Path("data/images")


def load_chunks():
    """Read the PDF and return one chunk per animal page."""
    doc = fitz.open(PDF_PATH)
    chunks = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        if not text:
            continue

        # first line of the page = animal name
        name = text.splitlines()[0].strip()
        key = name.lower().replace(" ", "_")  # "Brown Bear" -> "brown_bear"

        # find this animal's images by name
        images = sorted(str(p) for p in IMAGES_DIR.glob(f"{key}_*.jpg"))

        chunks.append({
            "id": f"text_{key}",
            "animal": name,
            "page": page_num,
            "text": " ".join(text.split()),  # clean extra whitespace
            "images": images,
        })

    return chunks


if __name__ == "__main__":
    chunks = load_chunks()
    print(f"Total chunks: {len(chunks)}\n")
    for c in chunks[:3]:
        print(f"[{c['animal']}] page {c['page']}")
        print(f"  text: {c['text'][:100]}...")
        print(f"  images: {c['images']}\n")

    # sanity check: any animal without images?
    missing = [c["animal"] for c in chunks if not c["images"]]
    print("Animals with no images:", missing or "none ✅")