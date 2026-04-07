import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# إعداد الصفحة للوضع العريض (Wide) ليناسب الأطباء
st.set_page_config(page_title="EEG Smart Lab | Pro", layout="wide")

# تنسيق CSS لتصغير العناصر وجعلها احترافية
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .stMetric { background: white; padding: 10px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .pay-btn { background: #FFD700; color: black; padding: 5px 15px; border-radius: 5px; text-decoration: none; font-size: 14px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# إدارة الجلسة (Session State)
if 'step' not in st.session_state: st.session_state.step = "main"

# --- واجهة البداية (الأزرار الثلاثة) ---
if st.session_state.step == "main":
    st.title("🧠 EEG Smart Lab")
    cols = st.columns(3)
    if cols[0].button("👨‍⚕️ طبيب"): st.session_state.step = "doctor_login"
    if cols[1].button("👤 مريض"): st.session_state.step = "patient"
    if cols[2].button("⚙️ أدمن"): st.session_state.step = "admin"

# --- واجهة الطبيب (الدخول والاشتراك) ---
elif st.session_state.step == "doctor_login":
    tab1, tab2 = st.tabs(["🔑 دخول", "📝 اشتراك جديد"])
    with tab1:
        u = st.text_input("Username")
        if st.button("Se Connecter"): 
            st.session_state.step = "doctor_dashboard"
            st.rerun()
    with tab2:
        st.write("### Créer un Compte")
        st.text_input("Nom & Prénom")
        st.markdown('<div style="border:1px solid #FFD700; padding:10px; border-radius:10px; text-align:center;">'
                    '<b>100,000 DZD / شهر</b><br><br>'
                    '<a href="#" class="pay-btn">💳 Payer</a></div><br>', unsafe_allow_html=True)
        if st.button("S'INSCRIRE ET ENTRER"):
            st.session_state.step = "doctor_dashboard"
            st.rerun()

# --- واجهة التحليل "الواو" (Dashboard) ---
elif st.session_state.step == "doctor_dashboard":
    st.sidebar.markdown("### 👨‍⚕️ فضاء الطبيب")
    if st.sidebar.button("🚪 خروج"): 
        st.session_state.step = "main"
        st.rerun()

    # التقسيم: يسار (الرفع والمعلومات) | يمين (الإشارة والنتيجة)
    col_side, col_main = st.columns([1, 2.5])

    with col_side:
        st.subheader("📥 البيانات")
        up = st.file_uploader("ارفع ملف EEG", type=['csv', 'npy'])
        st.divider()
        st.metric("حالات اليوم", "12", "+2")
        st.metric("النموذج", "ResNet152", "Active")

    with col_main:
        st.header("📊 مركز التحليل العصبي الحي")
        if up:
            with st.spinner("جاري معالجة الإشارة..."):
                time.sleep(1.5)
                # توليد إشارة وهمية للعرض الاحترافي
                t = np.linspace(0, 10, 500)
                sig = np.sin(t) + np.random.normal(0, 0.2, 500)
                
                # التلفزيون (Plotly Chart)
                fig = go.Figure()
                fig.add_trace(go.Scatter(y=sig, mode='lines', line=dict(color='#1E3A8A')))
                fig.update_layout(title="EEG Live Stream (Simulation)", height=300, margin=dict(l=0,r=0,t=30,b=0))
                st.plotly_chart(fig, use_container_width=True)

                st.subheader("🎯 النتيجة النهائية")
                time.sleep(1)
                st.success("✅ الحالة: طبيعية (Normal) - لا توجد نوبات صرع")
        else:
            st.info("يرجى رفع ملف لبدء المحاكاة والتحليل.")
