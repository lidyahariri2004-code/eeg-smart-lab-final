import streamlit as st
import sqlite3
import os

# 1. إعداد الصفحة وتنسيق الـ CSS (تصغير الزر وتعديل الألوان)
st.set_page_config(page_title="EEG Smart Lab", layout="centered")

st.markdown("""
    <style>
    .main-title { color: #1E3A8A; text-align: center; font-size: 28px; }
    .payment-box {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 12px;
        border: 1.5px solid #FFD700;
        text-align: center;
        margin: 10px auto;
        max-width: 300px; /* تصغير حجم الصندوق */
    }
    .price-tag {
        font-size: 20px;
        font-weight: bold;
        color: #B8860B;
    }
    .pay-button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: white !important;
        padding: 8px 20px; /* تصغير الحشوة لتصغير الزر */
        border-radius: 8px;
        font-weight: bold;
        font-size: 16px; /* تصغير الخط */
        text-decoration: none;
        display: inline-block;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. وظائف قاعدة البيانات
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

# 3. إدارة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_name = ""

# --- الواجهة الرئيسية ---
if not st.session_state.logged_in:
    st.markdown("<h1 class='main-title'>🧠 EEG Smart Lab</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👨‍⚕️ طبيب", use_container_width=True): st.session_state.temp_role = "doctor"
    with col2:
        if st.button("👤 مريض", use_container_width=True): st.session_state.temp_role = "patient"
    with col3:
        if st.button("⚙️ أدمن", use_container_width=True): st.session_state.temp_role = "admin"

    if 'temp_role' in st.session_state and st.session_state.temp_role == "doctor":
        st.divider()
        tab1, tab2 = st.tabs(["🔑 دخول", "📝 اشتراك جديد"])
        
        with tab1:
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("Se Connecter"):
                conn = get_db_connection()
                user = conn.execute("SELECT * FROM doctor WHERE username=? AND password=?", (u, p)).fetchone()
                conn.close()
                if user:
                    st.session_state.logged_in = True
                    st.session_state.role = "doctor"
                    st.session_state.user_name = user['fname']
                    st.rerun()
                else: st.error("❌ خطأ في الدخول")

        with tab2:
            st.write("### Créer un Compte")
            c1, c2 = st.columns(2)
            fname = c1.text_input("Prénom")
            lname = c2.text_input("Nom")
            email = st.text_input("Email")
            uname = st.text_input("Username", key="reg_u")
            pword = st.text_input("Password", type="password", key="reg_p")
            
            # البتون الصغير الجديد والاشتراك الشهري
            st.markdown("""
                <div class="payment-box">
                    <div class="price-tag">100,000 DZD / شهر</div>
                    <p style="font-size: 0.8em; color: #666;">خطة التحليل المتقدمة</p>
                    <a href="#" class="pay-button">💳 Payer</a>
                </div>
            """, unsafe_allow_html=True)
            
            agree = st.checkbox("أوافق على شروط الاشتراك")
            if st.button("S'INSCRIRE"):
                if agree and uname and pword:
                    try:
                        conn = get_db_connection()
                        conn.execute("INSERT INTO doctor (fname, lname, email, username, password) VALUES (?,?,?,?,?)",
                                     (fname, lname, email, uname, pword))
                        conn.commit()
                        conn.close()
                        st.success("✅ سجلتي بنجاح!")
                    except: st.error("❌ المستخدم موجود")

# --- واجهة الطبيب ---
else:
    st.sidebar.write(f"المستخدم: {st.session_state.user_name}")
    if st.sidebar.button("خروج"):
        st.session_state.logged_in = False
        st.rerun()
    st.header("👨‍⚕️ فضاء الطبيب")
    st.file_uploader("ارفع ملف EEG")
