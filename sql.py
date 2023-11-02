import mysql.connector
import streamlit as st
import pandas as pd

conn=mysql.connector.connect(
   host="localhost",
   port="3306",
   user="root",
   passwd="aB@S1Q2l3",
   db="medibot"
)
c=conn.cursor()


def view_all_data():
    c.execute('''SELECT *
                FROM medibot_bookings 
                LEFT JOIN medibot_doctor 
                USING (doctor_id)
                LEFT JOIN medibot_patient
                ON medibot_bookings.patient_id = medibot_patient.userID
                ORDER BY day ASC;''')
    data=c.fetchall()
    return data

def get_specializations():
    c.execute('''SELECT DISTINCT(speciality)
                FROM medibot_doctor;
                ''')
    data=c.fetchall()
    specializations = []
    for i in data:
        specializations.append(i[0].lower())
    return specializations

def get_doctors():
    c.execute('''SELECT DISTINCT(doctor_name)
                FROM medibot_doctor;
                ''')
    data=c.fetchall()
    doctors = []
    for i in data:
        doctors.append(i[0].lower())
    return doctors

def get_sessions():
    c.execute('''SELECT *
                FROM medibot_login;
                ''')
    data=c.fetchall()
    d = pd.DataFrame(data, columns = ['sessionID', 'userID', 'login_time'])
    d['date'] = d['login_time'].dt.date

    time_categories = {
    '12 am - 3 am': range(0, 3),
    '3 am - 6 am': range(3, 6),
    '6 am - 9 am': range(6, 9),
    '9 am - 12 pm': range(9, 12),
    '12 pm - 3 pm': range(12, 15),
    '3 pm - 6 pm': range(15, 18),
    '6 pm - 9 pm': range(18, 21),
    '9 pm - 12 am': range(21, 24),
    }
    d['time_category'] = d['login_time'].dt.hour.apply(lambda x: next((category for category, hours in time_categories.items() if x in hours), None))
    
    return d

print(get_sessions())