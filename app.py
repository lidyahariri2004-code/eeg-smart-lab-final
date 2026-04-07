import os
import numpy as np
import pandas as pd
import pywt
import cv2
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from tensorflow.keras.models import load_model
from flask_sqlalchemy import SQLAlchemy 
from matplotlib import cm
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

app = Flask(__name__)
app.secret_key = "pfe_2026_ultra_secure_version"

# --- 1. إعداد قاعدة البيانات (SQLite) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'medical_system.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# جدول الأطباء
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

# جدول المرضى
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    prenom = db.Column(db.String(50))
    age = db.Column(db.Integer)
    username = db.Column(db.String(50), unique=True) 
    password = db.Column(db.String(50))
    # علاقة عكسية لجلب السجلات بسهولة
    logs = db.relationship('SeizureLog', backref='patient', lazy=True)

# جدول سجل النوبات (معدل لربط البيانات)
class SeizureLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    timestamp = db.Column(db.DateTime, default=datetime.now) 
    result = db.Column(db.String(50))

with app.app_context():
    db.create_all()

# --- 2. تحميل الموديل والدالة ---
MODEL_PATH = os.path.join(BASE_DIR, 'model.keras')
model = load_model(MODEL_PATH) if os.path.exists(MODEL_PATH) else None
STATIC_DIR = os.path.join(BASE_DIR, 'static')

if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

def generate_scalogram(canal, wavelet_name='cmor1.5-1.0', output_size=(224,224), fs=512):
    scales = np.logspace(1,3,num=100)
    coeffs, freqs = pywt.cwt(canal, scales, wavelet_name, 1/fs)
    mask = (freqs >= 1) & (freqs <= 80)
    coeffs = coeffs[mask,:]
    power = np.log1p(np.abs(coeffs))
    power_norm = (power - power.min())/(power.max()-power.min() + 1e-8)
    rgba = cm.get_cmap('viridis')(power_norm)
    rgb = np.delete(rgba, 3, 2)
    img_resized = cv2.resize(rgb, output_size)
    img_name = f"diag_{np.random.randint(1,999999)}.png"
    img_path = os.path.join(STATIC_DIR, img_name)
    cv2.imwrite(img_path, cv2.cvtColor(np.uint8(img_resized*255), cv2.COLOR_RGB2BGR))
    return img_name, img_resized

# --- 3. الروابط (Routes) ---

@app.route('/')
def index():
    return render_template('welcome.html')

# --- الجزء الخاص بـ Admin (معدل ليشمل المراقبة) ---
@app.route('/admin_doctors')
def admin_dashboard():
    # جلب قائمة الأطباء والمرضى
    docs = Doctor.query.all()
    pats = Patient.query.all()
    # جلب سجلات النوبات مرتبة من الأحدث إلى الأقدم مع بيانات المريض
    logs = SeizureLog.query.order_by(SeizureLog.timestamp.desc()).all()
    
    return render_template('admin.html', doctors=docs, patients=pats, seizure_logs=logs)

# -----------------------------------

@app.route('/patient_auth')
def patient_auth():
    return render_template('patient_auth.html')

@app.route('/patient_register_action', methods=['POST'])
def patient_register_action():
    try:
        nom, prenom, age, password = request.form.get('nom'), request.form.get('prenom'), request.form.get('age'), request.form.get('pass')
        if Patient.query.filter_by(username=nom).first(): return "Erreur: Utilisateur existe."
        new_p = Patient(nom=nom, prenom=prenom, age=age, username=nom, password=password)
        db.session.add(new_p); db.session.commit()
        session['user_id'] = new_p.id
        session['user_name'], session['role'] = f"{prenom} {nom}", 'patient'
        return redirect(url_for('patient_dash'))
    except Exception as e: return str(e)

@app.route('/patient_login_action', methods=['POST'])
def patient_login_action():
    p = Patient.query.filter_by(username=request.form.get('user'), password=request.form.get('pass')).first()
    if p:
        session['user_id'] = p.id
        session['user_name'], session['role'] = f"{p.prenom} {p.nom}", 'patient'
        return redirect(url_for('patient_dash'))
    return "Identifiants Patient incorrects"

@app.route('/patient_dash')
def patient_dash():
    if 'user_name' not in session or session.get('role') != 'patient': 
        return redirect(url_for('patient_auth'))
    return render_template('patient_dash.html')

@app.route('/patient_history')
def patient_history():
    if 'user_name' not in session or session.get('role') != 'patient': 
        return redirect(url_for('patient_auth'))
    logs = SeizureLog.query.filter_by(patient_id=session['user_id']).order_by(SeizureLog.timestamp.desc()).all()
    today_count = SeizureLog.query.filter(
        SeizureLog.patient_id == session['user_id'],
        db.func.date(SeizureLog.timestamp) == datetime.now().date()
    ).count()
    return render_template('patient_history.html', logs=logs, today_count=today_count)

@app.route('/doctor_portal')
def doctor_portal():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        new_doc = Doctor(fname=request.form.get('fname'), lname=request.form.get('lname'), email=request.form.get('email'), 
                         phone=request.form.get('phone'), username=request.form.get('username'), password=request.form.get('password'))
        db.session.add(new_doc); db.session.commit()
        session['user_name'], session['role'] = f"{new_doc.fname} {new_doc.lname}", 'doctor'
        return redirect(url_for('dashboard'))
    except: return "Erreur d'inscription docteur."

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        doc = Doctor.query.filter_by(username=request.form.get('username'), password=request.form.get('password')).first()
        if doc:
            session['user_name'], session['role'] = f"{doc.fname} {doc.lname}", 'doctor'
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_name' not in session or session.get('role') != 'doctor': return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files.get('file')
    if not file or not model: return jsonify({"error": "Modèle introuvable"})
    try:
        df = pd.read_csv(file, header=None, sep=None, engine='python')
        raw_signal = df.iloc[:, 0].values.astype(float)
        signal = (raw_signal - np.mean(raw_signal)) / (np.std(raw_signal) + 1e-8)
        img_name, img_data = generate_scalogram(signal)
        prob = float(model.predict(np.expand_dims(img_data, axis=0), verbose=0)[0][0])
        res_text = "Seizure (F)" if prob <= 0.5 else "Normal (N)"
        
        # حفظ السجل إذا كانت هناك نوبة وكان المريض مسجل دخوله
        if res_text == "Seizure (F)" and 'user_id' in session:
            new_log = SeizureLog(patient_id=session['user_id'], result="Seizure Detected")
            db.session.add(new_log); db.session.commit()
            
        return jsonify({
            "filename": file.filename, "res_text": res_text,
            "prob": round(prob, 4), "img_url": f"/static/{img_name}",
            "signal": raw_signal.tolist()[:300]
        })
    except Exception as e: return jsonify({"error": str(e)})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)