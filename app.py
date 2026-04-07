import streamlit as st
import sqlite3
import os

# --- إعداد الصفحة ---
st.set_page_config(page_title="EEG Smart Lab", layout="centered")

# --- دالة التعامل مع قاعدة البيانات ---
def get_db_connection():
    conn = sqlite3.connect('medical_system.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # جدول الأطباء فيه كامل المعلومات تاع الفورم تاعك
    conn.execute('''CREATE TABLE IF NOT EXISTS doctor 
                 (id INTEGER PRIMARY KEY, fname TEXT, lname TEXT, email TEXT, username TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- إدارة حالة الدخول ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_name = ""

# --- الواجهة الرئيسية ---
if not st.session_state.logged_in:
    st.title("🧠 EEG Smart Lab")
    st.markdown("### اختر صفتك للدخول")
    
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
        
        # إذا اختار طبيب، نظهر له خيارين (دخول أو تسجيل)
        if st.session_state.temp_role == "doctor":
            tab1, tab2 = st.tabs(["تسجيل الدخول (Login)", "إنشاء حساب جديد (Register)"])
            
            with tab1:
                u = st.text_input("Username", key="login_u")
                p = st.text_input("Password", type="password", key="login_p")
                if st.button("دخول"):
                    conn = get_db_connection()
                    user = conn.execute("SELECT * FROM doctor WHERE username=? AND password=?", (u, p)).fetchone()
                    conn.close()
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.role = "doctor"
                        st.session_state.user_name = f"{user['fname']} {user['lname']}"
                        st.rerun()
                    else:
                        st.error("❌ معلومات خاطئة")

            with tab2:
                st.subheader("📝 استمارة التسجيل")
                # تطبيق الفورم اللي بعثتيها
                c1, c2 = st.columns(2)
                with c1: fname = st.text_input("Prénom")
                with c2: lname = st.text_input("Nom")
                email = st.text_input("Adresse Email")
                username = st.text_input("Nom d'utilisateur")
                password = st.text_input("Mot de passe", type="password")
                
                st.divider()
                # إضافة جزء الاشتراك
                st.info("💳 **خطة الاشتراك الاحترافية**")
                st.write("للحصول على الخدمة، يرجى دفع مبلغ: **100,000 DZD / سنة**")
                agree = st.checkbox("أوافق على الاشتراك والدفع لاحقاً")
                
                if st.button("S'INSCRIRE MAINTENANT"):
                    if agree and username and password:
                        try:
                            conn = get_db_connection()
                            conn.execute("INSERT INTO doctor (fname, lname, email, username, password) VALUES (?,?,?,?,?)",
                                         (fname, lname, email, username, password))
                            conn.commit()
                            conn.close()
                            st.success("✅ تم التسجيل بنجاح! يمكنك الآن تسجيل الدخول.")
                        except:
                            st.error("❌ اسم المستخدم موجود مسبقاً")
                    else:
                        st.warning("⚠️ يرجى ملء كل الخانات والموافقة على الاشتراك")

        # هنا تقدري تزيدي نفس المنطق للمريض والأدمن إذا حبيتي
        else:
            st.info(f"واجهة الـ {st.session_state.temp_role} قيد التطوير")

# --- الواجهة بعد الدخول ---
else:
    st.sidebar.title(f"أهلاً {st.session_state.user_name}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
        
    if st.session_state.role == "doctor":
        st.header("👨‍⚕️ فضاء الطبيب")
        st.file_uploader("ارفع ملف الإشارة لتحليلها")
