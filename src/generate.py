import os
from dotenv import load_dotenv
from groq import Groq
from retrieve import retrieve
from vector_db import get_collection

load_dotenv()

MODEL = "openai/gpt-oss-120b"

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY not found. Check your .env file.")
client = Groq(api_key=api_key)


def animal_text(animal):
    """Fetch the PDF text of one specific animal from the DB."""
    key = animal.lower().replace(" ", "_")
    res = get_collection().get(ids=[f"text_{key}"])
    return res["documents"][0] if res["documents"] else None


def answer(question=None, image_path=None, k=3):
    question = question or "Tell me about this animal."
    results = retrieve(query_text=question, query_image=image_path, k=k)

    contexts = []
    identified = None

    # if the user sent an image, the best matching image tells us the animal
    if image_path:
        identified = results["image"][0]["animal"]
        t = animal_text(identified)
        if t:
            contexts.append(t)

    for r in results["text"]:
        if r["content"] not in contexts:
            contexts.append(r["content"])

    system = (
        "You are a friendly zoo guide. Answer ONLY using the context below. "
        "If the answer is not in the context, say you don't know."
    )
    if identified:
        system += f" The user's image was identified as: {identified}."

    user = "Context:\n" + "\n\n".join(contexts) + f"\n\nQuestion: {question}"

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.3,
    )
    return resp.choices[0].message.content


if __name__ == "__main__":
    print("--- Text only ---")
    print(answer("Which animal has a mane and lives in groups?"))

    print("\n--- Image + text ---")
    print(answer("What does it eat?", "data/images/giraffe_1.jpg"))

    print("\n--- Image only ---")
    print(answer(image_path="data/images/penguin_1.jpg"))