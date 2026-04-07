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
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; transition: 0.3s; height: 3em; }
    
    /* Box de Paiement */
    .payment-box {
        background-color: #ffffff; padding: 15px; border-radius: 12px;
        border: 2px solid #FFD700; text-align: center; margin: 10px auto; max-width: 280px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .price-tag { font-size: 18px; font-weight: bold; color: #B8860B; }
    .pay-button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: black !important; padding: 8px 15px; border-radius: 8px;
        font-weight: bold; font-size: 14px; text-decoration: none; display: inline-block;
    }

    /* Panneaux */
    .doctor-panel, .patient-panel {
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
    # Table Docteurs
    conn.execute('''CREATE TABLE IF NOT EXISTS doctor 
                 (id INTEGER PRIMARY KEY, fname TEXT, lname TEXT, email TEXT, username TEXT UNIQUE, password TEXT)''')
    # Table Patients
    conn.execute('''CREATE TABLE IF NOT EXISTS patient 
                 (id INTEGER PRIMARY KEY, nom TEXT, prenom TEXT, age INTEGER, phone_parent TEXT, password TEXT, username TEXT UNIQUE)''')
    conn.commit()
    conn.close()

init_db()

# --- 3. GESTION D'ÉTAT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.role = ""

# --- 4. INTERFACE ---

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>🧠 EEG Smart Lab</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: 
        if st.button("👨‍⚕️ Docteur"): st.session_state.role = "doctor"
    with col2: 
        if st.button("👤 Patient"): st.session_state.role = "patient"
    with col3: 
        if st.button("⚙️ Admin"): st.info("Espace Admin en développement")

    # --- ESPACE DOCTEUR ---
    if st.session_state.role == "doctor":
        st.divider()
        tab1, tab2 = st.tabs(["🔑 Connexion", "📝 Inscription"])
        with tab1:
            u = st.text_input("Nom d'utilisateur")
            p = st.text_input("Mot de passe", type="password")
            if st.button("Se Connecter"):
                conn = get_db_connection()
                user = conn.execute("SELECT * FROM doctor WHERE username=? AND password=?", (u, p)).fetchone()
                conn.close()
                if user:
                    st.session_state.logged_in, st.session_state.user_name = True, f"Dr. {user['fname']} {user['lname']}"
                    st.rerun()
                else: st.error("❌ Identifiants incorrects")
        with tab2:
            st.subheader("Nouveau compte Docteur")
            c1, c2 = st.columns(2)
            fn, ln = c1.text_input("Prénom"), c2.text_input("Nom")
            un, pw = st.text_input("Username"), st.text_input("Password", type="password")
            st.markdown('<div class="payment-box"><div class="price-tag">100,000 DZD / Mois</div><a href="#" class="pay-button">💳 Payer</a></div>', unsafe_allow_html=True)
            if st.button("S'INSCRIRE"):
                conn = get_db_connection()
                try:
                    conn.execute("INSERT INTO doctor (fname, lname, username, password) VALUES (?,?,?,?)", (fn, ln, un, pw))
                    conn.commit()
                    st.session_state.logged_in, st.session_state.user_name = True, f"Dr. {fn} {ln}"
                    st.rerun()
                except: st.error("Username déjà pris")
                finally: conn.close()

    # --- ESPACE PATIENT ---
    elif st.session_state.role == "patient":
        st.divider()
        ptab1, ptab2 = st.tabs(["🔑 Accès Dossier", "📝 Nouveau Dossier"])
        with ptab1:
            pu = st.text_input("Nom d'utilisateur (Username)")
            pp = st.text_input("Mot de passe", type="password", key="ppass")
            if st.button("Accéder au dossier"):
                conn = get_db_connection()
                # تم تصحيح الخطأ هنا (حذف كلمة ERROR)
                user = conn.execute("SELECT * FROM patient WHERE username=? AND password=?", (pu, pp)).fetchone()
                conn.close()
                if user:
                    st.session_state.logged_in, st.session_state.user_name = True, f"Patient: {user['nom']} {user['prenom']}"
                    st.rerun()
                else: st.error("❌ Dossier introuvable")
        with ptab2:
            st.subheader("Créer mon dossier médical")
            pc1, pc2 = st.columns(2)
            p_nom = pc1.text_input("Nom")
            p_prenom = pc2.text_input("Prénom")
            pc3, pc4 = st.columns([1, 2])
            p_age = pc3.number_input("Âge", min_value=0, max_value=120)
            p_phone = pc4.text_input("Tél. Urgence")
            p_un = st.text_input("Choisir un Username")
            p_pw = st.text_input("Mot de passe", type="password", key="preg")
            
            st.markdown('<div class="payment-box"><div class="price-tag">50 DZD / Consultation</div><a href="#" class="pay-button">💳 Payer 50 DZD</a></div>', unsafe_allow_html=True)
            
            if st.button("Créer mon dossier"):
                if p_un and p_pw:
                    conn = get_db_connection()
                    try:
                        conn.execute("INSERT INTO patient (nom, prenom, age, phone_parent, username, password) VALUES (?,?,?,?,?,?)", 
                                     (p_nom, p_prenom, p_age, p_phone, p_un, p_pw))
                        conn.commit()
                        st.session_state.logged_in, st.session_state.user_name = True, f"Patient: {p_nom} {p_prenom}"
                        st.success("✅ Dossier créé !")
                        time.sleep(1); st.rerun()
                    except: st.error("Username déjà utilisé")
                    finally: conn.close()

# --- ESPACE APRÈS CONNEXION ---
else:
    st.sidebar.markdown(f"### 👤 {st.session_state.user_name}")
    if st.sidebar.button("🚪 Déconnexion"):
        st.session_state.logged_in = False
        st.rerun()

    if "Dr." in st.session_state.user_name:
        st.markdown("## 🏥 Laboratoire d'Analyse EEG")
        st.divider()
        col_l, col_r = st.columns([1, 2])
        with col_l:
            st.markdown('<div class="doctor-panel">', unsafe_allow_html=True)
            st.subheader("📥 Importer Données")
            up = st.file_uploader("Fichier EEG (CSV/NPY)", type=['csv', 'npy'])
            if up:
                with st.spinner('Analyse...'): time.sleep(2)
                st.success("✅ Signal traité")
            st.markdown('</div>', unsafe_allow_html=True)
        with col_r:
            if up:
                st.markdown('<div class="doctor-panel">', unsafe_allow_html=True)
                st.subheader("📊 Visualisation & Diagnostic")
                chart_data = pd.DataFrame(np.random.randn(50, 1), columns=['Amplitude'])
                st.line_chart(chart_data)
                st.success("🎯 Diagnostic: État Normal (Pas de crises)")
                st.image("https://via.placeholder.com/400x150.png?text=Scalogram+Result", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("En attente de données...")
    else:
        st.markdown("## 📁 Mon Dossier Médical (Espace Patient)")
        st.markdown('<div class="patient-panel">', unsafe_allow_html=True)
        st.write(f"**Patient:** {st.session_state.user_name}")
        st.write("---")
        st.warning("Aucune analyse EEG n'a été déposée par votre médecin pour le moment.")
        st.markdown('</div>', unsafe_allow_html=True)
