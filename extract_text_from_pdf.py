!pip install pytesseract
!sudo apt install tesseract-ocr
!sudo apt install libtesseract-dev
!pip install pdf2image
!apt-get install poppler-utils


# Extracting Text from PDF

import pytesseract
from pdf2image import convert_from_path
import json
import re

def extract_text_from_pdf(pdf_path):
    try:
        images = convert_from_path(pdf_path)
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def parse_text_to_json(text):
    match = re.search(r'Patient Name:\s*(.*)', text)
    patient_name = match.group(1) if match else None  # Assign None if no match

    match = re.search(r'DOB:\s*(.*)', text)
    dob = match.group(1) if match else None

    match = re.search(r'Treatment Date:\s*(.*)', text)
    date = match.group(1) if match else None

    match = re.search(r'Injection:\s*(Yes|No)', text)
    injection = match.group(1) if match else None

    match = re.search(r'Exercise Therapy:\s*(Yes|No)', text)
    exercise_therapy = match.group(1) if match else None


    difficulty_ratings = {} # Initialize as an empty dictionary

    # Bending
    match = re.search(r'Bending:\s*(\d)', text)
    if match:
        difficulty_ratings["bending"] = int(match.group(1))
    else:
        difficulty_ratings["bending"] = None # or some default value like 0
        print("Warning: 'Bending' value not found in the text.")

    # Putting on Shoes
    match = re.search(r'Putting on Shoes:\s*(\d)', text)
    if match:
        difficulty_ratings["putting_on_shoes"] = int(match.group(1))
    else:
        difficulty_ratings["putting_on_shoes"] = None # or some default value
        print("Warning: 'Putting on Shoes' value not found in the text.")

    # Sleeping
    match = re.search(r'Sleeping:\s*(\d)', text)
    if match:
        difficulty_ratings["sleeping"] = int(match.group(1))
    else:
        difficulty_ratings["sleeping"] = None # or some default value
        print("Warning: 'Sleeping' value not found in the text.")


    # Handle potential None values from re.search
    match = re.search(r'Since last treatment:\s*(.*)', text)
    since_last_treatment = match.group(1) if match else None

    match = re.search(r'Since start of treatment:\s*(.*)', text)
    since_start_of_treatment = match.group(1) if match else None

    match = re.search(r'Last 3 days:\s*(.*)', text)
    last_3_days = match.group(1) if match else None

    patient_changes = {
        "since_last_treatment": since_last_treatment,
        "since_start_of_treatment": since_start_of_treatment,
        "last_3_days": last_3_days
    }

    # Similar handling for other fields prone to this error
    match = re.search(r'Pain:\s*(\d+)', text)
    pain = int(match.group(1)) if match else None

    match = re.search(r'Numbness:\s*(\d+)', text)
    numbness = int(match.group(1)) if match else None

    match = re.search(r'Tingling:\s*(\d+)', text)
    tingling = int(match.group(1)) if match else None

    match = re.search(r'Burning:\s*(\d+)', text)
    burning = int(match.group(1)) if match else None

    match = re.search(r'Tightness:\s*(\d+)', text)
    tightness = int(match.group(1)) if match else None

    pain_symptoms = {
        "pain": pain,
        "numbness": numbness,
        "tingling": tingling,
        "burning": burning,
        "tightness": tightness
    }

    # Similar handling for medical_assistant_data
    match = re.search(r'Blood Pressure:\s*(.*)', text)
    blood_pressure = match.group(1) if match else None

    match = re.search(r'HR:\s*(\d+)', text)
    hr = int(match.group(1)) if match else None

    match = re.search(r'Weight:\s*(\d+)', text)
    weight = int(match.group(1)) if match else None

    match = re.search(r'Height:\s*(.*)', text)
    height = match.group(1) if match else None

    match = re.search(r'SpO2:\s*(\d+)', text)
    spo2 = int(match.group(1)) if match else None

    match = re.search(r'Temperature:\s*(.*)', text)
    temperature = match.group(1) if match else None

    match = re.search(r'Blood Glucose:\s*(\d+)', text)
    blood_glucose = int(match.group(1)) if match else None

    match = re.search(r'Respirations:\s*(\d+)', text)
    respirations = int(match.group(1)) if match else None

    medical_assistant_data = {
        "blood_pressure": blood_pressure,
        "hr": hr,
        "weight": weight,
        "height": height,
        "spo2": spo2,
        "temperature": temperature,
        "blood_glucose": blood_glucose,
        "respirations": respirations
    }

    structured_data = {
        "patient_name": patient_name,
        "dob": dob,
        "date": date,
        "injection": injection,
        "exercise_therapy": exercise_therapy,
        "difficulty_ratings": difficulty_ratings,
        "patient_changes": patient_changes,
        "pain_symptoms": pain_symptoms,
        "medical_assistant_data": medical_assistant_data
    }
    return json.dumps(structured_data, indent=4)

if __name__ == "__main__":
    pdf_path = "/content/drive/MyDrive/Assignments/Okasol/oaksol_Intern_OCR_Assignment.pdf"
    text = extract_text_from_pdf(pdf_path)
    if text:
        json_data = parse_text_to_json(text)
        with open("output.json", "w") as json_file:
            json_file.write(json_data)
        print("JSON data saved to output.json")