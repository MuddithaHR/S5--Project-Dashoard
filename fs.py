import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime 
import pandas as pd
from sql import *

user_id = 0
chat_id = 0

def get_chat_history_to_dataframe():
    if not firebase_admin._apps:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    try:
        db = firestore.client()
        docs = db.collection('Chats')
        results = docs.stream()
        
        arr = []

        for result in results:
            arr.append(result.to_dict())
        
        df = pd.DataFrame.from_dict(arr)
        df['time'] = df['time'].dt.tz_convert('Asia/Kolkata')
        df['date'] = df['time'].dt.date
        df['time_of_day'] = df['time'].dt.time
        df['user_input'] = df['user_input'].str.lower()

        return df

    except Exception as e:
        print(f"Failed to get chat history: {str(e)}")


def get_speciality_counts(start_date, end_date):
    specializations = get_specializations()

    counts = {}
    df = get_chat_history_to_dataframe()
    df=df.query(
            "date >= @start_date & date <= @end_date"
        )

    for specialization in specializations:
        counts[specialization] = df['user_input'].str.count(specialization).sum()

    spec_df = pd.DataFrame(list(counts.items()), columns=['Specialization', 'Search Counts']).sort_values(by=['Search Counts'], ascending=False).head()

    return spec_df


def get_doctor_counts(start_date, end_date):
    doctors = get_doctors()

    counts = {}
    df = get_chat_history_to_dataframe()
    df=df.query(
            "date >= @start_date & date <= @end_date"
        )

    for doctor in doctors:
        counts[doctor] = df['user_input'].str.count(doctor).sum()

    doc_df = pd.DataFrame(list(counts.items()), columns=['Doctor Name', 'Search Counts']).sort_values(by=['Search Counts'], ascending=False).head()

    return doc_df


def get_disease_counts(start_date, end_date):
    
    diseases = ["influenza", "covid", "common cold", "heart disease", "cancer", "diabetes", "hypertension", "stroke", "arthritis", "obesity", "asthma", "chronic obstructive pulmonary disease", "hiv/aids", "malaria", "tuberculosis", "hepatitis", "pneumonia", "osteoporosis", "allergies", "depression", "anxiety disorders", "schizophrenia", "bipolar disorder", "parkinson's disease", "epilepsy", "multiple sclerosis", "rheumatoid arthritis", "autoimmune diseases", "celiac disease", "crohn's disease", "ulcerative colitis", "glaucoma", "macular degeneration", "osteoarthritis", "gout", "fibromyalgia", "endometriosis", "flu", "irritable bowel syndrome", "lupus", "psoriasis", "eczema", "rosacea", "gastritis", "acne", "tinnitus", "sleep apnea", "cataracts", "chronic kidney disease"]

    counts = {}
    df = get_chat_history_to_dataframe()
    df=df.query(
            "date >= @start_date & date <= @end_date"
        )

    for disease in diseases:
        counts[disease] = df['user_input'].str.count(disease).sum()

    dis_df = pd.DataFrame(list(counts.items()), columns=['Disease Name', 'Search Counts']).sort_values(by=['Search Counts'], ascending=False).head()

    return dis_df