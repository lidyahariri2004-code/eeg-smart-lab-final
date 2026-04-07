import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
import warnings

warnings.filterwarnings('ignore')

# --- 1. إعدادات الصفحة والجمالية (Wide Layout for Doctors) ---
st.set_page_config(page_title="EEG Smart Lab | Advanced Analytics", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f1f5f9; }
    /* تنسيق الكاردات الخاصة بالتحليل */
    .analysis-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
    }
    .status-text {
        font-weight: bold;
        font-size: 20px;
        color: #1E3A8A;
        text-align: center;
        margin: 10px 0;
    }
    .main-title { color: #1E3A8A; font-weight: bold; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة قاعدة البيانات (SQL) ---
def get_db_connection():
    conn = sqlite3.connect('medical_system.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- 3. إدارة الجلسة (Session State) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.role = ""

# --- 4. منطق الواجهات ---

# أ) واجهة الدخول والتسجيل (نحتفظ بها كما هي بلا مشاكل)
if not st.session_state.logged_in:
    # ... (هنا ضعي كود الدخول والتسجيل الذهبي اللي تفاهمنا عليه في Image 3) ...
    # (لكن لا داعي لإعادة كتابته هنا، سأركز على واجهة الطبيب الجديدة)
    st.session_state.logged_in = True # محاكاة الدخول لعرض الواجهة الجديدة
    st.session_state.user_name = "د. ليليا"
    st.session_state.role = "doctor"
    st.rerun() # تأكدي من إزالة هذه الأسطر الثلاثة في الكود النهائي!

# ب) واجهة الطبيب الاحترافية الجديدة (Simulation Layout)
else:
    # --- Sidebar احترافي ---
    st.sidebar.markdown(f"### 👨‍⚕️ {st.session_state.user_name}")
    st.sidebar.divider()
    if st.sidebar.button("🚪 تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

    # محتوى الصفحة الجديدة
    st.markdown(f"## 🏥 فضاء التحليل العصبي الرقمي")
    
    st.divider()

    # --- التقسيم الجديد: يسار (إحصائيات ورفع) | يمين (التحليل الحي والنتيجة) ---
    col_left, col_right = st.columns([1, 2.5])

    # 1. القائمة اليسرى (Sidebar-like Dashboard on the main page)
    with col_left:
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.subheader("📥 مركز البيانات")
        # الجزء الخاص برفع الملفات
        uploaded_file = st.file_uploader("ارفع ملف الإشارة (CSV/NPY)", type=['csv', 'npy'])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.subheader("📋 ملخص اليوم")
        # صغرنا KPI تاع الصورة القديمة وحطيناها هنا
        st.metric("حالات اليوم", "12", "+2")
        st.metric("الدقة", "98.5%", "ResNet152")
        st.markdown('</div>', unsafe_allow_html=True)

        # بطاقة حالة الحساب
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.subheader("💳 حالة الاشتراك")
        st.info("الخطة المتقدمة (شهرية) - نشطة.")
        st.caption("تاريخ التجديد: 25 أفريل 2026")
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. القائمة اليمنى (المختبر الحي والنتيجة - "الواو")
    with col_right:
        if uploaded_file:
            # دالة لمحاكاة تحميل البيانات وقرائتها
            def simulate_eeg_processing(file):
                df = pd.read_csv(file, header=None).iloc[:, 0].values.astype(float)
                signal = (df - np.mean(df)) / (np.std(df) + 1e-8)
                return signal[:500] # نأخذ أول 500 نقطة للعرض

            st.write("### ⏱️ فحص الإشارة العصبي (Simulation)")
            
            with st.spinner('جاري جلب وتحليل الإشارة من الملف...'):
                time.sleep(1.5)
                signal_data = simulate_eeg_processing(uploaded_file)
                
            # محاكاة عرض إشارة متحركة (Professional Simulation)
            st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
            st.write("📊 عرض الإشارة العصبي الحيّ")
            # استخدام Plotly لإشارة باحترافية
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=signal_data, mode='lines', line=dict(color='#1E3A8A', width=2)))
            fig.update_layout(template='plotly_white', height=250, margin=dict(l=20, r=20, t=20, b=20),
                              xaxis_title="Time points", yaxis_title="Microvolts (Norm)")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # جزء النتيجة النهائية (The Climax)
            st.write("### 🎯 نتيجة تحليل ResNet152 الذكي")
            with st.spinner('جاري تطبيق خوارزمية Deep Learning للبحث عن النوبات...'):
                time.sleep(2)
                
            st.markdown('<div class="analysis-card" style="border-left: 5px solid #10b981;">', unsafe_allow_html=True)
            # النتيجة باحترافية
            st.write("#### تشخيص الذكاء الاصطناعي:")
            st.markdown('<p class="status-text" style="color: #10b981;">✅ إشارة مكتملة - لا توجد نوبات صرع مكتشفة (Normal)</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # تقدري تزيدي هنا الـ Scalogram إذا حبيتي بعد الأستاذة تشوفو

        else:
            # الحالة الفارغة قبل رفع الملف
            st.info("يرجى رفع ملف EEG من القائمة اليسرى للبدء في تحليل إشارة المخ الذكي.")
            st.image("https://via.placeholder.com/1000x500.png?text=EEG+Lab+-+Live+Simulation+Will+Appear+Here", caption="واجهة التحليل الحي قيد الانتظار...")

    # جزء البزنس (Business Logic)
    st.divider()
    st.caption("نظام EEG Smart Lab مدعوم بـ Deep Learning - جميع الحقوق محفوظة لعام 2026 | Simulation mode for demonstration")
