# ArguMint: AI-Powered Argument Evaluation Tool

ArguMint is an interactive, AI-powered assistant that analyzes user-submitted arguments using research papers from Semantic Scholar and provides structured, critical feedback using a local LLM. Designed as a browser-based app with Streamlit, ArguMint helps users strengthen their reasoning by grounding claims in actual research.

---

## Features

-  **Semantic Scholar Integration**: Fetches the top relevant research papers for any argument.
-  **Abstract Summarization**: Displays authors, abstracts, and links to full papers.
-  **Local LLM Reasoning**: Uses a quantized local model (via `llama.cpp`) to evaluate the argument.
-  **Structured Feedback**: Offers verdict (True/False/Partially True), reasoning, and suggestions.
-  **Streamlit UI**: Clean, interactive web interface.

---

## Use Case

Ideal for:
- Researchers validating hypotheses
- Students preparing essays or debates
- Developers exploring LLMs for reasoning tasks
- Anyone seeking evidence-based evaluation of ideas

---

## How It Works

1. **Input Argument**: User enters a short argument or claim.
2. **Search**: ArguMint retrieves top research papers using `search_papers()` with Semantic Scholar's API.
3. **Model Feedback**: A local LLM (like `tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf` via `llama.cpp`) analyzes the argument in context of the abstracts.
4. **Display Results**:
   - Relevant papers with titles, abstracts, and authors.
   - Critical feedback with reasoning and suggestions.

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ArguMint.git
cd ArguMint
```

### 2. Clone the Repository
```bash
python3 -m venv env_name
source env_name/bin/activate  # On Windows: .\env_name\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download GGUF Model
Pick a lightweight model suitable for CPU (I have TinyLlama 1.1) from TheBloke GGUF Models or community repos. 
Place the downloaded .gguf file in your project folder.

### 5. Run the app
```bash
streamlit run app.py
```

### Developed by Jasvin Kaur
Let’s connect on [LinkedIN](https://www.linkedin.com/in/jasvin-kaur/)
