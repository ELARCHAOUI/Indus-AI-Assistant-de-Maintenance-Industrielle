# app.py
import streamlit as st
import os
import google.generativeai as genai
from utils import get_diagnosis_rag 

import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_diagnosis_rag
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
# --- NOUVELLE SECTION : Visualisation des Données ---
st.subheader("Analyse des Données de Capteurs")

# Ligne de chargement
df_sensors = pd.read_csv('../data/sensor_data.csv', on_bad_lines='warn')

# --- AJOUTEZ CETTE LIGNE DE DÉBOGAGE ---
#st.write("Colonnes lues par Pandas :", df_sensors.columns)
# -----------------------------------------

# La ligne qui plante (pour l'instant)
df_sensors['timestamp'] = pd.to_datetime(df_sensors['timestamp'])

fig = px.line(
    df_sensors, 
    x='timestamp', 
    y='vibration_level', 
    title='Niveau de Vibration de la Pompe P-101',
    markers=True
)
# Ajoute une ligne pour le seuil d'alerte
fig.add_hline(y=1.0, line_dash="dot", line_color="red", annotation_text="Seuil d'alerte")
st.plotly_chart(fig, use_container_width=True)

# --- Section de Saisie Utilisateur  ---
st.subheader("Diagnostic de la Panne")
equipment = st.text_input("Nom de l'équipement", value="Pompe P-101")
symptoms = st.text_area(
    "Symptômes observés",
    value="Vibrations excessives détectées sur le graphique ci-dessus.",
    height=100
)
# --- Bouton de Lancement et Affichage des Résultats ---
st.subheader("2. Obtenez le diagnostic")


if st.button("Lancer le Diagnostic"):
    if equipment and symptoms:
        with st.spinner("Analyse en cours... L'IA cherche dans la base de connaissances..."):
            # MODIFICATION : On récupère maintenant deux valeurs
            diagnosis_result, retrieved_chunks = get_diagnosis_rag(equipment, symptoms)
            
            st.subheader("3. Résultat de l'Analyse")
            st.markdown(diagnosis_result)
            
            # --- C'EST LA PARTIE MAGIQUE ---
            # On affiche les sources que l'IA a utilisées, dans un menu déroulant
            with st.expander("Voir les sources utilisées par l'IA (Contexte RAG)"):
                st.info(f"L'IA a basé sa réponse sur les {len(retrieved_chunks)} extraits les plus pertinents du manuel :")
                for i, chunk in enumerate(retrieved_chunks):
                    st.write(f"**Source {i+1}:**")
                    st.write(f"> {chunk}")
        # ------------------------------------
    else:
        st.error("Veuillez renseigner le nom de l'équipement et les symptômes.")