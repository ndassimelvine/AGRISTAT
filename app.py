import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. Configuration de la page
st.set_page_config(
    page_title="AgroAnalytics Europe",
    page_icon="🚜",
    layout="wide", # Utilise tout l'écran
    initial_sidebar_state="expanded"
)

# 2. Style CSS pour un look moderne
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

if st.session_state.dark_mode:
    st.markdown("""
        <style>
        .main {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            background-color: #4caf50;
            color: white;
        }
        .css-1r6slb0 { /* Style des cartes */
            border: 1px solid #333333;
            border-radius: 10px;
            padding: 20px;
            background-color: #2d2d2d;
            color: #ffffff;
        }
        .stSidebar {
            background-color: #1e1e1e;
        }
        .stTextInput, .stSelectbox, .stNumberInput, .stDateInput {
            background-color: #2d2d2d;
            color: #ffffff;
        }
        </style>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .main {
            background-color: #f5f7f9;
        }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            background-color: #2e7d32;
            color: white;
        }
        .css-1r6slb0 { /* Style des cartes */
            border: 1px solid #e6e9ef;
            border-radius: 10px;
            padding: 20px;
            background-color: white;
        }
        </style>
        """, unsafe_allow_html=True)

# 3. Barre latérale de navigation
with st.sidebar:
    st.image("https://www.flaticon.com/free-icons/agriculture", width=100) # Optionnel: un logo
    st.title("AgroAnalytics v2.0")
    menu = st.radio("Navigation", ["Tableau de Bord", "Collecte de Données", "Paramètres"])
    st.info("Utilisateur : Expert Agronome")

# --- SIMULATION DE DONNÉES (À remplacer par ta BDD) ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=['Date', 'Parcelle', 'Culture', 'Rendement', 'Qualité'])

# --- PAGE : COLLECTE DE DONNÉES ---
if menu == "Collecte de Données":
    st.header("📥 Enregistrement des Récoltes")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            with st.form("agri_form", clear_on_submit=True):
                date_saisie = st.date_input("Date de récolte", datetime.now())
                parcelle = st.text_input("Identifiant Parcelle (ex: Zone A1)")
                culture = st.selectbox("Type de Culture", ["Blé tendre", "Maïs", "Colza", "Tournesol", "Betterave"])
                rendement = st.number_input("Rendement (Quintaux/Ha)", min_value=0.0)
                qualite = st.select_slider("Qualité estimée", options=["Médiocre", "Moyenne", "Bonne", "Excellente"])
                
                submitted = st.form_submit_button("Valider la saisie")
                if submitted:
                    new_data = pd.DataFrame([[date_saisie, parcelle, culture, rendement, qualite]], 
                                            columns=['Date', 'Parcelle', 'Culture', 'Rendement', 'Qualité'])
                    st.session_state.db = pd.concat([st.session_state.db, new_data], ignore_index=True)
                    st.success("Données enregistrées avec succès !")

# --- PAGE : TABLEAU DE BORD (ANALYSE) ---
elif menu == "Tableau de Bord":
    st.header("📊 Analyse Descriptive du Secteur")
    
    # Indicateurs clés (KPIs)
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Parcelles", len(st.session_state.db))
    kpi2.metric("Rendement Moyen", f"{st.session_state.db['Rendement'].mean():.2f} q/ha" if not st.session_state.db.empty else "0")
    kpi3.metric("Culture Dominante", st.session_state.db['Culture'].mode()[0] if not st.session_state.db.empty else "N/A")

    if not st.session_state.db.empty:
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("Répartition par Culture")
            fig = px.pie(st.session_state.db, names='Culture', hole=0.4, color_discrete_sequence=px.colors.sequential.Greens_r)
            st.plotly_chart(fig, use_container_width=True)
            
        with col_chart2:
            st.subheader("Évolution des Rendements")
            fig2 = px.bar(st.session_state.db, x='Date', y='Rendement', color='Culture', barmode='group')
            st.plotly_chart(fig2, use_container_width=True)
            
        st.subheader("Détail des données")
        st.dataframe(st.session_state.db, use_container_width=True)
    else:
        st.warning("Aucune donnée disponible. Veuillez utiliser l'onglet 'Collecte de Données'.")

# --- PAGE : PARAMÈTRES ---
elif menu == "Paramètres":
    st.header("⚙️ Configuration du Système")
    
    st.subheader("🛠️ Personnalisation des cultures")
    nouvelle_culture = st.text_input("Ajouter une nouvelle culture à la liste")
    if st.button("Ajouter"):
        st.success(f"La culture '{nouvelle_culture}' a été ajoutée avec succès.")

    st.divider()
    
    st.subheader("💾 Gestion des données")
    col_reset, col_export = st.columns(2)
    
    with col_reset:
        if st.button("🗑️ Réinitialiser la base de données"):
            st.session_state.db = pd.DataFrame(columns=['Date', 'Parcelle', 'Culture', 'Rendement', 'Qualité'])
            st.warning("Toutes les données ont été supprimées.")
            
    with col_export:
        # Transformation du dataframe en CSV pour le téléchargement
        csv = st.session_state.db.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger l'export CSV",
            data=csv,
            file_name='export_agri_donnees.csv',
            mime='text/csv',
        )

    st.divider()
    st.subheader("🌙 Apparence")
    st.session_state.dark_mode = st.toggle("Activer le mode nuit", value=st.session_state.dark_mode)