import streamlit as st
import requests

# Set the FastAPI deployment URL
API_URL = "https://h-a-pred.onrender.com/predict/"  # Replace with your API's deployed URL

# Streamlit app title and description
st.title("Heart Attack Risk Prediction")
st.write("This app predicts the risk of a heart attack based on clinical parameters.")

with st.form(key="prediction_form"):
    st.header("Enter Patient Details:")
    age = float(st.number_input("Age", min_value=1, max_value=120, value=45))
    
    # Use the `index` parameter to map "Male" and "Female" to integers
    sex_label = st.selectbox("Sex", options=["Male", "Female"])
    sex = 1 if sex_label == "Male" else 0
    
    # Similarly update other categorical inputs
    cp_label = st.selectbox("Chest Pain Type (CP)", options=["Typical Angina", "Atypical Angina", "Non-Anginal", "Asymptomatic"])
    cp = {"Typical Angina": 0, "Atypical Angina": 1, "Non-Anginal": 2, "Asymptomatic": 3}[cp_label]
    
    trestbps = float(st.number_input("Resting Blood Pressure (trestbps)", min_value=50, max_value=200, value=120))
    chol = float(st.number_input("Cholesterol (chol)", min_value=100, max_value=600, value=200))
    
    fbs_label = st.selectbox("Fasting Blood Sugar > 120 mg/dl (FBS)", options=["Yes", "No"])
    fbs = 1 if fbs_label == "Yes" else 0
    
    restecg_label = st.selectbox("Resting Electrocardiographic Results (restecg)", options=["Normal", "ST-T wave abnormality", "Left ventricular hypertrophy"])
    restecg = {"Normal": 0, "ST-T wave abnormality": 1, "Left ventricular hypertrophy": 2}[restecg_label]
    
    thalach = float(st.number_input("Maximum Heart Rate Achieved (thalach)", min_value=50, max_value=220, value=150))
    
    exang_label = st.selectbox("Exercise Induced Angina (exang)", options=["Yes", "No"])
    exang = 1 if exang_label == "Yes" else 0
    
    oldpeak = float(st.number_input("ST Depression Induced (oldpeak)", min_value=0.0, max_value=10.0, value=1.0))
    
    slope_label = st.selectbox("Slope of the Peak Exercise ST Segment", options=["Upsloping", "Flat", "Downsloping"])
    slope = {"Upsloping": 0, "Flat": 1, "Downsloping": 2}[slope_label]
    
    ca = int(st.number_input("Number of Major Vessels (ca)", min_value=0, max_value=4, value=0))
    
    thal_label = st.selectbox("Thalassemia (thal)", options=["Normal", "Fixed Defect", "Reversible Defect"])
    thal = {"Normal": 0, "Fixed Defect": 1, "Reversible Defect": 2}[thal_label]

    # Add Submit Button
    submit_button = st.form_submit_button(label="Predict")


# Process the form submission
if submit_button:
    # Prepare input data for the API
    input_data = {
        "age": age,
        "sex": sex,
        "cp": cp,
        "trestbps": trestbps,
        "chol": chol,
        "fbs": fbs,
        "restecg": restecg,
        "thalach": thalach,
        "exang": exang,
        "oldpeak": oldpeak,
        "slope": slope,
        "ca": ca,
        "thal": thal,
    }

    # Send data to the API and get the prediction
    try:
        response = requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            result = response.json()
            prediction = result.get("prediction")
            probability = result.get("probability")

            # Display the prediction result
            st.success("Prediction successful!")
            st.write(f"**Prediction:** {'Heart Attack Risk' if prediction == 1 else 'No Risk'}")
            st.write(f"**Probability:** {probability}")

        else:
            st.error(f"Error: {response.status_code}")
            st.write(response.json())

    except Exception as e:
        st.error("Failed to connect to the prediction API.")
        st.write(f"Error details: {e}")
