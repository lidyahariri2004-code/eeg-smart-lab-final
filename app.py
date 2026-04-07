import streamlit as st
import sqlite3
import os

# 1. إعداد الصفحة وتنسيق الـ CSS للزر الذهبي "تاع الصوارد"
st.set_page_config(page_title="EEG Smart Lab", layout="centered")

st.markdown("""
    <style>
    .main-title { color: #1E3A8A; text-align: center; font-weight: bold; }
    .payment-box {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #FFD700;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    }
    .price-tag {
        font-size: 28px;
        font-weight: bold;
        color: #B8860B;
        margin: 10px 0;
    }
    .pay-button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: white !important;
        padding: 15px 30px;
        border-radius: 10px;
        font-weight: bold;
        font-size: 20px;
        text-decoration: none;
        display: inline-block;
        transition: 0.3s;
        border: none;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .pay-button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
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
    # إنشاء جدول الأطباء بالمعلومات المطلوبة
    conn.execute('''CREATE TABLE IF NOT EXISTS doctor 
                 (id INTEGER PRIMARY KEY, fname TEXT, lname TEXT, email TEXT, username TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# 3. إدارة الجلسة (Session)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_name = ""

# --- الواجهة الرئيسية (الأزرار الثلاثة) ---
if not st.session_state.logged_in:
    st.markdown("<h1 class='main-title'>🧠 EEG Smart Lab</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>مرحباً بك، اختر صفتك للدخول</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👨‍⚕️ طبيب (Doctor)", use_container_width=True):
            st.session_state.temp_role = "doctor"
    with col2:
        if st.button("👤 مريض (Patient)", use_container_width=True):
            st.session_state.temp_role = "patient"
    with col3:
        if st.button("⚙️ أدمن (Admin)", use_container_width=True):
            st.session_state.temp_role = "admin"

    if 'temp_role' in st.session_state:
        st.divider()
        
        if st.session_state.temp_role == "doctor":
            tab1, tab2 = st.tabs(["🔑 تسجيل الدخول", "📝 فتح حساب جديد"])
            
            with tab1:
                u = st.text_input("اسم المستخدم", key="l_u")
                p = st.text_input("كلمة المرور", type="password", key="l_p")
                if st.button("دخول"):
                    conn = get_db_connection()
                    user = conn.execute("SELECT * FROM doctor WHERE username=? AND password=?", (u, p)).fetchone()
                    conn.close()
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.role = "doctor"
                        st.session_state.user_name = f"د. {user['fname']}"
                        st.rerun()
                    else:
                        st.error("❌ تأكد من معلوماتك أو اشترك أولاً.")

            with tab2:
                st.subheader("إستمارة التسجيل والاشتراك")
                c1, c2 = st.columns(2)
                with c1: fname = st.text_input("Prénom")
                with c2: lname = st.text_input("Nom")
                email = st.text_input("Adresse Email")
                username = st.text_input("Nom d'utilisateur")
                password = st.text_input("Mot de passe", type="password")
                
                # تصميم "بُون الصوارد" الذهبي
                st.markdown("""
                    <div class="payment-box">
                        <h4 style="color: black;">💳 نظام الاشتراك السنوي</h4>
                        <p style="color: #555;">للاستفادة من ميزات الذكاء الاصطناعي لتحليل إشارات EEG</p>
                        <div class="price-tag">100,000 DZD / السنة</div>
                        <p style="font-size: 0.9em; color: #666;">(الدفع متوفر عبر بطاقة الذهبية أو CIB)</p>
                        <br>
                        <a href="#" class="pay-button">💳 اشترك الآن | S'abonner</a>
                    </div>
                """, unsafe_allow_html=True)
                
                agree = st.checkbox("أؤكد أنني قمت بعملية الدفع وأوافق على الشروط")
                
                if st.button("تأكيد التسجيل النهائي"):
                    if agree and username and password:
                        try:
                            conn = get_db_connection()
                            conn.execute("INSERT INTO doctor (fname, lname, email, username, password) VALUES (?,?,?,?,?)",
                                         (fname, lname, email, username, password))
                            conn.commit()
                            conn.close()
                            st.success("✅ تم حفظ حسابك بنجاح! يمكنك الآن الدخول من قسم Login.")
                        except:
                            st.error("❌ هذا المستخدم موجود مسبقاً.")
                    else:
                        st.warning("⚠️ يرجى إكمال البيانات والموافقة على الاشتراك.")

        else:
            st.info(f"واجهة الـ {st.session_state.temp_role} قيد الإعداد.")

# --- واجهة الطبيب بعد الدخول ---
else:
    st.sidebar.title(f"مرحباً {st.session_state.user_name}")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()
        
    if st.session_state.role == "doctor":
        st.header("👨‍⚕️ لوحة تحكم الطبيب المختص")
        st.write("يمكنك الآن البدء في تحليل إشارات الـ EEG.")
        st.file_uploader("ارفع ملف الإشارة (CSV/NPY)", type=['csv', 'npy'])
