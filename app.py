import streamlit as st
from paper_search import search_papers
# import openai  

# openai.api_key = st.secrets["OPENAI_API_KEY"]  

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
        combined_abstracts = "\n\n".join([p["abstract"] for p in papers])

        for i, paper in enumerate(papers, 1):
            with st.expander(f"{i}. {paper['title']}"):
                st.markdown(f"**Authors**: {paper['authors']}")
                st.markdown(f"**Abstract**: {paper['abstract']}")
                st.markdown(f"[Read More]({paper['url']})")

        # GPT section is disabled for now
        st.info("GPT summarization is disabled until OpenAI API key is added.")
