from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_vectorstore(chunks):
    client = chromadb.Client()
    collection = client.create_collection(name="shopvite")

    for chunk in chunks:
        embedding = model.encode(chunk["text"]).tolist()

        collection.add(
            documents=[chunk["text"]],
            metadatas=[{
                "source": chunk["source"],
                "chunk_index": chunk["chunk_index"]
            }],
            ids=[chunk["id"]],
            embeddings=[embedding]
        )

    return collection