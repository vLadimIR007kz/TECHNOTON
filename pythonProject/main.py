import streamlit as st
from pyarrow import null
import pandas as pd
import time
import streamlit as st
import plotly.express as px
import mysql.connector
import random
connection=mysql.connector.connect(host="mysql-48983cc-nazarenko-32e6.a.aivencloud.com",port=17657, user="avnadmin", password="AVNS_Dal6Z8qW-7uIbLWO5ze", ssl_ca="ca.pem")

copilot="Here the result from Copilot will be displayed"
chatGPT="Here the result from ChatGpt will be displayed"




with st.form(key='form1'):
    texting=st.text_area("Text to analyze")
    submit=st.form_submit_button("Analyze")
    language_2=st.radio("Select language",["Eng","Kaz", "Rus"])
    if submit:
        cursor=connection.cursor()
        idor=random.randint(1,999)
        cursor.execute("USE defaultdb")
        cursor.execute("INSERT INTO our_information Values(%s,%s,%s,%s,%s,%s,%s,%s)", (idor,texting,language_2,"0","0","0","0","0"))
        #st.write(cursor.execute("SELECT * FROM text"))
        cursor.close()


st.write(chatGPT)
st.write(copilot)
