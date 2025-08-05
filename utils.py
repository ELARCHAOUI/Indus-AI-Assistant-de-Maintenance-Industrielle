# utils.py
import pandas as pd
import fitz  # PyMuPDF
import google.generativeai as genai

def load_knowledge_base(csv_path='data/history.csv'):
    """Charge l'historique des pannes depuis un fichier CSV."""
    try:
        df = pd.read_csv(csv_path,encoding='latin-1')
        # Convertit le dataframe en une chaîne de texte simple
        return df.to_string()
    except FileNotFoundError:
        return "Fichier d'historique des pannes non trouvé."

def load_technical_manual(pdf_path='data/manual.pdf'):
    """Extrait le texte d'un manuel technique en PDF."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Erreur de lecture du manuel PDF : {e}"
    
# suite de utils.py

def get_diagnosis(equipment, symptoms):
    """Génère un diagnostic en utilisant le RAG sur les documents locaux."""
    
    # 1. Retrieval (Récupération)
    knowledge_base = load_knowledge_base()
    technical_manual = load_technical_manual()

    # 2. Augmented (Augmentation) - Construction du Prompt
    prompt = f"""
    Tu es un ingénieur de maintenance senior et un expert en diagnostic.
    Ta mission est d'aider un technicien sur le terrain.

    ### CONTEXTE FOURNI ###
    Voici les informations dont tu disposes. Base TOUTE ta réponse EXCLUSIVEMENT sur ce contexte.

    1. HISTORIQUE DES PANNES PRÉCÉDENTES :
    {knowledge_base}

    2. MANUEL TECHNIQUE DE L'ÉQUIPEMENT :
    {technical_manual}
    ### FIN DU CONTEXTE ###

    ### PROBLÈME ACTUEL ###
    - Équipement concerné : {equipment}
    - Symptômes observés par le technicien : {symptoms}

    ### TA MISSION ###
    En te basant UNIQUEMENT sur le contexte fourni, fournis une réponse claire et structurée en Markdown :
    1.  **Diagnostic Probable :** Identifie la cause racine la plus probable du problème.
    2.  **Plan d'Action :** Propose une liste d'étapes claires et numérotées pour que le technicien puisse confirmer le diagnostic et réparer la panne.
    3.  **Pièces et Outils :** Liste les pièces de rechange ou les outils spécifiques mentionnés dans le contexte qui pourraient être nécessaires.
    """

    # 3. Generation (Génération)
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Une erreur est survenue avec l'API Gemini : {e}"