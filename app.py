import streamlit as st
import os
import sqlite3
import pandas as pd
from tensorflow.keras.models import load_model

# --- 1. إعداد قاعدة البيانات (SQLite) ---
def init_db():
    conn = sqlite3.connect('medical_system.db')
    c = conn.cursor()
    # جدول الأطباء
    c.execute('''CREATE TABLE IF NOT EXISTS doctor 
                 (id INTEGER PRIMARY KEY, fname TEXT, lname TEXT, username TEXT UNIQUE, password TEXT)''')
    # جدول المرضى
    c.execute('''CREATE TABLE IF NOT EXISTS patient 
                 (id INTEGER PRIMARY KEY, nom TEXT, prenom TEXT, username TEXT UNIQUE, password TEXT)''s''')
    conn.commit()
    conn.close()

init_db()

# --- 2. تحميل الموديل ---
@st.cache_resource
def get_model():
    if os.path.exists('model.keras'):
        return load_model('model.keras')
    return None

model = get_model()

# --- 3. واجهة المستخدم (Streamlit UI) ---
st.set_page_config(page_title="EEG Smart Lab Mobile", layout="centered")

# إدارة الحالة (Session State) للتحقق من تسجيل الدخول
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_name = ""

# --- صفحة تسجيل الدخول ---
if not st.session_state.logged_in:
    st.title("🧠 EEG Smart Lab")
    role = st.selectbox("تسجيل الدخول كـ:", ["طبيب (Doctor)", "مريض (Patient)", "أدمن (Admin)"])
    
    tab1, tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب جديد"])
    
    with tab1:
        user = st.text_input("اسم المستخدم")
        pw = st.text_input("كلمة المرور", type="password")
        if st.button("دخول"):
            conn = sqlite3.connect('medical_system.db')
            c = conn.cursor()
            table = "doctor" if "طبيب" in role else "patient"
            c.execute(f"SELECT * FROM {table} WHERE username=? AND password=?", (user, pw))
            result = c.fetchone()
            conn.close()
            
            if result:
                st.session_state.logged_in = True
                st.session_state.role = role
                st.session_state.user_name = user
                st.rerun()
            else:
                st.error("خطأ في اسم المستخدم أو كلمة المرور")

    with tab2:
        new_user = st.text_input("اسم مستخدم جديد")
        new_pw = st.text_input("كلمة مرور جديدة", type="password")
        if st.button("تسجيل حساب"):
            try:
                conn = sqlite3.connect('medical_system.db')
                c = conn.cursor()
                table = "doctor" if "طبيب" in role else "patient"
                c.execute(f"INSERT INTO {table} (username, password) VALUES (?,?)", (new_user, new_pw))
                conn.commit()
                conn.close()
                st.success("تم التسجيل بنجاح! يمكنك الآن تسجيل الدخول.")
            except:
                st.error("اسم المستخدم موجود مسبقاً")

# --- صفحة الداشبورد بعد الدخول ---
else:
    st.sidebar.title(f"مرحباً {st.session_state.user_name}")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

    if "طبيب" in st.session_state.role:
        st.header("👨‍⚕️ فضاء الطبيب")
        uploaded_file = st.file_uploader("ارفع ملف EEG (CSV)", type="csv")
        if uploaded_file:
            st.info("جاري المعالجة...")
            # هنا تحطي كود الـ Prediction تاعك
