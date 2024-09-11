import streamlit as st
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

st.set_page_config(page_title="Sanjay AI", page_icon="📚", layout="wide")

from sentence_transformers import SentenceTransformer
import requests
import xml.etree.ElementTree as ET
import nltk
from nltk.tokenize import sent_tokenize
import numpy as np
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Download necessary NLTK data
@st.cache_resource
def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)

    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab', quiet=True)

    try:
        sent_tokenize("This is a test sentence.")
    except Exception as e:
        st.error(f"Error initializing NLTK data: {e}")

download_nltk_data()

# Load models
@st.cache_resource
def load_models():
    sentence_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    flan_t5_model_name = "google/flan-t5-base"
    tokenizer = AutoTokenizer.from_pretrained(flan_t5_model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(flan_t5_model_name)
    return sentence_model, model, tokenizer

sentence_model, flan_t5_model, flan_t5_tokenizer = load_models()

# Fetch Papers from arXiv API
@st.cache_data(ttl=3600)
def fetch_papers_arxiv(topic, max_results=50):  # Reduced max_results
    base_url = 'http://export.arxiv.org/api/query?'
    query = f'search_query=all:{topic}&start=0&max_results={max_results}&sortBy=relevance&sortOrder=descending'

    response = requests.get(base_url + query)
    root = ET.fromstring(response.content)

    papers = []
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
        url = entry.find('{http://www.w3.org/2005/Atom}id').text.strip()
        date = entry.find('{http://www.w3.org/2005/Atom}published').text.strip()
        papers.append({"title": title, "summary": summary, "url": url, "date": date})

    return papers[:min(len(papers), 20)]  # Cap at 20 papers for faster processing

# Semantic Search
@st.cache_data(ttl=3600)
def semantic_search(query, papers):
    query_embedding = sentence_model.encode([query])
    paper_embeddings = sentence_model.encode([p['summary'] for p in papers])
    similarities = np.dot(query_embedding, paper_embeddings.T)[0]
    top_indices = np.argsort(similarities)[::-1][:5]  # Get top 5 most relevant papers
    return [papers[i] for i in top_indices]

# Generate Answer
def generate_answer(question, papers):
    # Prepare context by focusing on relevant parts of the papers with a higher relevance threshold
    relevant_contexts = []
    for paper in papers:
        relevance_score = sentence_model.encode(question).dot(sentence_model.encode(paper['title'] + " " + paper['summary']))
        if relevance_score > 0.7:  # Increased threshold for better relevance
            relevant_contexts.append(f"Title: {paper['title']}\nSummary: {paper['summary']}")
    
    full_context = "\n\n".join(relevant_contexts)
    
    prompt = f"""Based on the following research papers, provide a detailed and accurate answer to this question: {question}
    If the information is not directly available, synthesize a response based on related information.
    Include specific details, methods, and findings when relevant.

    Context:
    {full_context}

    Detailed Answer:"""
    
    input_ids = flan_t5_tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512).input_ids
    
    outputs = flan_t5_model.generate(
        input_ids,
        max_length=300,  # Increased for more detailed answers
        num_beams=5,  # Use more beams for more informed answers
        temperature=0.6,  # Slightly reduced temperature for more focused responses
        do_sample=True,  # Enable sampling for diversity
    )
    
    answer = flan_t5_tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Find the most relevant papers for citation
    paper_relevance = [
        (paper, sentence_model.encode(paper['summary']).dot(sentence_model.encode(answer)))
        for paper in papers
    ]
    relevant_papers = sorted(paper_relevance, key=lambda x: x[1], reverse=True)[:2]  # Top 2 relevant papers
    
    return {
        "answer": answer,
        "references": [{"title": paper['title'], "url": paper['url']} for paper, _ in relevant_papers]
    }

# Streamlit Frontend
def main():
    st.title("Sanjay AI Based on Research papers")

    st.markdown("""
    <style>
    .stButton>button {width: 100%;} 
    .paper-box {background-color: #000000; border-radius: 5px; padding: 10px; margin-bottom: 10px;}
    .answer-box {background-color: #036c5f; border-radius: 5px; padding: 10px; margin-bottom: 10px;}
    </style>
    """, unsafe_allow_html=True)

    topic = st.text_input("Enter your research topic:", key="topic_input")

    col1, col2 = st.columns([2,1])

    with col1:
        if st.button("🔍 Fetch Papers", key="fetch_button"):
            with st.spinner("Fetching papers..."):
                papers = fetch_papers_arxiv(topic)
            if papers:
                st.session_state.papers = papers
                st.session_state.top_papers = semantic_search(topic, papers)
                st.write(f"### Top Relevant Papers (out of {len(papers)} fetched)")
                for i, paper in enumerate(st.session_state.top_papers):
                    st.markdown(f"""
                    <div class="paper-box">
                    <h4>{i+1}. {paper['title']}</h4>
                    <p><strong>Date:</strong> {paper['date']}</p>
                    <p>{paper['summary'][:200]}...</p>
                    <a href="{paper['url']}" target="_blank">Read more</a>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("No papers found for the given topic.")

    with col2:
        st.write("### Ask a Question")
        question = st.text_input("Enter your question:", key="question_input")
        
        if st.button("🤔 Get Detailed Answer", key="answer_button"):
            if hasattr(st.session_state, 'top_papers'):
                with st.spinner("Generating detailed answer..."):
                    result = generate_answer(question, st.session_state.top_papers)
                st.write("### Answer:")
                st.markdown(f"""
                <div class="answer-box">
                <p>{result['answer']}</p>
                <h4>References:</h4>
                <ol>
                {"".join(f"<li><a href='{ref['url']}' target='_blank'>{ref['title']}</a></li>" for ref in result['references'])}
                </ol>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Please fetch papers first before asking a question.")

if __name__ == "__main__":
    main()
