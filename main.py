import speech_recognition as sr
import logging
import os
import google.generativeai as genai
import streamlit as st
from gtts import gTTS



#This is logger for the application
LOG_DIR = "logs"
LOG_FILE_NAME = "application.log"    # .log file is used. it recommended

os.makedirs(LOG_DIR, exist_ok = True)   #exist_ok =TRUE ensures that if a directory already exits it will not throw any error  #.makedirs is use to make a directory

# log_path = LOG_DIR + "/" + LOG_FILE_NAME  OR

log_path = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename = log_path,
    format = '[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO
)



def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said : {query}\n")
    except Exception as e:
        logging.info(e)
        print("Say that again please")
        return "None"
    return query

def text_to_speech(text):
    ttx = gTTS(text=text, lang="en")
    ttx.save("speech.mp3")
    
    
def gemini_model(user_input):
    genai.configure(api_key = "Your-own-API-Key")  #either you can do  this or do make file .env to set GOOGLE_API_KEY
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(user_input)
    results = response.text
    return results



# text = takeCommand()
# re = gemini_model(text)
# text_to_speech(re)


def main():
    st.title("Multilingual-AI-Assistant")
    if st.button("Ask me anything"):
        with st.spinner("Listening..."):
            text = takeCommand()
            re = gemini_model(text)
            text_to_speech(re)  
            
            
            audio_file = open("speech.mp3", "rb")  
            audio_bytes = audio_file.read()
            
            st.text_area(label= "Response:", value = re, height=350)
            st.audio(audio_bytes, format= "audio/mp3")
            st.download_button(label= "Download Speech", data=audio_bytes, file_name= "speech.mp3", mime="audio/mp3")
    

main()
