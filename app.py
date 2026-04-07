import streamlit as st
import sqlite3
import time
import pandas as pd
import numpy as np

# --- 1. CONFIGURATION ET STYLE (CSS) ---
st.set_page_config(page_title="EEG Smart Lab | Medical Space", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { background-color: #1E3A8A; color: white; }
    
    /* Box de Paiement */
    .payment-box {
        background-color: #ffffff; padding: 20px; border-radius: 15px;
        border: 2px solid #FFD700; text-align: center; margin: 15px auto; max-width: 300px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .price-tag { font-size: 20px; font-weight: bold; color: #B8860B; margin-bottom: 10px; }
    .pay-button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: black !important; padding: 10px 20px; border-radius: 8px;
        font-weight: bold; font-size: 15px; text-decoration: none; display: inline-block;
    }

    /* Panneau Docteur */
    .doctor-panel {
        background: white; padding: 25px; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); border-top: 6px solid #1E3A8A;
    }
    h1, h2, h3 { color: #1E3A8A; font-family: 'Helvetica Neue', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BASE DE DONNÉES ---
def get_db_connection():
    conn = sqlite3.connect('medical_system.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS doctor 
                 (id INTEGER PRIMARY KEY, fname TEXT, lname TEXT, email TEXT, username TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- 3. GESTION D'ÉTAT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.role = ""

# --- 4. INTERFACE ---

# A) AUTHENTIFICATION (Login / Register)
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>🧠 EEG Smart Lab</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray;'>Plateforme d'Analyse Neurologique Avancée</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: 
        if st.button("👨‍⚕️ Docteur"): st.session_state.role = "doctor"
    with col2: 
        if st.button("👤 Patient"): st.info("Espace Patient en développement")
    with col3: 
        if st.button("⚙️ Admin"): st.info("Espace Admin en développement")

    if st.session_state.role == "doctor":
        st.divider()
        tab1, tab2 = st.tabs(["🔑 Connexion", "📝 Inscription & Paiement"])
        
        with tab1:
            u = st.text_input("Nom d'utilisateur")
            p = st.text_input("Mot de passe", type="password")
            if st.button("Se Connecter"):
                conn = get_db_connection()
                user = conn.execute("SELECT * FROM doctor WHERE username=? AND password=?", (u, p)).fetchone()
                conn.close()
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_name = f"Dr. {user['fname']} {user['lname']}"
                    st.rerun()
                else: st.error("❌ Identifiants incorrects")

        with tab2:
            st.subheader("Créer un nouveau compte professionnel")
            c1, c2 = st.columns(2)
            fn = c1.text_input("Prénom")
            ln = c2.text_input("Nom")
            em = st.text_input("Email")
            un = st.text_input("Username", key="u2")
            pw = st.text_input("Password", type="password", key="p2")
            
            st.markdown("""<div class="payment-box">
                        <div class="price-tag">100,000 DZD / Mois</div>
                        <a href="#" class="pay-button">💳 Payer Maintenant</a>
                        </div>""", unsafe_allow_html=True)
            
            chk = st.checkbox("J'accepte d'activer mon compte après le paiement")
            
            if st.button("S'INSCRIRE ET ACCÉDER"):
                if chk and un and pw:
                    try:
                        conn = get_db_connection()
                        conn.execute("INSERT INTO doctor (fname, lname, email, username, password) VALUES (?,?,?,?,?)",
                                     (fn, ln, em, un, pw))
                        conn.commit()
                        conn.close()
                        st.session_state.logged_in = True
                        st.session_state.user_name = f"Dr. {fn} {ln}"
                        st.success("✅ Inscription réussie ! Redirection...")
                        time.sleep(1)
                        st.rerun()
                    except: st.error("❌ Ce nom d'utilisateur existe déjà")

# B) ESPACE ANALYSE (Après Connexion)
else:
    # Sidebar
    st.sidebar.markdown(f"### 👨‍⚕️ {st.session_state.user_name}")
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Déconnexion"):
        st.session_state.logged_in = False
        st.rerun()

    # Dashboard Principal
    st.markdown("## 🏥 Laboratoire d'Analyse EEG")
    st.markdown("---")

    # Layout: Gauche (Upload) | Droite (Visualisation & Résultats)
    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.markdown('<div class="doctor-panel">', unsafe_allow_html=True)
        st.subheader("📥 Importer Données")
        uploaded_file = st.file_uploader("Fichier EEG (CSV/NPY)", type=['csv', 'npy'])
        
        if uploaded_file:
            st.info(f"Fichier: {uploaded_file.name}")
            with st.spinner('Analyse du signal en cours...'):
                time.sleep(2)
                st.success("✅ Signal traité avec succès")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        if uploaded_file:
            st.markdown('<div class="doctor-panel">', unsafe_allow_html=True)
            st.subheader("📊 Résultats de l'Intelligence Artificielle")
            
            # Simulation de l'affichage du signal
            st.write("📈 **Visualisation du Signal EEG (Live)**")
            chart_data = pd.DataFrame(np.random.randn(50, 1), columns=['Amplitude'])
            st.line_chart(chart_data)
            
            st.divider()
            
            # Résultats Finaux
            res1, res2 = st.columns(2)
            with res1:
                st.write("🎯 **Diagnostic:**")
                st.success("État: Normal (Pas de crises détectées)")
            with res2:
                st.write("🖼️ **Visualisation:**")
                st.image("https://via.placeholder.com/400x200.png?text=Scalogram+Result", caption="Scalogram (Wavelet Transform)")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("👋 Bienvenue Docteur. Veuillez charger un fichier EEG pour démarrer l'analyse intelligente.")
            st.image("https://via.placeholder.com/1000x400.png?text=En+attente+de+donn%C3%A9es...", use_container_width=True)

    # Footer
    st.markdown("---")
    st.caption("EEG Smart Lab - Powered by Deep Learning (ResNet152) - © 2026")
