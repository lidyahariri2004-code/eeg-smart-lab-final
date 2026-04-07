import streamlit as st
import os
import sqlite3
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

# --- إعداد قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('medical_system.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS doctor (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)')
    conn.commit()
    conn.close()

init_db()

# --- تحميل الموديل ---
@st.cache_resource
def load_my_model():
    if os.path.exists('model.keras'):
        return load_model('model.keras')
    return None

model = load_my_model()

# --- واجهة المستخدم ---
st.title("🧠 EEG Smart Lab")

if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("القائمة", menu)
    
    user = st.text_input("اسم المستخدم")
    pw = st.text_input("كلمة المرور", type='password')
    
    if choice == "Register":
        if st.button("إنشاء حساب"):
            conn = sqlite3.connect('medical_system.db')
            c = conn.cursor()
            try:
                c.execute('INSERT INTO doctor (username, password) VALUES (?,?)', (user, pw))
                conn.commit()
                st.success("تم التسجيل! روح لـ Login")
            except:
                st.error("المستخدم موجود")
            conn.close()
            
    else:
        if st.button("دخول"):
            conn = sqlite3.connect('medical_system.db')
            c = conn.cursor()
            c.execute('SELECT * FROM doctor WHERE username=? AND password=?', (user, pw))
            if c.fetchone():
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("معلومات غلط")
            conn.close()

else:
    st.sidebar.success(f"مرحباً بك")
    if st.sidebar.button("خروج"):
        st.session_state.auth = False
        st.rerun()
    
    st.header("👨‍⚕️ فضاء الطبيب")
    file = st.file_uploader("ارفع ملف الـ EEG", type=['csv'])
    if file:
        st.write("جاري التحليل...")
        # هنا زيدي الـ logic تاع الـ scalogram اللي كان عندك
