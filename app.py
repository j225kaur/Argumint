import streamlit as st
from paper_search import search_papers 
from llama_cpp import Llama

# Load the GGUF model
llm = Llama.from_pretrained(
    repo_id="TheBloke/phi-2-GGUF",
    filename="phi-2.Q2_K.gguf",
)

# Summarize abstract with fallback
def summarize_abstract(abstract, max_chars=600):
    try:
        prompt = f"Summarize the following research abstract in 2 sentences:\n\n{abstract}"
        result = llm(prompt, max_tokens=100, echo=False)
        return result["choices"][0]["text"].strip()
    except Exception:
        return abstract[:max_chars] + "..."

# Generate feedback using summarized abstracts
def get_feedback(argument, abstract_summaries):
    summaries = "\n".join(f"- {s}" for s in abstract_summaries)
    prompt = f"""
Evaluate this argument based on the research summaries.

Argument:
\"\"\"{argument}\"\"\"

Research Summaries:
{summaries}

Answer the following:
1. Is the argument true? (Yes / No / Partially)
2. Why or why not? (2 bullet points)
"""
    output = llm(prompt, max_tokens=512, echo=False)
    return output["choices"][0]["text"].strip()


# Streamlit UI setup
st.set_page_config(page_title="ArguMint", layout="wide")
st.title("🧠 ArguMint: AI-Powered Argument Assistant")

user_argument = st.text_area("Enter your argument:", height=150)

# Find relevant papers and generate feedback
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

        with st.spinner("Summarizing research..."):
            try:
                top_abstracts = [p["abstract"] for p in papers[:3]]
                summarized_abstracts = [summarize_abstract(a) for a in top_abstracts]

                feedback = get_feedback(user_argument, summarized_abstracts)
                st.subheader("🧠 Local LLM Feedback")
                st.markdown(feedback)
            except Exception as e:
                st.error(f"Error running local LLM: {e}")

# Manual feedback button
if st.button("Ask Local LLM for Feedback") and user_argument:
    with st.spinner("Analyzing your argument..."):
        papers = search_papers(user_argument)
        try:
            top_abstracts = [p["abstract"] for p in papers[:3]]
            summarized_abstracts = [summarize_abstract(a) for a in top_abstracts]

            feedback = get_feedback(user_argument, summarized_abstracts)
            st.subheader("🧠 Local LLM Feedback")
            st.markdown(feedback)
        except Exception as e:
            st.error(f"Error running local LLM: {e}")
