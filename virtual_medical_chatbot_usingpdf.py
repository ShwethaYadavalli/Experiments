import streamlit as st
import openai
import fitz  # PyMuPDF

# Set OpenAI API key
openai.api_key = "your_openai_api_key"

# PDF text extraction function
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# Search function to find relevant snippet in the PDF text
def search_text(query, text):
    query = query.lower()
    text = text.lower()
    
    start = text.find(query)
    if start == -1:
        return "Sorry, I could not find any relevant information."
    
    end = min(start + len(query) + 300, len(text))
    snippet = text[start - 300:end]
    
    return snippet

# Use GPT to generate a medical diagnosis answer based on the snippet
def generate_answer_from_snippet(snippet, user_query):
    prompt = f"""
    The following is an excerpt from a medical encyclopedia. 
    Based on this, answer the following question as accurately as possible:
    
    Excerpt: {snippet}
    
    Question: {user_query}
    
    Answer:
    """
    response = openai.Completion.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5
    )

    answer = response.choices[0].text.strip()
    return answer

# Streamlit UI
st.title("🩺 Medical Diagnosis Chatbot")

# Upload PDF button
pdf_file = st.file_uploader("Medical Encyclopedia PDF", type=["pdf"])

if pdf_file is not None:
    pdf_text = extract_text_from_pdf(pdf_file)
    st.write("PDF Loaded! You can now ask medical questions.")

    # User input (question)
    user_query = st.text_input("Ask a medical question:", "")

    if user_query:
        # Search for relevant snippet in the PDF
        snippet = search_text(user_query, pdf_text)

        # Generate a response using GPT
        response = generate_answer_from_snippet(snippet, user_query)

        # Display the result
        st.subheader("Answer from Medical Encyclopedia:")
        st.write(response)
