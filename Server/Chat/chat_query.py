import os
import asyncio
import time
import re
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACEHUB_API_TOKEN")

os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACE_API_KEY

pc = Pinecone(api_key=PINECONE_API_KEY)
spec = ServerlessSpec(cloud="aws", region=PINECONE_ENV)
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

embed_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

llm = ChatGroq(
    temperature=0.3,
    model_name="openai/gpt-oss-20b",
    groq_api_key=GROQ_API_KEY
)

prompt = PromptTemplate.from_template("""
You are a helpful healthcare assistant. Answer the following question
based only on the provided context and based on medical field only.

Question: {question}

Context: {context}

Include the document source if relevant in your answer.
""")

rag_chain = prompt | llm

async def answer_query(query: str, user_role: str):
    embedding = await asyncio.to_thread(embed_model.embed_query, query)
    results = await asyncio.to_thread(
        index.query,
        vector=embedding,
        top_k=3,
        include_metadata=True
    )

    filtered_contexts = []
    sources = set()

    for match in results["matches"]:
        metadata = match.get("metadata", {})
        if metadata.get("role") == user_role:
            filtered_contexts.append(metadata.get("text", ""))
            sources.add(metadata.get("source"))

    if not filtered_contexts:
        return {"answer": "No relevant information found.", "sources": []}

    docs_text = "\n".join(filtered_contexts)
    final_answer = await asyncio.to_thread(
        rag_chain.invoke, {"question": query, "context": docs_text}
    )

    clean_answer = re.sub(r'(\*{1,2}|`+|\|)', '', final_answer.content)
    clean_answer = re.sub(r'\n{2,}', '\n\n', clean_answer)
    clean_answer = re.sub(r'\n', ' ', clean_answer)
    clean_answer = re.sub(r'\s{2,}', ' ', clean_answer).strip()
    return {
        "answer": clean_answer,
        "sources": list(sources)
    }

if __name__ == "__main__":
    async def test():
        res = await answer_query("What is COVID-19?", user_role="doctor")
        print(res)

    asyncio.run(test())
