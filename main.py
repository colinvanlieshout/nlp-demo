import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import os

#our functions
from question_answering import questionAnswering
from pdftotxt import convertpdftotxt

#conda activate nlp_venv
#streamlit run main.py

initial_questions = [
    # ['Over welk ministerie wordt er gesproken?', 'Ministerie'],
    # ['Op welke datum is dit gepubliceerd?', 'Publicatie datum'],
    # ['Welke besluit is er door de afzender genomen?', 'Besluit'],
    # ['Wat is het onderwerp van het document?', 'Onderwerp'],
    # ['Door wie is de vraag gesteld?', 'Vraag gesteld door']
    # ['Over welk ministerie wordt er gesproken?'],
    # ['Op welke datum is dit gepubliceerd?'],
    # ['Welke besluit is er door de afzender genomen?'],
    # ['Wat is het onderwerp van het document?'],
    # ['Door wie is de vraag gesteld?']
    'Over welk ministerie wordt er gesproken?',
    'Op welke datum is dit gepubliceerd?',
    'Welke besluit is er door de afzender genomen?',
    'Wat is het onderwerp van het document?',
    'Door wie is de vraag gesteld?'
]

answer_df = pd.DataFrame(columns=['Vraag', 'Antwoord'])

def main():
    """
    succesful questions:
    - Over welk ministerie wordt er gesproken?
    - Op welke datum is dit gepubliceerd?

    """
    st.title('Reclassering demo')
    
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

        #4. already answer the standard questions
        answered_questions = []
        for question in initial_questions:
            result, score = questionAnswering(context=context, question=question)
            answered_questions.append([question, result, score])
            print(answered_questions)

            if len(answered_questions) == 2:
                # answered_questions.append(question)
                # print()
                df = pd.DataFrame(data = answered_questions, columns = ['Vraag', 'Antwoord', 'Score'])
                table = st.table(df)
                # table = st.table(answered_questions)
            elif len(answered_questions) > 2:
                table.add_rows([answered_questions[-1]])

        #4. ask the question
        question = st.text_input('Wat zou u graag zelf nog willen weten?')

        #5. answer the question
        if st.button('Run'):
            result, score = questionAnswering(context=context, question=question)
            st.write('Het antwoord op uw vraag is: '+ result + '.')
            st.write('Confidence: ' + score + '.')


if __name__ == "__main__":
    main()