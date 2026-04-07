import streamlit as st
import sqlite3
import os

# إعداد الصفحة للبرطابل
st.set_page_config(page_title="EEG Smart Lab", layout="centered")

# دالة للتحقق من الطبيب في قاعدة البيانات
def check_doctor(username, password):
    conn = sqlite3.connect('medical_system.db')
    c = conn.cursor()
    c.execute("SELECT * FROM doctor WHERE username=? AND password=?", (username, password))
    data = c.fetchone()
    conn.close()
    return data

st.title("🧠 EEG Smart Lab")

# إدارة الجلسة (Session State)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("تسجيل دخول الطبيب")
    user = st.text_input("اسم المستخدم")
    pw = st.text_input("كلمة المرور", type="password")
    
    if st.button("دخول"):
        if check_doctor(user, pw):
            st.session_state.logged_in = True
            st.success("تم الدخول بنجاح!")
            st.rerun()
        else:
            st.error("اسم المستخدم أو كلمة المرور خاطئة")
else:
    st.sidebar.success("أهلاً بك أيها الطبيب")
    if st.sidebar.button("تسجيل خروج"):
        st.session_state.logged_in = False
        st.rerun()
        
    st.header("👨‍⚕️ لوحة تحكم الطبيب")
    uploaded_file = st.file_uploader("ارفع ملف EEG لتحليله (CSV)", type="csv")
    if uploaded_file:
        st.info("جاري المعالجة...")
        # هنا يجي كود الـ Prediction
