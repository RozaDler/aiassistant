# In server/routes/user_query.py

from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from modules.llm import get_llm_chain
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from logger import logger
import os

router = APIRouter()

@router.post("/ask/")
async def ask_question(question: str = Form(...)):
    try:
        logger.info(f"User Query..:{question}")

        # --- 1. Setup embeddings and connect to Pinecone ---
        embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        # Use LangChain's PineconeVectorStore to easily create a retriever
        vectorstore = PineconeVectorStore.from_existing_index(
            index_name=os.environ.get("PINECONE_INDEX_NAME"),
            embedding=embed_model
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        # --- 2. Get relevant documents to show the sources ---
        source_documents = retriever.get_relevant_documents(question)

        # --- 3. Get the modern LCEL chain from llm.py ---
        chain = get_llm_chain(retriever)
        
        # --- 4. Invoke the chain with just the question ---
        llm_response = chain.invoke(question)

        # --- 5. Format and return the final response ---
        # Note: The metadata key might be 'source', 'file_path', etc.
        # Adjust doc.metadata.get("source", "") if your key is different.
        response_data = {
            "response": llm_response,
            "sources": [doc.metadata.get("source", "N/A") for doc in source_documents]
        }
        
        logger.info("Query was successful")
        return JSONResponse(status_code=200, content=response_data)

    except Exception as e:
        logger.exception("Error processing query")
        return JSONResponse(status_code=500, content={"error": str(e)})


# from fastapi import APIRouter, Form
# from fastapi.responses import JSONResponse
# from modules.llm import get_llm_chain
# from modules.query_handlers import query_chain
# from langchain_core.documents import Document
# from langchain.schema import BaseRetriever
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from pinecone import Pinecone
# from pydantic import Field
# from typing import List, Optional
# from logger import logger
# import os

# # Initialise router 

# router = APIRouter()

# @router.post("/ask/")
# async def ask_question(question:str=Form(...)):
#     try:
#         logger.info(f"User Query..:{question}")

#         # embed model + pinecone setup
#         pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
#         index = pc.Index(os.environ["PINECONE_INDEX_NAME"])
#         embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#         embedded_query = embed_model.embed_query(question)
#         res = index.query(vector=embedded_query,top_k=3,include_metadata=True)

#         docs = [
#             Document(
#                 page_content=match["metadata"].get("text",""),
#                 metadata=match["metadata"]
#             )for match in res["matches"]
#         ]

#         class SimpleRetriever(BaseRetriever):
#             tags: Optional[List[str]] = Field(default_factory=list)
#             metadata: Optional[dict] = Field(default_factory=dict)

#             def __init__(self, documents: List[Document]):
#                 super().__init__()
#                 self._docs = documents
            
#             def _get_relevant_documents(self, query:str) -> List[Document]:
#                 return self._docs
            
#         retriever=SimpleRetriever(docs)
#         chain=get_llm_chain(retriever)
#         result=query_chain(chain,question)

#         logger.info("Query is sucessful")
#         return result

#     except Exception as e:
#         logger.exception("Error processing query")
#         return JSONResponse(status_code=500,content={"error":str(e)})

