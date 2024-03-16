import requests
import re

URL = "https://translate.yandex.net/api/v1.5/tr.json/translate" 
KEY = "trnsl.1.1.20240316T053700Z.6b41ba660d7d2ea6.da3c59d45adab52b10560d7b5b423a93c523d652" 


def translate_to_eng(input_text: str, input_language: str):
    if input_language!="en":
        params = {
        "key": KEY,     
        "text": input_text,
        "lang": input_language+"-en"
        }
        response = requests.get(URL, params=params)
        translated_text = ''.join(response.json()['text'])
    else:
        translated_text = input_text

    return translated_text


def translate_to_orig_lang(comment: str, input_language: str):
    if input_language!="en":
        params = {
        "key": KEY,     
        "text": comment,
        "lang": "en-"+input_language
        }
        response = requests.get(URL, params=params)
        translated_comment = ''.join(response.json()['text'])
    else:
        translated_comment = comment

    return translated_comment

# print(translate_to_eng("привет! это текст был на русском", "ru"))
# print(translate_to_eng("Сәлем! бұл мәтін қазақ тілінде болды", "kk"))
# print(translate_to_orig_lang("hello! this text was in English", "kk"))
# print(translate_to_orig_lang("hello! this text was in English", "ru"))








def get_GPT_answer(input_text: str):
    url = "https://api.openai.com/v1/chat/completions"
    api_key = "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"  
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "gpt-4", 
        "messages": [{
                "role": "user",
                "content": "Analyze this text and write a percentage from 0 to 100 of how strong the gender bias (towards women) is here. Number only, NO additional text or percent sign (%). 0 - no bias at all, 100 - very strong bias, which is expressed completely throughout the text. Next, write a comment on this situation in a separate paragraph (how exactly the bias is expressed). The text: "+input_text,
            }],
        "max_tokens": 200  
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    # return response_data['choices'][0]['message']['content']
    percent = re.search(r'\b\d{2}\b', response_data['choices'][0]['message']['content']).group()
    
    lines = response_data['choices'][0]['message']['content'].split('\n')
    lines_without_first_two = lines[2:]
    comment = '\n'.join(lines_without_first_two)
    return percent, comment



# prompt = """ 
# Mia (looks determined): "...and I can speak basic Spanish too! It would be great to connect with our Latino customers. Plus, I'm a total people person, always making sure everyone has a positive experience."
# Brian (barely glancing at her, mutters): "Uh-huh, that's nice. Listen, college kid, this isn't exactly rocket science. You pour coffee, you take orders, maybe wipe down a table or two. Don't need any fancy languages or people-schmoozing for that."
# Mia:"Actually, customer service is a big part of the job. Making people feel welcome and creating a positive atmosphere is key to keeping them coming back. I can handle the coffee-making part easily, but I think I can bring a lot more to the table."
# Brian (scoffs, finally meeting her eyes): "Look, sweetheart, this job isn't for overthinkers. It's perfect for high school kids who need some spending money. You know, someone with a bit more... free time. You wouldn't want to be stuck here all day, would you? You girls have better things to do, right?"
# Mia (sits up straight, her smile gone): "With all due respect, Mr. Jones, I can assure you I'm more than capable of handling the responsibilities of this job, regardless of my gender. In fact, I'm looking for a stable position to build a career, not just some pocket money. If your ideal employee is someone who underestimates women, then perhaps this isn't the opportunity for me."
# """
# perc, comm = get_GPT_answer(prompt)
# print(perc)
# print(comm)




def get_Gemini_answer(input_text: str):
    Gemini_api_key = "AIzaSyAdk1BzcCcR6dfuXbNFwL5F43zyKYi2nFE"
    Gemini_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={Gemini_api_key}"
    headers = {"Content-Type": "application/json"}

    data = {"contents": [{"role": "user","parts": [{
                    "text": "Analyze this text and write a percentage from 0 to 100 of how strong the gender bias (towards women) is here. Number only, NO additional text or percent sign (%). 0 - no bias at all, 100 - very strong bias, which is expressed completely throughout the text. Next, write a comment on this situation in a separate paragraph (how exactly the bias is expressed). The text: "+input_text
            }]}]}

    try:
        response = requests.post(Gemini_url, json=data, headers=headers)
        response.raise_for_status()  # Бросает исключение, если статус не 200

        result = response.json()
        if 'candidates' in result and len(result['candidates']) > 0:
            candidate = result['candidates'][0]
            try:
                text_result = candidate['content']['parts'][0]['text']
                print(text_result)

                percent = re.search(r'\b\d{2}\b', text_result).group()
                lines = text_result.split('\n')
                lines_without_first_two = lines[2:]
                comment = ''.join(lines_without_first_two)

            except KeyError:
                print("Ошибка: Ключ 'content' отсутствует в результате")
                percent = ""
                comment = ""
        else:
            print("Результат не содержит данных")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP ошибка: {err}")
    except Exception as err:
        print(f"Ошибка: {err}")

    return percent, comment

prompt = """ 
Mia (looks determined): "...and I can speak basic Spanish too! It would be great to connect with our Latino customers. Plus, I'm a total people person, always making sure everyone has a positive experience."
Brian (barely glancing at her, mutters): "Uh-huh, that's nice. Listen, college kid, this isn't exactly rocket science. You pour coffee, you take orders, maybe wipe down a table or two. Don't need any fancy languages or people-schmoozing for that."
Mia:"Actually, customer service is a big part of the job. Making people feel welcome and creating a positive atmosphere is key to keeping them coming back. I can handle the coffee-making part easily, but I think I can bring a lot more to the table."
Brian (scoffs, finally meeting her eyes): "Look, sweetheart, this job isn't for overthinkers. It's perfect for high school kids who need some spending money. You know, someone with a bit more... free time. You wouldn't want to be stuck here all day, would you? You girls have better things to do, right?"
Mia (sits up straight, her smile gone): "With all due respect, Mr. Jones, I can assure you I'm more than capable of handling the responsibilities of this job, regardless of my gender. In fact, I'm looking for a stable position to build a career, not just some pocket money. If your ideal employee is someone who underestimates women, then perhaps this isn't the opportunity for me."
"""
perc, comm = get_Gemini_answer(prompt)
print(comm)

