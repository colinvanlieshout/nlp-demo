import streamlit as st
import pandas as pd
import os
import base64
import re

#our functions
from question_answering import questionAnswering
from pdftotxt import convertpdftotxt
from NER import create_ner_dict

#conda activate nlp_venv
#streamlit run main.py

initial_questions = [
    'Over welk ministerie wordt er gesproken?',
    'Op welke datum is dit gepubliceerd?',
    'Welke besluit is er door de afzender genomen?',
    'Wat is het onderwerp van het document?',
    'Door wie is de vraag gesteld?'
]

def main():
    """
    """

    #this is just to make debugging easier
    print(str('-'*50))
    set_png_as_page_bg('dqw_background.png')
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
        # #4. already answer the standard questions
        generate_question_table(initial_questions, context)

        # #4. ask the question
        question = st.text_input('Wat zou u graag zelf nog willen weten?')

        # #5. answer the question
        if st.button('Run'):
            result, score = questionAnswering(context=context, question=question)
            st.write('Het antwoord op uw vraag is: '+ result + '.')
            st.write('Confidence: ' + str(score) + '.')

        # #6. selectbox for NER labels
        #this thing cost me a lot of debuggin time. Apparently you cannot use f.read() twice without reloading the file (damnit)
        f = open(file_location, "r", encoding="utf8")
        text = f.read()
        NER_dict = create_ner_dict(text)

        labels = list(NER_dict.keys())
        selection = st.selectbox('Kies de soort entiteit welke u wilt inspecteren', labels)
           
        #7 find all occurences of the chosen word, with surrounding words
        st.write(str(list(NER_dict[selection].keys())))

        question2 = st.text_input('Welke entiteit zou u graag in zinsverband zien?')

        if len(question2) != 0:
            for m in re.finditer(question2, text):
                # print(m.start())

                accepted_splits = []

                #goal here is to get the sentence itself instead of cutting it off in the middle, doesn't work perfectly yet
                search_area = text[m.start()-300:m.end()+300]
                splits = search_area.split('.')
                # splits = splits[1:-1]
                for split in splits:
                    if question2 in split:
                        if split not in accepted_splits:
                            # st.write(split)
                            accepted_splits.append(split)
                
                accepted_splits = list(set(accepted_splits))
                
                for split in accepted_splits:
                    st.write(split)
                print(accepted_splits)

                st.write('==============')



def generate_question_table(initial_questions, context):
    """
    gets a list of questions, and asks them to questionAnswering one by one based on the text (context).
    To enhance usability results are appended to the table, such that you don't have to wait too long for something to appear.
    """
    answered_questions = []
    for question in initial_questions:
        result, score = questionAnswering(context=context, question=question)
        answered_questions.append([question, result, score])

        #starting at two, because at one it transposes the table and that doesn't work well
        if len(answered_questions) == 2:
            #starting off with a dataframe as that seems the only way to get table headers in
            df = pd.DataFrame(data = answered_questions, columns = ['Vraag', 'Antwoord', 'Score'])
            df.index += 1
            table = st.table(df)
        elif len(answered_questions) > 2:
            #add new rows
            table.add_rows([answered_questions[-1]])

def get_base64_of_bin_file(bin_file):
    """
    function to read png file 
    ----------
    bin_file: png -> the background image in local folder
    """
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    """
    function to display png as bg
    ----------
    png_file: png -> the background image in local folder
    """
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    background-repeat: no-repeat;
    }
    </style>
    ''' % bin_str
    # background-position-y: 100px;
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

if __name__ == "__main__":
    main()