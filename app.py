# app.py
import streamlit as st
import os
import google.generativeai as genai
from utils import get_diagnosis # On importe notre cerveau !

# --- Configuration de la Page et de l'API ---
st.set_page_config(page_title="Indus-AI", page_icon="🤖")
st.title("Indus-AI : Assistant de Maintenance Industrielle")
st.markdown("Décrivez une panne, l'IA analyse la documentation pour vous aider.")

try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    st.error("Clé API Google non trouvée. Veuillez la configurer.")
    st.stop()

# --- Section de Saisie Utilisateur ---
st.subheader("1. Décrivez le problème")
equipment = st.text_input(
    "Nom de l'équipement", 
    placeholder="Ex: Pompe Centrifuge P-101"
)
symptoms = st.text_area(
    "Symptômes observés ou logs d'erreur", 
    height=150,
    placeholder="Ex: Vibrations excessives et bruit de claquement..."
)

# --- Bouton de Lancement et Affichage des Résultats ---
st.subheader("2. Obtenez le diagnostic")
if st.button("Lancer le Diagnostic"):
    if equipment and symptoms:
        with st.spinner("Analyse en cours... L'IA lit la documentation..."):
            # C'est ici que l'on connecte l'interface au cerveau
            diagnosis_result = get_diagnosis(equipment, symptoms)
            
            st.subheader("3. Résultat de l'Analyse")
            st.markdown(diagnosis_result)
    else:
        st.error("Veuillez renseigner le nom de l'équipement et les symptômes.")