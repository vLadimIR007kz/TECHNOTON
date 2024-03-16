import pymysql
import streamlit as st
from pyarrow import null
import pandas as pd
import time
import streamlit as st
import plotly.express as px
import mysql.connector
import random

from sqlalchemy import create_engine

copilot="Here the result from Copilot will be displayed"
chatGPT="Here the result from ChatGpt will be displayed"

with st.form(key='form1'):
    texting=st.text_area("Text to analyze")
    submit=st.form_submit_button("Analyze")
    language_2=st.radio("Select language",["Eng","Kaz", "Rus"])
    if submit:
        st.write(language_2)
        st.write(texting)


st.write(chatGPT)
st.write(copilot)
