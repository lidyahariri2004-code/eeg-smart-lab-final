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
    
    /* تنسيق الأزرار لتكون متراصة في الموبايل */
    div[data-testid="stHorizontalBlock"] > div {
        min-width: 0px !important;
    }
    
    .stButton>button { 
        width: 100%; 
        border-radius: 10px; 
        font-weight: bold; 
        transition: 0.3; 
        height: 3.5em; 
        font-size: 13px !important; /* تصغير الخط قليلاً ليناسب عرض شاشة الهاتف */
        padding: 0px 2px;
    }
    
    .payment-box {
        background-color: #ffffff; padding: 15px; border-radius: 12px;
        border: 2px solid #FFD700; text-align: center; margin: 10px auto; max-width: 280px;
    }
    .price-tag { font-size: 18px; font-weight: bold; color: #B8860B; }
    .pay-button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: black !important; padding: 8px 15px; border-radius: 8px;
        font-weight: bold; font-size: 14px; text-decoration: none; display: inline-block;
    }

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
    conn.execute('''CREATE TABLE IF NOT EXISTS doctor 
                 (id INTEGER PRIMARY KEY, fname TEXT, lname TEXT, email TEXT, username TEXT UNIQUE, password TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS patient 
                 (id INTEGER PRIMARY KEY, nom TEXT, prenom TEXT, age INTEGER, phone_parent TEXT, password TEXT, username TEXT UNIQUE)''')
    conn.commit()
    conn.close()

init_db()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.role = ""

# --- 3. INTERFACE D'ACCÈS ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>🧠 EEG Smart Lab</h1>", unsafe_allow_html=True)
    
    # استخدام columns مع تحديد العرض لضمان بقائها بجانب بعضها
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("👨‍⚕️ Docteur"): st.session_state.role = "doctor"
    with c2: 
        if st.button("👤 Patient"): st.session_state.role = "patient"
    with c3: 
        if st.button("⚙️ Admin"): st.info("Bientôt")

    # --- LOGIQUE DOCTEUR ---
    if st.session_state.role == "doctor":
        st.divider()
        t1, t2 = st.tabs(["🔑 Connexion", "📝 Inscription"])
        with t1:
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
        with t2:
            st.subheader("Nouveau compte Docteur")
            fn = st.text_input("Prénom")
            ln = st.text_input("Nom")
            un = st.text_input("Username")
            pw = st.text_input("Password", type="password")
            st.markdown('<div class="payment-box"><div class="price-tag">100,000 DZD / Mois</div><a href="#" class="pay-button">💳 Payer</a></div>', unsafe_allow_html=True)
            if st.button("S'INSCRIRE"):
                conn = get_db_connection()
                try:
                    conn.execute("INSERT INTO doctor (fname, lname, username, password) VALUES (?,?,?,?)", (fn, ln, un, pw))
                    conn.commit()
                    st.session_state.logged_in, st.session_state.user_name = True, f"Dr. {fn} {ln}"
                    st.rerun()
                except: st.error("Username déjà utilisé")
                finally: conn.close()

    # --- LOGIQUE PATIENT ---
    elif st.session_state.role == "patient":
        st.divider()
        pt1, pt2 = st.tabs(["🔑 Accès Dossier", "📝 Nouveau Dossier"])
        with pt1:
            pu = st.text_input("Nom d'utilisateur (Patient)")
            pp = st.text_input("Mot de passe", type="password", key="p_login")
            if st.button("Ouvrir mon dossier"):
                conn = get_db_connection()
                user = conn.execute("SELECT * FROM patient WHERE username=? AND password=?", (pu, pp)).fetchone()
                conn.close()
                if user:
                    st.session_state.logged_in, st.session_state.user_name = True, f"Patient: {user['nom']} {user['prenom']}"
                    st.rerun()
                else: st.error("❌ Introuvable")
        with pt2:
            st.subheader("Création Dossier Médical")
            p_nom = st.text_input("Nom")
            p_prenom = st.text_input("Prénom")
            p_age = st.number_input("Âge", min_value=0)
            p_tel = st.text_input("Tél. Urgence")
            p_un = st.text_input("Choisir Username")
            p_pw = st.text_input("Mot de passe", type="password", key="p_reg")
            st.markdown('<div class="payment-box"><div class="price-tag">50 DZD / Consultation</div><a href="#" class="pay-button">💳 Payer 50 DZD</a></div>', unsafe_allow_html=True)
            if st.button("Créer et Payer"):
                conn = get_db_connection()
                try:
                    conn.execute("INSERT INTO patient (nom, prenom, age, phone_parent, username, password) VALUES (?,?,?,?,?,?)", (p_nom, p_prenom, p_age, p_tel, p_un, p_pw))
                    conn.commit()
                    st.session_state.logged_in, st.session_state.user_name = True, f"Patient: {p_nom} {p_prenom}"
                    st.rerun()
                except: st.error("Username déjà utilisé")
                finally: conn.close()

# --- 4. ESPACE APRÈS CONNEXION ---
else:
    st.sidebar.markdown(f"### 👤 {st.session_state.user_name}")
    if st.sidebar.button("🚪 Déconnexion"):
        st.session_state.logged_in = False
        st.rerun()

    if "Dr." in st.session_state.user_name:
        st.markdown("## 🏥 Laboratoire d'Analyse EEG")
        st.divider()
        col_l, col_r = st.columns([1, 2.5])
        with col_l:
            st.markdown('<div class="doctor-panel">', unsafe_allow_html=True)
            st.subheader("📥 Importer")
            up = st.file_uploader("Signal EEG", type=['csv', 'npy'])
            if up:
                with st.spinner('Analyse...'): time.sleep(1.5)
                st.success("✅ Prêt")
            st.markdown('</div>', unsafe_allow_html=True)
        with col_r:
            if up:
                st.markdown('<div class="doctor-panel">', unsafe_allow_html=True)
                st.line_chart(pd.DataFrame(np.random.randn(50, 1)))
                st.success("🎯 Diagnostic: État Normal")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("En attente de signal...")
    else:
        st.markdown("## 📁 Mon Dossier Médical")
        st.markdown(f'<div class="patient-panel">Bienvenue <b>{st.session_state.user_name}</b>.<br>Aucun résultat disponible.</div>', unsafe_allow_html=True)
