#  Reflection — ShopVite RAG Assistant

## Prompt Engineering

Le prompt a été conçu pour être strict et limiter les hallucinations du modèle.  
J’ai explicitement demandé au modèle de répondre uniquement à partir du contexte fourni et de ne pas inventer d’informations.  
Des règles simples ont été ajoutées : répondre en français, citer les sources et refuser si l’information est absente.  
J’ai également structuré le contexte avec les sources pour améliorer la compréhension du modèle.  
Enfin, le prompt encourage l’utilisation d’informations partielles lorsque cela est pertinent, afin d’éviter des refus inutiles.

---

##  Améliorations possibles

Avec plus de temps, j’améliorerais le système de retrieval en ajoutant un reranking des résultats pour améliorer la pertinence.  
Je pourrais aussi utiliser des embeddings plus performants ou un modèle hybride (BM25 + embeddings).  
L’ajout d’un cache pour les requêtes fréquentes permettrait d’optimiser les performances.    
Enfin, une meilleure interface utilisateur avec historique des conversations améliorerait l’expérience utilisateur.

---

##  Limites actuelles

Une des principales limites est la dépendance au retrieval : si les bons chunks ne sont pas récupérés, la réponse sera incorrecte ou absente.  
Le système reste sensible à la formulation des questions utilisateur.  
De plus, il n’y a pas de reranking avancé ni de compréhension fine du contexte global du corpus.  
Enfin, le système ne gère pas encore les conversations multi-turns (pas de mémoire).