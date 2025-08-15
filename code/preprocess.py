# preprocess.py

import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os

print("Démarrage du pré-traitement...")

# --- 1. Charger et découper le document en 'chunks' ---
PDF_PATH = '../data/manual.pdf'
doc = fitz.open(PDF_PATH)
chunks = []
for page_num, page in enumerate(doc):
    # Extraire le texte de la page
    text = page.get_text("text")
    # Découper le texte en paragraphes (un double saut de ligne est un bon séparateur)
    paragraphs = text.split('\n\n')
    for para in paragraphs:
        # On ne garde que les paragraphes avec un contenu significatif
        if len(para.strip()) > 50:
            chunks.append(para.strip().replace('\n', ' '))

print(f"Document '{PDF_PATH}' découpé en {len(chunks)} morceaux (chunks).")

# --- 2. Créer les 'embeddings' (vecteurs numériques) ---
# Ce modèle est excellent pour la recherche sémantique en plusieurs langues
print("Chargement du modèle SentenceTransformer...")
model = SentenceTransformer('all-MiniLM-L6-v2')

print("Création des embeddings pour chaque chunk... (cela peut prendre un moment)")
embeddings = model.encode(chunks, show_progress_bar=True)
print("Embeddings créés avec succès.")

# --- 3. Créer et peupler l'index FAISS ---
dimension = embeddings.shape[1]  # Dimension des vecteurs
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

print(f"Index FAISS créé avec {index.ntotal} vecteurs.")

# --- 4. Sauvegarder l'index et les chunks pour une utilisation future ---
if not os.path.exists('../data'):
    os.makedirs('../data')

faiss.write_index(index, '../data/manual.faiss')
with open('../data/chunks.pkl', 'wb') as f:
    pickle.dump(chunks, f)

print("Index FAISS ('manual.faiss') et chunks ('chunks.pkl') sauvegardés dans le dossier 'data/'.")
print("Pré-traitement terminé !")