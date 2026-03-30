#  ShopVite RAG Assistant

Assistant FAQ intelligent basé sur un pipeline RAG (Retrieval-Augmented
Generation) pour répondre aux questions clients à partir de documents
e-commerce (retour, livraison, garantie, produits).

------------------------------------------------------------------------

# Architecture du pipeline

User Question 
↓ 
FastAPI (/ask)
↓
Retriever (Chroma + Embeddings)
↓
Top-K Chunks
↓
Context Builder
↓ 
LLM (OpenAI)
↓ 
Answer + Sources + Confidence

------------------------------------------------------------------------

#  Pipeline détaillé

## 1. Ingestion des données

-   Formats : TXT, PDF, JSON
-   Nettoyage du texte
-   JSON → 1 document par produit

## 2. Chunking

-   Découpage intelligent 
-   Basé sur paragraphes

## 3. Embeddings

-   Modèle : all-MiniLM-L6-v2
-   Stockage : ChromaDB

## 4. Retrieval

-   Recherche sémantique
-   Filtrage par distance
-   Suppression doublons

## 5. Génération

-   Modèle : GPT-4o-mini
-   Prompt strict anti-hallucination

## 6. API

-   /health → statut
-   /ask → question

## 7. Interface

-   Streamlit

------------------------------------------------------------------------
 # Quick Start
 ## 1. Lancement en local
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
Configuration

## 2. Créer un fichier .env :

OPENAI_API_KEY=your_api_key_here
Lancer l’API
uvicorn src.main:app --reload
Lancer l’interface
streamlit run app.py
Accès
API docs : http://localhost:8000/docs
Interface : http://localhost:8501



------------------------------------------------------------------------

#  Choix techniques

-   SentenceTransformers : rapide et léger
-   ChromaDB : simple et local
-   FastAPI : performant
-   Streamlit : interface rapide


------------------------------------------------------------------------

#  Exemples

## Question valide

Quelle est la durée de retour ?

Réponse attendue : 30 jours calendaires

## Question produit

Quel est le prix du Smartphone X100 ?

Réponse : 699€

## Hors-scope

Quelle est la capitale du Japon ?

Réponse : Je ne peux pas répondre...

------------------------------------------------------------------------

#  Fonctionnalités

-   RAG complet
-   Multi-format
-   Anti-hallucination
-   Sources + confidence
-   Interface utilisateur

------------------------------------------------------------------------

