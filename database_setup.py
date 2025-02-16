from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
from datetime import datetime

Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    dob = Column(DateTime, nullable=False)

class FormData(Base):
    __tablename__ = 'forms_data'
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, nullable=False)
    form_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

def setup_database():
    engine = create_engine('sqlite:///patient_assessments.db')
    Base.metadata.create_all(engine)
    return engine

def insert_data(engine, data):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    patient = session.query(Patient).filter_by(name=data["patient_name"], dob=datetime.strptime(data["dob"], "%m/%d/%Y")).first()
    if not patient:
        patient = Patient(name=data["patient_name"], dob=datetime.strptime(data["dob"], "%m/%d/%Y"))
        session.add(patient)
        session.commit()
    
    form_data = FormData(patient_id=patient.id, form_json=json.dumps(data))
    session.add(form_data)
    session.commit()

if __name__ == "__main__":
    engine = setup_database()
    with open("output.json", "r") as json_file:
        sample_data = json.load(json_file)
    insert_data(engine, sample_data)
    print("Data inserted into the database.")