import streamlit as st
import sqlite3
import os

# إعداد الصفحة
st.set_page_config(page_title="EEG Smart Lab", layout="centered")

def check_doctor(user, pw):
    conn = sqlite3.connect('medical_system.db')
    c = conn.cursor()
    c.execute("SELECT * FROM doctor WHERE username=? AND password=?", (user, pw))
    data = c.fetchone()
    conn.close()
    return data

st.title("🧠 EEG Smart Lab")

if 'login' not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.subheader("تسجيل دخول الطبيب")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Log In"):
        if check_doctor(username, password):
            st.session_state.login = True
            st.rerun()
        else:
            st.error("خطأ في البيانات")
else:
    st.sidebar.success("مرحباً بك")
    if st.sidebar.button("Logout"):
        st.session_state.login = False
        st.rerun()
    st.header("فضاء الطبيب")
    st.file_uploader("ارفع ملف EEG", type=['csv'])
