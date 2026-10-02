
import streamlit as st
import tempfile
from pathlib import Path

from generate import answer


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title=" The Zoooo",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    .hero {
        padding: 28px;
        border-radius: 18px;
        background: linear-gradient(120deg, #172554, #1d4ed8);
        color: white;
        margin-bottom: 24px;
    }

    .hero h1 {
        color: white;
        margin-bottom: 8px;
    }

    .hero p {
        color: #dbeafe;
        font-size: 16px;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        min-height: 45px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="hero">
    <h1>🦁 Zoo Multimodal RAG</h1>
    <p>
        Explore the animal kingdom using text, images,
        and AI-powered retrieval.
    </p>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# Sidebar
# -----------------------------

st.markdown("""
<style>
    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="collapsedControl"] {
        display: none;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Example Questions
# -----------------------------
st.subheader("💡 Try an Example")

examples = [
    "Which animal has a mane and lives in groups?",
    "What do giraffes eat?",
    "Which animals live in Africa?",
]

cols = st.columns(3)

if "question" not in st.session_state:
    st.session_state.question = ""

for i, example in enumerate(examples):
    if cols[i].button(example, key=f"example_{i}"):
        st.session_state.question = example


# -----------------------------
# User Input
# -----------------------------
st.subheader("Ask About an Animal")

question = st.text_area(
    "Your question",
    key="question",
    placeholder="Example: What does this animal eat?",
    height=100,
)

uploaded_image = st.file_uploader(
    "Upload an animal image (optional)",
    type=["jpg", "jpeg", "png", "webp"],
    help="Upload an image to search for a similar animal.",
)

if uploaded_image is not None:
    st.image(
        uploaded_image,
        caption="Uploaded Image",
        width=320,
    )

st.caption(
    "You can enter a question, upload an image, or do both."
)

search_clicked = st.button(
    "✨ Find Answer",
    type="primary",
)


# -----------------------------
# Retrieval and Generation
# -----------------------------
if search_clicked:

    if not question.strip() and uploaded_image is None:
        st.warning("Please enter a question or upload an image.")

    else:
        image_path = None

        try:
            # Save uploaded image temporarily
            if uploaded_image is not None:
                suffix = Path(uploaded_image.name).suffix.lower()

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix,
                ) as temp_file:
                    temp_file.write(uploaded_image.getvalue())
                    image_path = temp_file.name

            with st.spinner(
                "Searching the knowledge base and generating an answer..."
            ):
                if image_path is not None:
                    response = answer(
                        question.strip(),
                        image_path=image_path,
                    )
                else:
                    response = answer(question.strip())

            st.divider()
            st.subheader("🤖 AI Response")

            st.markdown(response)

        except Exception as error:
            st.error("Something went wrong while processing your query.")

            with st.expander("View error details"):
                st.code(str(error))

        finally:
            if image_path is not None:
                Path(image_path).unlink(missing_ok=True)


# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "Zoo Multimodal RAG | Text Retrieval + Image Retrieval + LLM"
)