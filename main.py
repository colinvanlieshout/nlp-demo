import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import os

#our functions
from question_answering import questionAnswering
from pdftotxt import convertpdftotxt

def main():
    """
    succesful questions:
    - Over welk ministerie wordt er gesproken?
    - Op welke datum is dit gepubliceerd?

    """
    st.title('Reclassering demo')
    
    #1. upload pdf file to streamlit
    uploaded_file = st.file_uploader('pdf_file')
    print(uploaded_file.name)
    
    #2. convert to txt if it doesn't exist
    path_txt = 'data/txt'
    convertpdftotxt(uploaded_file.name, path_txt)
    
    #3. read txt file
    file_location = os.path.join(path_txt, uploaded_file.name.split('.')[0])+ '.txt'
    f = open(file_location, "r", encoding="utf8")
    
    #3. display txt in streamlit
    context = st.text_area(label = "Wij hebben uw pdf bestand gestandaardiseerd.", value = f.read())

    #4. ask the question
    question = st.text_input('Wat zou u graag willen weten?')

    #5. answer the question
    if st.button('Run'):
        result, score = questionAnswering(context=context, question=question)
        st.write('Het antwoord op uw vraag is: '+ result + '.')
        st.write('Confidence: ' + score + '.')


if __name__ == "__main__":
    main()