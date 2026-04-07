import streamlit as st
import sqlite3
import os

# هاد الجزء يخلي الكود يخدم حتى ولو TensorFlow مكانش
try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    HAS_TF = True
except ImportError:
    HAS_TF = False

# ... باقي الكود تاعك (الدخول، قاعدة البيانات) يبقى كما راهو ...

st.title("🧠 EEG Smart Lab")

if not HAS_TF:
    st.warning("⚠️ النظام يعمل في وضع 'الواجهة الذكية'. (TensorFlow is updating on server)")
