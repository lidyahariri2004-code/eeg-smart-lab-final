import streamlit as st

# إعداد الصفحة للبرطابل
st.set_page_config(page_title="EEG Smart Lab", layout="centered")

st.title("🧠 EEG Smart Lab")
st.write("مرحباً بك في نظام تحليل إشارات الدماغ")

# الواجهة المطلوبة: 3 أزرار اختيار
choice = st.selectbox("الدخول بصفتك:", ["إختر...", "طبيب (Doctor)", "مريض (Patient)", "أدمن (Admin)"])

if choice == "طبيب (Doctor)":
    st.subheader("👨‍⚕️ قسم الطبيب")
    uploaded_file = st.file_uploader("ارفع ملف الإشارة (EEG) هنا", type=['npy', 'csv'])
    if uploaded_file:
        st.success("تم رفع الملف بنجاح، جاري التحليل...")

elif choice == "مريض (Patient)":
    st.subheader("👤 قسم المريض")
    st.info("يمكنك رؤية نتائج تحاليلك هنا.")

elif choice == "أدمن (Admin)":
    st.subheader("⚙️ لوحة التحكم")
    st.warning("خاص بالمسؤولين فقط.")
