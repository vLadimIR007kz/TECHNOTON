import streamlit as st
from pyarrow import null
import pandas as pd
import time
import streamlit as st
import plotly.express as px
import mysql.connector
import random
import requests
import re

import os
# from dotenv 
from dotenv import load_dotenv

load_dotenv()



gemini="Here the result from Gemini will be displayed"
chatGPT="Here the result from ChatGPT-4 will be displayed"

# gemini_p = "Gemini: percent of bias"
# chatGPT_p = "ChatGPT: percent of bias"

Yandex_URL = "https://translate.yandex.net/api/v1.5/tr.json/translate" 
Yandex_KEY = os.getenv("yandex")

@st.cache_data
def translate_to_eng(input_text: str, input_language: str):
    translated_text = ""
    if input_language!="English":
        params = {
        "key": Yandex_KEY,     
        "text": input_text,
        "lang": "kk-en" if input_language == "Kazakh" else "ru-en"
        }
        try:
            response = requests.get(Yandex_URL, params=params)
            response.raise_for_status()  # Бросает исключение, если статус не 200

            response_data = response.json()
            if 'text' in response_data:
                translated_text = ''.join(response_data['text'])
                print(translated_text)
            else:
                print("Ошибка: Ключ 'text' отсутствует в результате")
        except requests.exceptions.HTTPError as err:
            print(f"HTTP ошибка: {err}")
        except Exception as err:
            print(f"Ошибка: {err}")
    else:
        translated_text = input_text

    return translated_text

@st.cache_data
def translate_to_orig_lang(comment: str, input_language: str):
    translated_comment = ""
    if input_language!="English":
        params = {
        "key": Yandex_KEY,     
        "text": comment,
        "lang": "en-kk" if input_language == "Kazakh" else "en-ru"
        }
        try:
            response = requests.get(Yandex_URL, params=params)
            response.raise_for_status()  # Бросает исключение, если статус не 200

            response_data = response.json()
            if 'text' in response_data:
                translated_comment = ''.join(response_data['text'])
                print(translated_comment)
            else:
                print("Ошибка: Ключ 'text' отсутствует в результате")
        except requests.exceptions.HTTPError as err:
            print(f"HTTP ошибка: {err}")
        except Exception as err:
            print(f"Ошибка: {err}")
    else:
        translated_comment = comment

    return translated_comment



@st.cache_data
def get_GPT_answer(input_text: str):
    comment = ""
    url = "https://api.openai.com/v1/chat/completions"
    api_key = os.getenv("gpt")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-4", 
        "messages": [{
                "role": "user",
                "content": "Analyze this text and answer whether there is bias here (yes/no). Write a percentage from 0 to 100 of how strong the gender bias (towards women) is here. 0 - no bias at all, 100 - very strong bias, which is expressed completely throughout the text. Next, write a comment on this situation in a separate paragraph (how exactly the bias is expressed). Add explanatory phrases “Answer:” “Percentage of bias: %” and “Comment:”. The text: "+input_text,
            }],
        "max_tokens": 200  
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  

        response_data = response.json()
        print(response_data)
        if 'choices' in response_data and len(response_data['choices']) > 0:
            choice = response_data['choices'][0]
            if 'message' in choice and 'content' in choice['message']:
                text_response_data = choice['message']['content']
                print(text_response_data)
                # percent = re.search(r'\b\d{2}\b', text_response_data).group()
                # lines = response_data['choices'][0]['message']['content'].split('\n')
                # lines_without_first_two = lines[2:]
                # comment = '\n'.join(lines_without_first_two)
                comment = text_response_data

            else:
                print("Ошибка: Ключ 'message' или 'content' отсутствует в результате")
        else:
            print("Результат не содержит данных")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP ошибка: {err}")
    except Exception as err:
        print(f"Ошибка: {err}")
    
    return comment



@st.cache_data
def get_Gemini_answer(input_text: str):
    comment = ""
    Gemini_api_key = os.getenv("gemini")
    Gemini_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={Gemini_api_key}"
    headers = {"Content-Type": "application/json"}

    data = {"contents": [{"role": "user","parts": [{
                    "text": "Analyze this text and answer whether there is bias here (yes/no). Write a percentage from 0 to 100 of how strong the gender bias (towards women) is here. 0 - no bias at all, 100 - very strong bias, which is expressed completely throughout the text. Next, write a comment on this situation in a separate paragraph (how exactly the bias is expressed). Add explanatory phrases “Answer:” “Percentage of bias: %” and “Comment:”. The text: "+input_text
            }]}]}

    try:
        response = requests.post(Gemini_url, json=data, headers=headers)
        response.raise_for_status()  # Бросает исключение, если статус не 200

        result = response.json()
        print(result)
        if 'candidates' in result and len(result['candidates']) > 0:
            candidate = result['candidates'][0]
            try:
                text_result = candidate['content']['parts'][0]['text']
                print(text_result)

                # percent = re.search(r'\b\d{2}\b', text_result).group()
                # lines = text_result.split('\n')
                # lines_without_first_two = lines[2:]
                # comment = ''.join(lines_without_first_two)
                comment = text_result
            except KeyError:
                print("Ошибка: Ключ 'content' отсутствует в результате")
        else:
            print("Результат не содержит данных")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP ошибка: {err}")
    except Exception as err:
        print(f"Ошибка: {err}")

    return comment



with st.form(key='form1'):
    texting=st.text_area("Text to analyze")
    submit=st.form_submit_button("Analyze")
    language_2=st.radio("Select language",["Kazakh", "English", "Russian"])
    if submit:
        input_eng_text = translate_to_eng(texting, language_2)
        com_GPT_eng = get_GPT_answer(input_eng_text)
        com_Gem_eng = get_Gemini_answer(input_eng_text)
        gemini = translate_to_orig_lang(com_Gem_eng, language_2)
        chatGPT = translate_to_orig_lang(com_GPT_eng, language_2)

        # gemini_p = f"Gemini: {p_Gem} % of bias"
        # chatGPT_p = f"ChatGPT: {p_GPT} % of bias"
       
       

# st.write(chatGPT_p)
st.header("ChatGPT")
st.write(chatGPT)

# st.write("")
# st.write("")
# st.write("")

# st.write(gemini_p)
st.header("Gemini")
st.write(gemini)
