def chunk_text(text, chunk_size=500):
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(paragraph) > chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""

            start = 0
            while start < len(paragraph):
                end = start + chunk_size
                chunks.append(paragraph[start:end].strip())
                start = end
            continue

        if len(current_chunk) + len(paragraph) + 1 <= chunk_size:
            current_chunk += paragraph + "\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n"

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def chunk_documents(documents):
    all_chunks = []

    for doc_id, doc in enumerate(documents):
        chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "id": f"{doc_id}_{i}",
                "text": chunk,
                "source": doc["source"],
                "chunk_index": i
            })

    return all_chunks