import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

# set all env variables 
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
PINECONE_ENV="us-east-1"
PINECONE_INDEX_NAME="airesearchindex"

os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY

# store users uplaoded docs
UPLOAD_DIR="./uploaded_docs"
os.makedirs(UPLOAD_DIR,exist_ok=True)

# initialise pinecone instance
pc = Pinecone(api_key=PINECONE_API_KEY)
spec = ServerlessSpec(cloud="aws", region=PINECONE_ENV)
existing_indexes = [i["name"] for i in pc.list_indexes()]

if PINECONE_INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=768, #dimension must match embedding models 
        metric="dotproduct",
        spec=spec

    )
    # if the index is not created yet, give it some time
    while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
        time.sleep(1)

index = pc.Index(PINECONE_INDEX_NAME)

# function to load, split, embed, and upsert pdf docs contents

def load_vectorstore(uploaded_files):
    embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    file_paths = []

    # 1. first step is upload the files
    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR)/file.filename
        with open(save_path,"wb") as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))

    # 2. Split
    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.split_documents(documents)

        texts = [chunk.page_content for chunk in chunks]
        metadata = [chunk.metadata for chunk in chunks]
        ids = [f"{Path(file_path).stem}-{i}]" for i in range(len(chunks))]

        # 3 Embedding
        print(f"Embedding chunks")
        embedding = embed_model.embed_documents(texts)

        # 4 Upsert
        print("upserting embeddings ...")
        with tqdm(total=len(embedding), desc="Upserting to Pinecone") as progress:
            index.upsert(vectors=zip(ids,embedding,metadata))
            progress.update(len(embedding))

        print(f"Upload complete for {file_path}")



