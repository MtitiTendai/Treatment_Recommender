from flask import Flask, render_template, url_for, flash, jsonify
from flask import Flask, render_template, request, redirect, url_for, session 
from flask_mysqldb import MySQL 
import mysql
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt
import numpy as np
import pandas as pd
import pickle
import os
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy 
import bcrypt
import pyttsx3
import speech_recognition as sr

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()



# custome and helping functions
#==========================helper funtions================
def helper(dis):
    desc = description_data[description_data['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    pre = precautions_data[precautions_data['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values]

    med = medications_data[medications_data['Disease'] == dis]['Medication']
    med = [med for med in med.values]

    die = diets_data[diets_data['Disease'] == dis]['Diet']
    die = [die for die in die.values]

    wrkout = workout_data[workout_data['disease'] == dis] ['workout']


    return desc,pre,med,die,wrkout

symptoms_dict = {'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12, 'spotting_ urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16, 'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20, 'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24, 'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32, 'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41, 'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45, 'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51, 'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55, 'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58, 'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61, 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75, 'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81, 'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131}
diseases_list = {15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis', 14: 'Drug Reaction', 33: 'Peptic ulcer diseae', 1: 'AIDS', 12: 'Diabetes ', 17: 'Gastroenteritis', 6: 'Bronchial Asthma', 23: 'Hypertension ', 30: 'Migraine', 7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)', 28: 'Jaundice', 29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A', 19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E', 3: 'Alcoholic hepatitis', 36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)', 18: 'Heart attack', 39: 'Varicose veins', 26: 'Hypothyroidism', 24: 'Hyperthyroidism', 25: 'Hypoglycemia', 31: 'Osteoarthristis', 5: 'Arthritis', 0: '(vertigo) Paroymsal  Positional Vertigo', 2: 'Acne', 38: 'Urinary tract infection', 35: 'Psoriasis', 27: 'Impetigo'}

# Model Prediction function
def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        input_vector[symptoms_dict[item]] = 1
    return diseases_list[svc.predict([input_vector])[0]]


# loading datasets
symptom_data = pd.read_csv('datasets/symtoms_df.csv')
precautions_data = pd.read_csv('datasets/precautions_df.csv')
workout_data = pd.read_csv('datasets/workout_df.csv')
description_data = pd.read_csv('datasets/description.csv')
medications_data = pd.read_csv('datasets/medications.csv')
diets_data = pd.read_csv('datasets/diets.csv')


# loading the model
svc = pickle.load(open('models/svc.pkl', 'rb'))

dataset_folder = "C:/Users/Admin/Desktop/medicine recommendation system in python/datasets"
def get_data():
    if os.name == "nt":
        os.startfile("datasets")
    elif os.name == "posix":
        os.system(f"open {dataset_folder}")
    return 'Folder should now be open in your file explorer'

# R

# Welcome
@app.route('/')
def welcome():
    return render_template('welcome.html')
# Signup
@app.route('/register',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        # handle request
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']

        new_user = User(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('User signup success')
        return redirect('/login')

    return render_template('register.html')

# Login
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['name'] = user.name
            session['email'] = user.email
            session['password'] = user.password
            return redirect('/index')
        else:
            return render_template('login.html',error='Login failed, invalid email or password')

    return render_template('login.html')

# Index
@app.route('/index')
def index():   
    return render_template('index.html')    
    
# Logout
@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/login')
 
# Define a route for the home page
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        symptoms = request.form.get('symptoms')
        user_symptoms = [s.strip() for s in symptoms.split(',')]
        # Remove any extra characters, if any
        user_symptoms = [symptom.strip("[]' ") for symptom in user_symptoms]
        predicted_disease = get_predicted_value(user_symptoms)
        desc, pre, med, die, wrkout = helper(predicted_disease)
        
        my_pre = []
        for i in pre[0]:
            my_pre.append(i)
        
        return render_template('index.html', predicted_disease= predicted_disease, dis_des= desc,
                                   dis_pre= my_pre, dis_med= med, dis_diet= die,
                                   dis_wrkout= wrkout)

# About route
@app.route('/about')
def about():
    return render_template("about.html")

# Speech Recognition
@app.route('/process_symptoms', methods=['GET','POST'])
def process_symptoms():
    data = request.get_json()
    symptoms = data['symptoms'].lower()

    # Dummy logic - replace with your actual model prediction logic
    matched_row = symptom_data[symptom_data['symptoms'].str.contains(symptoms, case=False)]
    
    if matched_row.empty:
        return jsonify({'disease': "unknown", 'precautions': "N/A", 'workouts': "N/A", 'medications': "N/A", 'diets': "N/A"})

    disease = matched_row.iloc[0]['disease']

    # Lookup from other datasets
    precautions = precautions_data[precautions_data['disease'] == disease].iloc[0]['precautions']
    workouts = workout_data[workout_data['disease'] == disease].iloc[0]['workouts']
    medications = medications_data[medications_data['disease'] == disease].iloc[0]['medications']
    diets = diets_data[diets_data['disease'] == disease].iloc[0]['diets']

    return jsonify({
        'disease': disease,
        'precautions': precautions,
        'workouts': workouts,
        'medications': medications,
        'diets': diets
    })

@app.route('/data')
def open_data_folder():
    folder_path = r"C:/Users/Admin/Desktop/medicine recommendation system in python/datasets"
    os.startfile(folder_path)  # This opens the folder in File Explorer
    return redirect('home')  # Redirect to home or another page


# Forgot Password
@app.route('/reset', methods=['GET'])
def forgot_password():
    return render_template('reset.html')

# Handle the reset form submission
@app.route('/reset-password', methods=['POST'])
def reset_password():
    email = request.form['email']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    if new_password != confirm_password:
        flash('Passwords do not match!')
        return redirect(url_for('forgot_password'))

    user = User.query.filter_by(email=email).first()
    if user:
        user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Password reset successfully! You can now log in.')
        return redirect(url_for('login'))
    else:
        flash('Email not found!')
        return redirect(url_for('forgot_password'))


# Python main
if __name__ == '__main__':
    app.run(debug= True)