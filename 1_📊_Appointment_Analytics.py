import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from sql import * 
import matplotlib.pyplot as plt
import numpy as np
from dateutil.relativedelta import relativedelta


st.set_page_config(page_title="Dashboard",page_icon="🏥",layout="wide")
st.markdown("<h1 style='text-align: center; color: rgb(204, 238, 255);'>Appointment Analytics Dashboard</h1>", unsafe_allow_html=True)

st.sidebar.success("You can navigate between above pages.")

table = view_all_data()
df = pd.DataFrame(table, columns=['doctor_id', 'appointment_ID', 'day', 'book', 'patient_id', 'doctor_name', 'speciality'
                           , 'userID', 'username', 'first_name', 'last_name', 'phone_number', 'email', 'created_at'])


st.sidebar.header("Filter Details Here")

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
start_date = st.sidebar.date_input('Start date', today - relativedelta(months=5))
end_date = st.sidebar.date_input('End date', tomorrow)
if start_date > end_date:
    st.error('Error: End date must not fall before start date.')

speciality = st.sidebar.multiselect(
    "Select Speciality",
     options=df["speciality"].unique(),
     default= None,
)

all_specialities = st.sidebar.checkbox("Select all specialities")

doctor = st.sidebar.multiselect(
    "Select Doctor",
     options=df['doctor_name'].unique(),
     default=None,
)

all_doctors = st.sidebar.checkbox("Select all doctors")
 
if all_specialities:
    if all_doctors:
        df_selection=df.query(
            "day >= @start_date & day <= @end_date"
        )
    else:
        df_selection=df.query(
            "day >= @start_date & day <= @end_date & doctor_name == @doctor"
        )
else:
    if all_doctors:
        df_selection=df.query(
            "day >= @start_date & day <= @end_date & speciality == @speciality"
        )
    else:
        df_selection=df.query(
            "day >= @start_date & day <= @end_date & speciality == @speciality & doctor_name == @doctor"
        )

total_appointments = float(len(df_selection[df_selection['book'] == 1]))
total_cancellations = float(len(df_selection[df_selection['book'] == 0]))
total_patients = float(len(df_selection['patient_id'].unique()))
total_doctors = float(len(df_selection['doctor_id'].unique()))


total1,total2,total3,total4=st.columns(4,gap='large')
with total1:
    st.metric(label="Appointments",value=f"{total_appointments:,.0f}")

with total2:
    st.metric(label="Cancellations",value=f"{total_cancellations:,.0f}")

with total3:
    st.metric(label="Patients",value=f"{total_patients:,.0f}")

with total4:
    st.metric(label="Doctors",value=f"{total_doctors:,.0f}")

st.markdown("##")
st.markdown("##")

graph1, graph2 =st.columns(2)
with graph1:
    st.markdown("<h3 style='text-align: center; color: rgb(204, 238, 255);'>Appointments based on Speciality</h3>", unsafe_allow_html=True)
    st.bar_chart(df_selection.groupby(by = ['speciality'])['appointment_ID'].count(), height = 330, color = '#008ae6')


with graph2:
    st.markdown("<h3 style='text-align: center; color: rgb(204, 238, 255);'>Daily Appointment Counts</h3>", unsafe_allow_html=True)
    st.line_chart(df_selection.groupby(by = ['day'])['appointment_ID'].count(), height = 250, color = '#008ae6')

hide_st_style=""" 

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""
st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)

st.markdown("""
<style>
div[data-testid="metric-container"] {
   background-color: rgba(0, 170, 255, 0.7);
   border: 1px solid rgb(28, 131, 225);
   padding: 5% 5% 5% 10%;
   border-radius: 5px;
   color: white;
   overflow-wrap: break-word;
}

/* breakline for metric text         */
div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: white;
}
</style>
"""
, unsafe_allow_html=True)