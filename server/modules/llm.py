from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")

def get_llm_chain(retriever):
    llm = ChatGroq(
        groq_api_key = GROQ_API_KEY,
        model_name = 'llama3-70b-8192'
    )

    prompt = PromptTemplate(
        input_variables = ["context", "query"],
        template = """
        You are **ResearchBot**, an AI-powered assistant trained
        to help users understand scientific research
        documents and scientific research paper related questions.

        Your job is to provide clear, accurate, and helpful responses based **only on the provided context**

        ---

        **Context**:
        {context}
        
        ----
        **User Query**
        {query}

        ---
        **Answer**:
        - Respond in a calm, factual, and respectful tone.
        - Use Simple and high level explanations when needed.
        - If the context does not contain the answer, say: "I'm sorry, but I couldn't find relevant information 
        in the provided documents."
        - Do NOT make up facts.
        - Do NOT give medical advice or diagnoses.
        """

    )
    return RetrievalQA.from_chain_type(
        llm = llm,
        chain_type ="stuff",
        retriever = retriever,
        chain_type_kwargs = {"prompt":prompt},
        return_source_documents = True
    )

    