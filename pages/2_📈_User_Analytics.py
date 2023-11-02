import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from fs import * 
from sql import *
import matplotlib.pyplot as plt
import numpy as np
from dateutil.relativedelta import relativedelta


st.set_page_config(page_title="Dashboard",page_icon="📈",layout="wide")
st.markdown("<h1 style='text-align: center; color: rgb(204, 238, 255);'>User Analytics Dashboard</h1>", unsafe_allow_html=True)

st.sidebar.success("You can navigate between above pages.")

df = get_chat_history_to_dataframe()
df_sessions = get_sessions()

st.sidebar.header("Filter Details Here")

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
start_date = st.sidebar.date_input('Start date', today- relativedelta(months=5))
end_date = st.sidebar.date_input('End date', tomorrow)
if start_date > end_date:
    st.error('Error: End date must not fall before start date.')
 
df_selection=df.query(
            "date >= @start_date & date <= @end_date"
        )

df_session_selection=df_sessions.query(
            "date >= @start_date & date <= @end_date"
        )

user_count = df_selection['user_id'].nunique()
chat_count = df_selection['chat_id'].nunique()
session_counts = df_session_selection['sessionID'].nunique()
chat_c_ratio = chat_count / session_counts * 100


total1,total2,total3,total4=st.columns(4,gap='large')
with total1:
    #st.info('Total Appointments',icon="📌")
    st.metric(label="User Count",value=f"{user_count:,.0f}")

with total2:
     #st.info('Total Cancellations',icon="📌")
    st.metric(label="Chat Count",value=f"{chat_count:,.0f}")

with total3:
#     st.info('Average',icon="📌")
    st.metric(label="Session Count",value=f"{session_counts:,.0f}")

with total4:
#     st.info('Central Earnings',icon="📌")
    st.metric(label="Chat Conversion Ratio",value=f"{chat_c_ratio:,.2f}%")


st.markdown("##")
st.markdown("##")

graph1, graph2, graph3 =st.columns(3)
with graph1:
    st.markdown("<h3 style='text-align: center; color: rgb(204, 238, 255);'>Top Searched Specialities</h3>", unsafe_allow_html=True)
    st.table(get_speciality_counts(start_date, end_date).reset_index(drop=True))


with graph2:
    st.markdown("<h3 style='text-align: center; color: rgb(204, 238, 255);'>Top Searched Doctors</h3>", unsafe_allow_html=True)
    st.table(get_doctor_counts(start_date, end_date).reset_index(drop=True))

with graph3:
    st.markdown("<h3 style='text-align: center; color: rgb(204, 238, 255);'>Top Searched Diseases</h3>", unsafe_allow_html=True)
    st.table(get_disease_counts(start_date, end_date).reset_index(drop=True))


st.markdown("##")
st.markdown("##")

st.markdown("<h3 style='text-align: center; color: rgb(204, 238, 255);'>User Engagement Breakdown</h3>", unsafe_allow_html=True)
st.bar_chart(df_session_selection.groupby(by = ['time_category'])['sessionID'].count(), height = 330, color = '#008ae6')


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
