# Indus-AI-Assistant-de-Maintenance-Industrielle
Une application web qui sert d'assistant intelligent pour les techniciens de maintenance. Elle utilise un LLM (Google Gemini) et une architecture RAG avancée avec une base de données vectorielle (FAISS) pour diagnostiquer des pannes en se basant sur la documentation technique et l'historique des pannes.

##  Le Problème

Dans un environnement industriel, le diagnostic de pannes est une tâche complexe. La connaissance est souvent dispersée dans des manuels PDF de centaines de pages et dans l'expérience des techniciens les plus seniors. Un technicien peut perdre un temps précieux à trouver la bonne information pour résoudre un problème, ce qui entraîne des temps d'arrêt coûteux pour les machines.

##  La Solution : Indus-AI

Indus-AI est un système expert qui centralise cette connaissance et la rend accessible instantanément. Le technicien peut décrire un problème en langage naturel, visualiser des données de capteurs, et l'IA va :
1.  **Analyser** les données de capteurs pour identifier des anomalies.
2.  **Rechercher (Retrieval)** dans la documentation technique et l'historique des pannes les informations les plus pertinentes.
3.  **Raisonner (Augmented Generation)** sur ce contexte pour fournir un diagnostic précis et un plan d'action étape par étape.

### Fonctionnalités Clés
*   **Visualisation de Données :** Affiche les données de capteurs (ex: vibrations) pour une détection visuelle des anomalies.
*   **Diagnostic de Pannes :** Propose les causes probables d'une panne à partir de symptômes textuels.
*   **Plan d'Action Guidé :** Génère une procédure de réparation structurée et sécuritaire.
*   **RAG Transparent :** Permet de voir exactement quels extraits de la documentation l'IA a utilisés pour formuler sa réponse.

##  Architecture Technique

L'application utilise une architecture **Retrieval-Augmented Generation (RAG)** optimisée pour la performance et la pertinence :

`Interface Streamlit` ➔ `Requête Utilisateur` ➔ `Recherche Sémantique (FAISS)` ➔ `Contexte Augmenté (Chunks pertinents + Historique CSV)` ➔ `API Google Gemini` ➔ `Réponse Structurée`

### Stack Technique
*   **Frontend :** Streamlit
*   **Visualisation :** Plotly
*   **Modèle de Langage (LLM) :** Google Gemini 1.5 Flash
*   **Architecture RAG :**
    *   **Base de Données Vectorielle :** FAISS (Facebook AI Similarity Search)
    *   **Modèle d'Embedding :** `Sentence-Transformers`
    *   **Lecture de Documents :** PyMuPDF (PDF), Pandas (CSV)
*   **Backend & Outils :** Python, Git, Environnements virtuels
##  Améliorations Futures

*   [ ] Intégration d'une base de données vectorielle plus robuste (ex: ChromaDB, Pinecone) pour une gestion dynamique.
*   [ ] Connexion à des sources de données en temps réel pour les graphiques de capteurs.
*   [ ] Ajout de la multimodalité : permettre au technicien d'envoyer une photo de la pièce défectueuse.

##  Contact

EL ARCHAOUI - mohamedelarchaoui766@gmail.com
