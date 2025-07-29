# 🧠 Medication Recommender System

## ❗ Problem Definition
In modern healthcare, generic treatment plans often overlook the unique medical histories, symptoms, and needs of individual patients. This can lead to ineffective treatments, adverse drug reactions, and poor health outcomes. Many patients, especially in under-resourced settings, also lack immediate access to qualified medical professionals for timely recommendations.

There is a need for a system that:
Analyzes patient-specific data (symptoms, history, etc.),
Uses machine learning to predict appropriate treatments,
And provides a personalized, fast, and accurate recommendation interface.

## 🎯 Objective
To develop a web-based machine learning system that provides personalized medication and treatment suggestions based on user-inputted medical data, ensuring accessibility, efficiency, and accuracy.

# Overview
This project is a **machine learning-based web application** designed to provide **personalized medication and treatment suggestions** based on patient data. The system allows users to **sign up or log in**, input health-related information, and receive intelligent treatment recommendations through a trained ML model.

---

## 📸 

![System Interface](static/interface.png)



## 🚀 Features

- ✅ User Signup & Login Authentication (Flask-Login)
- ✅ Personalized treatment recommendations using machine learning
- ✅ Easy-to-use web interface built with Flask + HTML/CSS
- ✅ Speech recognition for voice input
- ✅ Dashboard for patient data input and model interaction
- ✅ Deployed using flask

---

## 🛠️ Technologies Used

| Area            | Tools/Packages                          |
|-----------------|------------------------------------------|
| Backend         | Python, Flask                            |
| Frontend        | HTML, CSS, JavaScript                    |
| Machine Learning| scikit-learn, pandas, numpy, pickle      |
| Text Recognition| pytesseract, opencv-python, Pillow       |
| Authentication  | Flask-Login, Flask-WTF, WTForms          |
               

---

## 🧩 System Flow

1. **Login/Signup**: Users register or log in to access the system.
2. **Data Input**: Users enter medical data or upload images.
3. **Model Prediction**: Data is passed to a trained ML model to predict treatment.
4. **Recommendation**: Results are shown on the dashboard with treatment suggestions.
