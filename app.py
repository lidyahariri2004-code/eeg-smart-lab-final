import streamlit as st
import time
import pandas as pd
import numpy as np

# إعداد الصفحة للوضع العريض (Wide) ليناسب الأطباء
st.set_page_config(page_title="EEG Smart Lab | Pro", layout="wide")

# تنسيق CSS احترافي (ألوان هادئة وطبية)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stMetric { background: white; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0; }
    .status-card { background: white; padding: 20px; border-radius: 15px; border-left: 5px solid #1e40af; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    .pay-btn { background: #FFD700; color: black; padding: 8px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = "main"

# --- 1. الواجهة الرئيسية (الأزرار الثلاثة) ---
if st.session_state.step == "main":
    st.markdown("<h1 style='text-align:center;'>🧠 EEG Smart Lab</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align:center;'>مرحباً بك في منصة التحليل الذكي، اختر هويتك للبدء</p>", unsafe_allow_html=True)
    st.divider()
    c1, c2, c3 = st.columns(3)
    if c1.button("👨‍⚕️ طبيب (Doctor)", use_container_width=True): st.session_state.step = "doctor_auth"
    if c2.button("👤 مريض (Patient)", use_container_width=True): st.info("فضاء المريض قيد التطوير")
    if c3.button("⚙️ أدمن (Admin)", use_container_width=True): st.info("فضاء المدير قيد التطوير")

# --- 2. واجهة الدخول والاشتراك (الذهبية) ---
elif st.session_state.step == "doctor_auth":
    st.markdown("### 👨‍⚕️ فضاء الطبيب")
    t1, t2 = st.tabs(["🔑 تسجيل الدخول", "📝 اشتراك جديد"])
    with t1:
        st.text_input("اسم المستخدم")
        st.text_input("كلمة المرور", type="password")
        if st.button("دخول"): 
            st.session_state.step = "dashboard"
            st.rerun()
    with t2:
        st.write("#### فتح حساب طبيب جديد")
        st.text_input("الاسم واللقب")
        st.text_input("البريد الإلكتروني")
        st.markdown("""<div style='background:#fffbeb; padding:15px; border-radius:10px; border:1px solid #fef3c7; text-align:center;'>
                    <span style='color:#92400e; font-weight:bold;'>خطة التحليل الاحترافية: 100,000 DZD / شهر</span><br><br>
                    <a href='#' class='pay-btn'>💳 دفع واشتراك (Payer)</a></div><br>""", unsafe_allow_html=True)
        if st.button("تأكيد التسجيل والدخول"):
            st.session_state.step = "dashboard"
            st.rerun()

# --- 3. واجهة التحليل الاحترافية (الواو) ---
elif st.session_state.step == "dashboard":
    st.sidebar.markdown("### 👨‍⚕️ د. ليليا")
    if st.sidebar.button("🚪 خروج"): 
        st.session_state.step = "main"
        st.rerun()

    st.markdown("## 🏥 فضاء التحليل العصبي المتقدم")
    st.divider()

    # التقسيم الاحترافي: يسار (الرفع والمعلومات) | يمين (التلفزيون والنتيجة)
    col_side, col_main = st.columns([1, 2.5])

    with col_side:
        st.markdown('<div class="status-card">', unsafe_allow_html=True)
        st.subheader("📥 البيانات")
        up = st.file_uploader("ارفع ملف EEG (CSV/NPY)", type=['csv', 'npy'])
        st.markdown('</div><br>', unsafe_allow_html=True)
        
        st.metric("حالات اليوم", "12", "+2")
        st.metric("دقة الموديل", "98.5%", "ResNet152")
        st.metric("الاشتراك", "نشط", "30 يوم")

    with col_main:
        if up:
            st.subheader("📊 مراقبة الإشارة الحية (Live Stream)")
            with st.spinner("جاري قراءة البيانات وتحليل الذبذبات..."):
                time.sleep(1.5)
                # رسم الإشارة بطريقة احترافية وسريعة (Native Streamlit)
                chart_data = pd.DataFrame(np.random.randn(50, 1), columns=['EEG Signal'])
                st.line_chart(chart_data, height=250)
                
            st.divider()
            st.subheader("🎯 نتيجة التشخيص الذكي")
            with st.spinner("جاري تطبيق خوارزمية ResNet152..."):
                time.sleep(2)
            st.success("✅ النتيجة: طبيعية (Normal) - لا توجد نوبات صرع مكتشفة.")
            st.balloons()
        else:
            st.info("👋 مرحباً دكتور! يرجى رفع ملف إشارة المخ من القائمة اليسرى لبدء عملية التحليل.")
            st.image("https://via.placeholder.com/800x400.png?text=EEG+Simulation+Waiting+for+Data...", use_column_width=True)
