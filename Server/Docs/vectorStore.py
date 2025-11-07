import asyncio
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")


os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN
os.environ["HF_USE_API"] = "TRUE"


UPLOAD_DIR = "./uploaded_Docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


pc = Pinecone(api_key=PINECONE_API_KEY)
spec = ServerlessSpec(cloud='aws', region=PINECONE_ENV)

existing_index = [i["name"] for i in pc.list_indexes()]

if PINECONE_INDEX_NAME not in existing_index:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=768,
        metric="dotproduct",
        spec=spec
    )
 
    while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
        time.sleep(1)

index = pc.Index(PINECONE_INDEX_NAME)


async def load_vectorstore(uploaded_files, role: str, doc_id: str):
    """
    Process PDF files, split into chunks, embed using Hugging Face API embeddings,
    and upsert into Pinecone.
    """
   
    embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    for file in uploaded_files:
       
        save_path = Path(UPLOAD_DIR) / file.filename
        with open(save_path, "wb") as f:
            f.write(file.file.read())

    
        loader = PyPDFLoader(str(save_path))
        documents = loader.load()

       
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(documents)

        texts = [chunk.page_content for chunk in chunks]
        ids = [f"{doc_id}-{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "source": file.filename,
                "doc_id": doc_id,
                "role": role,
                "page": chunk.metadata.get("page", 0),
                "text": chunk.page_content  
            }
            for i, chunk in enumerate(chunks)
        ]

    
        embeddings = await asyncio.to_thread(embed_model.embed_documents, texts)

     
        with tqdm(total=len(embeddings), desc=f"Upserting {file.filename} to Pinecone") as progress:
            index.upsert(vectors=zip(ids, embeddings, metadatas))
            progress.update(len(embeddings))

