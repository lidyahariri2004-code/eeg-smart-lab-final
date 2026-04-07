import streamlit as st
import sqlite3
import time

# --- 1. إعدادات الصفحة والجمالية (CSS) ---
st.set_page_config(page_title="EEG Smart Lab | Doctor Space", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    .payment-box {
        background-color: #ffffff; padding: 15px; border-radius: 12px;
        border: 1.5px solid #FFD700; text-align: center; margin: 10px auto; max-width: 250px;
    }
    .price-tag { font-size: 18px; font-weight: bold; color: #B8860B; }
    .pay-button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: white !important; padding: 5px 15px; border-radius: 6px;
        font-weight: bold; font-size: 14px; text-decoration: none; display: inline-block;
    }
    .doctor-card {
        background: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-left: 5px solid #1E3A8A;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. قاعدة البيانات ---
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

# --- 3. إدارة الحالة ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = ""

# --- 4. منطق الواجهات ---

# أ) واجهة الدخول والتسجيل
if not st.session_state.logged_in:
    st.title("🧠 EEG Smart Lab")
    
    col1, col2, col3 = st.columns(3)
    with col1: 
        if st.button("👨‍⚕️ طبيب"): st.session_state.role = "doctor"
    with col2: 
        if st.button("👤 مريض"): st.session_state.role = "patient"
    with col3: 
        if st.button("⚙️ أدمن"): st.session_state.role = "admin"

    if 'role' in st.session_state and st.session_state.role == "doctor":
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register & Pay"])
        
        with tab1:
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

        with tab2:
            st.subheader("Créer un nouveau compte")
            c1, c2 = st.columns(2)
            fn = c1.text_input("Prénom")
            ln = c2.text_input("Nom")
            em = st.text_input("Email")
            un = st.text_input("Username", key="u2")
            pw = st.text_input("Password", type="password", key="p2")
            
            st.markdown("""<div class="payment-box"><div class="price-tag">100,000 DZD / Month</div>
                        <a href="#" class="pay-button">💳 Payer Maintenant</a></div>""", unsafe_allow_html=True)
            
            chk = st.checkbox("أوافق على تفعيل الحساب بعد الدفع")
            
            if st.button("S'INSCRIRE ET ENTRER"):
                if chk and un and pw:
                    try:
                        conn = get_db_connection()
                        conn.execute("INSERT INTO doctor (fname, lname, email, username, password) VALUES (?,?,?,?,?)",
                                     (fn, ln, em, un, pw))
                        conn.commit()
                        conn.close()
                        # دخول تلقائي
                        st.session_state.logged_in = True
                        st.session_state.user_name = f"{fn} {ln}"
                        st.success("✅ تم التسجيل والدفع بنجاح! جاري تحويلك للمختبر...")
                        time.sleep(1)
                        st.rerun()
                    except: st.error("❌ اسم المستخدم موجود")

# ب) واجهة التحليل "الرائعة" (الواو)
else:
    # Sidebar احترافي
    st.sidebar.markdown(f"### 👨‍⚕️ د. {st.session_state.user_name}")
    st.sidebar.divider()
    if st.sidebar.button("🚪 تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

    # محتوى الصفحة "الواو"
    st.markdown(f"## 🏥 فضاء التحليل العصبي المتقدم")
    
    # بطاقات إحصائية سريعة (Dashboard)
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1: st.metric("حالات اليوم", "12", "+2")
    with kpi2: st.metric("دقة النموذج", "98.5%", "ResNet152")
    with kpi3: st.metric("الاشتراك", "نشط", "30 يوم")

    st.divider()

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.markdown('<div class="doctor-card">', unsafe_allow_html=True)
        st.subheader("📥 رفع البيانات")
        uploaded_file = st.file_uploader("ارفع ملف EEG (CSV/NPY)", type=['csv', 'npy'])
        if uploaded_file:
            with st.spinner('جاري معالجة الإشارة وتحويلها لـ Scalogram...'):
                time.sleep(2)
                st.success("✅ تم التحويل بنجاح")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.subheader("📊 نتائج التحليل الذكي")
        if uploaded_file:
            # هنا نديرو Simulation لعرض النتائج
            st.info("إشارة المخ مكتملة - لا توجد نوبات صرع مكتشفة")
            # تقدري ترفعي صورة Scalogram هنا كمثال للأستاذة
            st.image("https://via.placeholder.com/600x300.png?text=EEG+Scalogram+Visualization", caption="Scalogram (Wavelet Transform)")
        else:
            st.warning("يرجى رفع ملف لبدء التحليل بالذكاء الاصطناعي.")

    # جزء البزنس (Business Logic)
    st.divider()
    st.caption("نظام EEG Smart Lab مدعوم بـ Deep Learning - جميع الحقوق محفوظة لعام 2026")
