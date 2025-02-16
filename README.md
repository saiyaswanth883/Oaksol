# Patient Assessment Data Extraction

## Overview
This project extracts text from scanned patient assessment forms (JPEG/PDF), parses and structures the extracted data into JSON format, and stores the structured data in a SQL database.

## Setup and Usage

### Prerequisites
- Python 3.x
- Tesseract OCR
- Poppler (for PDF conversion)

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/saiyaswanth883/Oaksol.git
   cd Oaksol
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

4. Ensure Tesseract OCR and Poppler are installed and added to your PATH.

### Usage

1. Extract text from a PDF file:
   ```sh
   python extract_text_from_pdf.py
   ```

2. Setup the database and insert sample data:
   ```sh
   python database_setup.py
   ```

## Sample JSON Output
```json
{
    "patient_name": "John Doe",
    "dob": "01/05/1988",
    "date": "02/06/2025",
    "injection": "Yes",
    "exercise_therapy": "No",
    "difficulty_ratings": {
        "bending": 3,
        "putting_on_shoes": 1,
        "sleeping": 2
    },
    "patient_changes": {
        "since_last_treatment": "Not Good",
        "since_start_of_treatment": "Worse",
        "last_3_days": "Bad"
    },
    "pain_symptoms": {
        "pain": 2,
        "numbness": 5,
        "tingling": 6,
        "burning": 7,
        "tightness": 5
    },
    "medical_assistant_data": {
        "blood_pressure": "120/80",
        "hr": 80,
        "weight": 67,
        "height": "5'7",
        "spo2": 98,
        "temperature": "98.6",
        "blood_glucose": 115,
        "respirations": 16
    }
}
```

## Database Schema
The database schema is defined in `database_setup.py` and includes two tables `patients` and `forms_data` with the following fields:
- `patients` table:
  - `id`: Integer, Primary Key
  - `name`: String
  - `dob`: DateTime
- `forms_data` table:
  - `id`: Integer, Primary Key
  - `patient_id`: Integer, Foreign Key referencing `patients(id)`
  - `form_json`: Text
  - `created_at`: DateTime

## SQL Scripts
The database setup and insertion are handled programmatically in `database_setup.py`.
