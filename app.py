import streamlit as st
import sqlite3
import os

# محاولة تحميل TensorFlow بلا ما يحبس السيستيم
try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

st.set_page_config(page_title="EEG Smart Lab", layout="centered")

# ... (باقي الكود تاع قاعدة البيانات اللي درناه قبيل)

st.title("🧠 EEG Smart Lab")

if not TF_AVAILABLE:
    st.warning("⚠️ النظام يشتغل حالياً في وضع العرض (بدون موديل الذكاء الاصطناعي) بسبب تحديثات السيرفر.")

# كود الدخول والواجهة (Doctor/Patient)
