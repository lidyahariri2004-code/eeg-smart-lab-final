import streamlit as st
import sqlite3
import os

# 1. إعداد الصفحة وتنسيقها
st.set_page_config(page_title="EEG Smart Lab", layout="centered")

# 2. دالة التعامل مع قاعدة البيانات
def check_user(username, password, table):
    conn = sqlite3.connect('medical_system.db')
    c = conn.cursor()
    # التحقق إذا كان المستخدم موجود في الجدول المختار (doctor أو patient)
    query = f"SELECT * FROM {table} WHERE username=? AND password=?"
    c.execute(query, (username, password))
    data = c.fetchone()
    conn.close()
    return data

# 3. إدارة حالة الدخول (Session State)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.user_name = ""

# --- الواجهة الرئيسية ---
if not st.session_state.logged_in:
    st.title("🧠 EEG Smart Lab")
    st.markdown("### مرحباً بك، اختر صفتك للدخول:")
    
    # الأزرار الثلاثة اللي حبيتيهم
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

    # إذا ضغط على واحد من الأزرار، تظهر خانات الـ Login
    if 'temp_role' in st.session_state:
        st.divider()
        st.subheader(f"تسجيل الدخول كـ {st.session_state.temp_role}")
        user = st.text_input("اسم المستخدم (Username)")
        pw = st.text_input("كلمة المرور (Password)", type="password")
        
        if st.button("دخول"):
            # الأدمن عنده دخول خاص (تقدري تبدليه)
            if st.session_state.temp_role == "admin" and user == "admin" and pw == "123":
                st.session_state.logged_in = True
                st.session_state.user_role = "admin"
                st.rerun()
            
            # الطبيب والمريض نتحقق من قاعدة البيانات
            elif st.session_state.temp_role in ["doctor", "patient"]:
                result = check_user(user, pw, st.session_state.temp_role)
                if result:
                    st.session_state.logged_in = True
                    st.session_state.user_role = st.session_state.temp_role
                    st.session_state.user_name = user
                    st.rerun()
                else:
                    st.error("❌ عذراً، اسم المستخدم أو كلمة المرور غير موجودة في قاعدة البيانات.")

# --- الواجهة بعد الدخول ---
else:
    st.sidebar.success(f"متصل كـ: {st.session_state.user_role}")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.temp_role = None
        st.rerun()

    if st.session_state.user_role == "doctor":
        st.header("👨‍⚕️ لوحة تحكم الطبيب")
        st.write(f"أهلاً دكتور {st.session_state.user_name}")
        file = st.file_uploader("ارفع ملف EEG لتحليله", type=['csv'])
        if file:
            st.success("تم رفع الملف، النظام جاهز للتحليل.")

    elif st.session_state.user_role == "patient":
        st.header("👤 فضاء المريض")
        st.write("هنا يمكنك الاطلاع على نتائجك.")

    elif st.session_state.user_role == "admin":
        st.header("⚙️ لوحة التحكم (Admin)")
        st.write("إدارة المستخدمين وقاعدة البيانات.")
