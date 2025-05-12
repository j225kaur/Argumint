import streamlit as st
from paper_search import search_papers 
from llama_cpp import Llama

llm = Llama.from_pretrained(
    repo_id="TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
    filename="tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
)

def summarize_abstract(abstract):
    try:
        prompt = f"Summarize this abstract in 2 sentences:\n\n{abstract}"
        result = llm(prompt, max_tokens=100, echo=False)
        return result["choices"][0]["text"].strip()
    except Exception:
        return abstract[:400] + "..."

def format_summaries(papers):
    formatted = ""
    for i, paper in enumerate(papers[:3], 1):
        summary = summarize_abstract(paper['abstract'])
        formatted += f"\nAbstract {i} Summary:\n{summary}\n"
    return formatted.strip()

def get_feedback(argument, summarized_abstracts):
    prompt = f"""
Given the following user claim and supporting research summaries, evaluate how accurate the claim is based on the summaries. 

User claim: "{argument}"

Summarized Research Abstracts:
{summarized_abstracts}

Your output should include:
1. A short answer: Is the user claim supported? (Yes, No, Partially)
2. Two bullet points explaining why.
"""
    output = llm(prompt, max_tokens=512, echo=False)
    return output["choices"][0]["text"].strip()

# Streamlit UI
st.set_page_config(page_title="ArguMint", layout="wide")
st.title("🧠 ArguMint: AI-Powered Argument Assistant")

user_argument = st.text_area("Enter your argument:", height=150)

if st.button("Find Supporting Research") and user_argument:
    with st.spinner("Searching Semantic Scholar..."):
        papers = search_papers(user_argument)

    if not papers:
        st.warning("No relevant papers found. Try rephrasing.")
    else:
        st.subheader("🔍 Top Relevant Papers")
        for i, paper in enumerate(papers, 1):
            with st.expander(f"{i}. {paper['title']}"):
                st.markdown(f"**Authors**: {paper['authors']}")
                st.markdown(f"**Abstract**: {paper['abstract']}")
                st.markdown(f"[Read More]({paper['url']})")

        with st.spinner("Analyzing your argument..."):
            try:
                summaries = format_summaries(papers)
                feedback = get_feedback(user_argument, summaries)
                st.subheader("🧠 Local LLM Feedback")
                st.markdown(feedback)
            except Exception as e:
                st.error(f"LLM Error: {e}")

if st.button("Ask Local LLM for Feedback") and user_argument:
    with st.spinner("Re-analyzing argument..."):
        papers = search_papers(user_argument)
        try:
            summaries = format_summaries(papers)
            feedback = get_feedback(user_argument, summaries)
            st.subheader("🧠 Local LLM Feedback")
            st.markdown(feedback)
        except Exception as e:
            st.error(f"LLM Error: {e}")
