import streamlit as st
import pandas as pd
import os
import base64

#our functions
from question_answering import questionAnswering
from pdftotxt import convertpdftotxt
from NER import create_ner_dict

#conda activate nlp_venv
#streamlit run main.py


def main():

    print('----------------------------------------------------------')

    
    #1. upload pdf file to streamlit
    uploaded_file = st.file_uploader('Upload de PDF file waarin u informatie wilt zoeken')

    if uploaded_file != None:
    
        #2. convert to txt if it doesn't exist
        path_txt = 'data/txt'
        convertpdftotxt(uploaded_file.name, path_txt)
        
        #3. read txt file
        file_location = os.path.join(path_txt, uploaded_file.name.split('.')[0])+ '.txt'
        f = open(file_location, "r", encoding="utf8")
        
        #3. display txt in streamlit
        context = st.text_area(label = "Wij hebben uw pdf bestand gestandaardiseerd.", value = f.read())

        f = open(file_location, "r", encoding="utf8")
        context2 = st.text_area(label = "Wij hebben uwbestand gestandaardiseerd.", value = f.read())


if __name__ == "__main__":
    main()