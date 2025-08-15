# utils.py
import pandas as pd
import google.generativeai as genai
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

# --- CHARGEMENT DES MODÈLES ET DE LA BASE DE CONNAISSANCES---
# utils.py
print("Chargement du modèle, de l'index FAISS et des chunks...")
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    index = faiss.read_index('../data/manual.faiss') # <-- Ligne critique
    with open('../data/chunks.pkl', 'rb') as f:      # <-- Ligne critique
        chunks = pickle.load(f)
except FileNotFoundError:
    print("ERREUR: Fichiers 'manual.faiss' ou 'chunks.pkl' non trouvés.")
    print("Veuillez exécuter le script 'preprocess.py' d'abord.")
    # SI LES FICHIERS NE SONT PAS TROUVÉS, ON FAIT CECI :
    model, index, chunks = None, None, []
# ------------------------------------------------------------------------------------

def load_knowledge_base(csv_path='../data/history.csv'):
    """Charge l'historique des pannes depuis un fichier CSV."""
    try:
        return pd.read_csv(csv_path, encoding='latin-1').to_string()
    except FileNotFoundError:
        return "Fichier d'historique des pannes non trouvé."

def get_diagnosis_rag(equipment, symptoms):
    """Génère un diagnostic en utilisant le RAG optimisé avec FAISS."""
    
    # --- AJOUT D'UN CONTRÔLE DE ROBUSTESSE ---
    # On vérifie dès le début si la base de connaissances est bien chargée.
    if index is None or chunks is None or not chunks:
        error_message = (
            "ERREUR CRITIQUE: La base de connaissances (index FAISS ou chunks) n'a pas pu être chargée.\n\n"
            "Veuillez vérifier que :\n"
            "1. Le script 'preprocess.py' a été exécuté avec succès.\n"
            "2. Les fichiers 'manual.faiss' et 'chunks.pkl' se trouvent bien dans le dossier 'data/'."
        )
        # On retourne le message et une liste vide pour que l'app ne plante pas
        return error_message, []

    # --- 1. RETRIEVAL (Récupération sémantique) ---
    # Transformer la question de l'utilisateur en vecteur
    augmented_query = f"Procédure de maintenance et spécifications techniques pour : {symptoms}"
    query_embedding = model.encode([augmented_query])
    k = 5
    distances, indices = index.search(np.array(query_embedding), k)
    retrieved_chunks = [chunks[i] for i in indices[0]]
    context_from_manual = "\n---\n".join(retrieved_chunks)
    
    context_from_history = load_knowledge_base()

    # --- 2. AUGMENTED (Construction du Prompt) ---
    prompt = f"""
    Tu es un ingénieur de maintenance senior et un expert en diagnostic.
    Ta mission est d'aider un technicien sur le terrain.

    ### CONTEXTE FOURNI ###
    Base ta réponse EXCLUSIVEMENT sur ce contexte.

    1. HISTORIQUE DES PANNES PRÉCÉDENTES :
    {context_from_history}

    2. EXTRAITS PERTINENTS DU MANUEL TECHNIQUE :
    {context_from_manual}
    ### FIN DU CONTEXTE ###

    ### PROBLÈME ACTUEL ###
    - Équipement concerné : {equipment}
    - Symptômes observés par le technicien : {symptoms}

    ### TA MISSION ###
    En te basant UNIQUEMENT sur le contexte fourni, fournis une réponse claire et structurée en Markdown :
    1.  **Diagnostic Probable :** Identifie la cause racine la plus probable.
    2.  **Plan d'Action :** Propose une liste d'étapes claires et numérotées.
    3.  **Pièces et Outils :** Liste les pièces ou outils spécifiques mentionnés.
    """

    # --- 3. GENERATION (Appel à l'API Gemini) ---
    try:
        llm_model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = llm_model.generate_content(prompt)
        return response.text, retrieved_chunks
    except Exception as e:
        return f"Une erreur est survenue avec l'API Gemini : {e}", []
    