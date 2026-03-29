from sentence_transformers import SentenceTransformer

# Charger le modèle d'embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve(collection, query, k=6, max_per_source=2, distance_threshold=1.2):
    """
    Retrieve les chunks les plus pertinents pour une question donnée.

    Args:
        collection: Chroma collection
        query (str): question utilisateur
        k (int): nombre de résultats bruts récupérés
        max_per_source (int): limite de chunks par document
        distance_threshold (float): seuil pour filtrer les résultats faibles

    Returns:
        filtered_docs (list[str])
        filtered_metas (list[dict])
    """

    # Encoder la question
    query_embedding = model.encode(query).tolist()

    # Interroger Chroma
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    # Structures de filtrage
    seen_docs = set()
    source_counts = {}
    filtered_docs = []
    filtered_metas = []

    # Filtrage intelligent
    for doc, meta, dist in zip(docs, metas, distances):
        doc_clean = doc.strip()
        source = meta.get("source", "unknown")

        
        if dist > distance_threshold:
            continue

        
        if len(doc_clean) < 30:
            continue

        
        if doc_clean in seen_docs:
            continue

        
        if source_counts.get(source, 0) >= max_per_source:
            continue

        
        seen_docs.add(doc_clean)
        source_counts[source] = source_counts.get(source, 0) + 1

        filtered_docs.append(doc_clean)
        filtered_metas.append(meta)

    return filtered_docs, filtered_metas


def build_context(docs, metas):
    """
    Construit un contexte structuré pour le LLM.
    """

    context = ""

    for i, (doc, meta) in enumerate(zip(docs, metas)):
        source = meta.get("source", "unknown")
        context += f"[Source: {source}]\n{doc}\n\n"

    return context


def is_out_of_scope(docs):
    """
    Détecte si aucune information pertinente n'a été trouvée.
    """

    if len(docs) == 0:
        return True

    
    total_length = sum(len(d) for d in docs)

    if total_length < 50:
        return True

    return False