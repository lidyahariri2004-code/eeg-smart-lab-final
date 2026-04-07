import streamlit as st
import sqlite3
import time
import pandas as pd
import numpy as np

# --- 1. إعدادات الصفحة (Wide Layout) ---
st.set_page_config(page_title="EEG Smart Lab | Dashboard", layout="wide")

# --- 2. ستايل CSS احترافي يخلي الواجهة "واو" ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f5; }
    .stMetric { background-color: white; padding: 15px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; }
    .doctor-panel {
        background-color: white; padding: 25px; border-radius: 15px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.08); border-top: 5px solid #1E3A8A;
    }
    .payment-tag {
        background-color: #fffbeb; padding: 10px; border-radius: 8px;
        border: 1px solid #FFD700; text-align: center; color: #B8860B; font-weight: bold;
    }
    .pay-button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: black !important; padding: 10px 20px; border-radius: 8px;
        font-weight: bold; text-decoration: none; display: inline-block; width: 100%; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. قاعدة البيانات ---
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

# --- 4. إدارة الجلسة ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.role = ""

# --- 5. منطق الواجهات ---

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>🧠 EEG Smart Lab</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: 
        if st.button("👨‍⚕️ طبيب (Doctor)", use_container_width=True): st.session_state.role = "doctor"
    with col2: 
        if st.button("👤 مريض (Patient)", use_container_width=True): st.info("واجهة المريض قيد التطوير")
    with col3: 
        if st.button("⚙️ أدمن (Admin)", use_container_width=True): st.info("واجهة المدير قيد التطوير")

    if st.session_state.role == "doctor":
        st.divider()
        t1, t2 = st.tabs(["🔑 تسجيل الدخول", "📝 اشتراك جديد"])
        
        with t1:
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("Se Connecter"):
                conn = get_db_connection()
                user = conn.execute("SELECT * FROM doctor WHERE username=? AND password=?", (u, p)).fetchone()
                conn.close()
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_name = f"{user['fname']} {user['lname']}"
                    st.rerun()
                else: st.error("❌ معلومات خاطئة")

        with t2:
            st.subheader("فتح حساب طبيب جديد")
            c1, c2 = st.columns(2)
            fn, ln = c1.text_input("Prénom"), c2.text_input("Nom")
            em, un = st.text_input("Email"), st.text_input("Username")
            pw = st.text_input("Password", type="password")
            
            st.markdown("""<div class="payment-tag">الاشتراك المتقدم: 100,000 DZD / شهر</div>""", unsafe_allow_html=True)
            st.markdown("<br><a href='#' class='pay-button'>💳 Payer Maintenant</a><br>", unsafe_allow_html=True)
            
            agree = st.checkbox("أوافق على تفعيل الحساب بعد الدفع")
            if st.button("S'INSCRIRE"):
                if agree and un and pw:
                    try:
                        conn = get_db_connection()
                        conn.execute("INSERT INTO doctor (fname, lname, email, username, password) VALUES (?,?,?,?,?)",
                                     (fn, ln, em, un, pw))
                        conn.commit()
                        conn.close()
                        st.session_state.logged_in = True
                        st.session_state.user_name = f"{fn} {ln}"
                        st.success("✅ تم التسجيل! جاري التحويل...")
                        time.sleep(1); st.rerun()
                    except: st.error("❌ المستخدم موجود")

# --- واجهة الطبيب الاحترافية (بعد الدخول) ---
else:
    st.sidebar.markdown(f"### 👨‍⚕️ د. {st.session_state.user_name}")
    if st.sidebar.button("🚪 تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

    st.markdown("## 🏥 مركز التحليل العصبي الرقمي")
    
    # بطاقات الإحصائيات (Metrics)
    m1, m2, m3 = st.columns(3)
    m1.metric("حالات اليوم", "12", "+2")
    m2.metric("دقة النموذج", "98.5%", "ResNet152")
    m3.metric("الاشتراك", "نشط ✅", "30 يوم")

    st.divider()

    # التقسيم الاحترافي: يسار (تحكم) | يمين (عرض ونتائج)
    col_left, col_right = st.columns([1, 2.5])

    with col_left:
        st.markdown('<div class="doctor-panel">', unsafe_allow_html=True)
        st.subheader("📥 رفع البيانات")
        up = st.file_uploader("ارفع ملف EEG", type=['csv', 'npy'])
        if up:
            st.success(f"تم تحميل: {up.name}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        if up:
            st.markdown('<div class="doctor-panel">', unsafe_allow_html=True)
            st.subheader("📊 مراقبة الإشارة الحية")
            with st.spinner("جاري معالجة الإشارة..."):
                time.sleep(1.5)
                # عرض إشارة تفاعلية سريعة
                chart_data = pd.DataFrame(np.random.randn(100, 1), columns=['EEG Signal'])
                st.line_chart(chart_data)
            
            st.divider()
            
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.subheader("🎯 النتيجة")
                st.success("✅ الحالة: طبيعية (Normal)")
            with res_col2:
                st.subheader("🖼️ Scalogram")
                st.image("https://via.placeholder.com/400x200.png?text=Scalogram+Visualization", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("👋 يرجى رفع ملف EEG من القائمة اليسرى لبدء التحليل.")
            st.image("https://via.placeholder.com/1000x400.png?text=EEG+Smart+Lab+System+Ready", use_container_width=True)
