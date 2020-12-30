import streamlit as st
import pandas as pd
import os
import re
import base64

#our functions
from question_answering import questionAnswering
from pdftotxt import convertpdftotxt, text_preprocessing
from NER import create_ner_dict, find_sentences_with_entity

#conda activate nlp_venv
#streamlit run main.py

initial_questions = [
    # 'Over welk ministerie wordt er gesproken?',
    'Op welke datum is dit gepubliceerd?',
    # 'Welke besluit is er door de afzender genomen?',
    'Wat is het onderwerp van het document?',
    'Door wie is de vraag gesteld?'
]

interesting_ner_labels = {
    'Landen, steden, staten.': 'GPE',
    'Personen.' : 'PERSON',
    'Nationaliteiten en religeuze of politieke groepen.': 'NORP',
    'Gebouwen, vliegvelden, en infrastructuur.' : 'FAC',
    'Organisaties.': 'ORG',
    # 'Non-GPE locations, mountain ranges, bodies of water.': 'LOC',	
    'Objecten, voertuigen, etenswaren, etc. (Niet services).': 'PRODUCT',
    'Weer, oorlog, sport of andere evenementen.': 'EVENT', 
    #'Titles of books, songs, etc.':  'WORK_OF_ART',
    # 'Named documents made into laws.': 'LAW',
    'Taal.': 'LANGUAGE',
    'Absolute of relatieve datum of periode.':'DATE',
    'Tijd.': 'TIME',
    # 'Percentage, including ”%“.' : 'PERCENT'
    'Geld'	: 'MONEY',
    # 'Measurements, as of weight or distance.':'QUANTITY',
    # '“first”, “second”, etc.':'ORDINAL',
    # 'CARDINAL'	: 'Numerals that do not fall under another type.'
}

def main():
    """
    All streamlit code lives within the function. I tried to put as much of the other code as possible outside of it.
    For quick testing comment out 4 and 5
    """

    #this is just to make debugging easier
    print(str('-'*50))

    #styling
    set_png_as_page_bg('dqw_background.png')
    st.title('Reclassering demo')
    
    #1. upload pdf file to streamlit
    st.header("PDF verwerking")
    uploaded_file = st.file_uploader('Upload de PDF file waarin u informatie wilt zoeken')

    if uploaded_file != None:
    
        #2. convert to txt if it doesn't exist
        path_txt = 'data/txt'
        convertpdftotxt(uploaded_file.name, path_txt)
        
        #3. read txt file
        file_location = os.path.join(path_txt, uploaded_file.name.split('.')[0])+ '.txt'
        f = open(file_location, "r", encoding="utf8")
        text = f.read()
        text = text_preprocessing(text)
        
        #3. display txt in streamlit
        context = st.text_area(label = "Wij hebben uw pdf bestand gestandaardiseerd.", value = text)
        # #4. already answer the standard questions
        generate_question_table(initial_questions, context)

        # #5. ask the question
        st.header("Vragen beantoorden")
        question = st.text_input('Wat zou u graag zelf nog willen weten?')

        #6. answer the question
        if st.button('Run'):
            result, score = questionAnswering(context=context, question=question)
            st.write('Het antwoord op uw vraag is: '+ result + '.')
            st.write('Score: ' + str(round(score, 2)) + '.')

        st.header("Entiteiten extraheren en onderzoekn")
        #7. selectbox for NER labels
        NER_dict = create_ner_dict(text)    
        labels = get_selectbox_labels(NER_dict, interesting_ner_labels)  

        selection = st.selectbox('Kies de soort entiteit welke u wilt inspecteren', labels)
        label = interesting_ner_labels[selection]
           
        #8 find and display the sentences in which the words appear
        st.write(str(list(NER_dict[label].keys())))

        requested_entity = st.text_input('Welke entiteit zou u graag in zinsverband zien?')
        if len(requested_entity) != 0:
            accepted_splits = find_sentences_with_entity(requested_entity, text)

            #iterate over accepted splits and print them in a nice format
            for i, split in enumerate(accepted_splits, 1):
                st.write("*Voorbeeld ", str(i), "*")
                #make the relevant word bold
                split = split.replace(requested_entity, "**" + requested_entity + "**")
                st.write(split + '.')

def get_selectbox_labels(NER_dict, interesting_ner_labels):
    """
    finds intersection between what labels are in the dict, and what we are interested in, 
    and based on that determines the labels for the selection box
    """
    intersection = list(set(NER_dict.keys()) & set(interesting_ner_labels.values())) 

    return list({k: v for k, v in interesting_ner_labels.items() if v in intersection}.keys())

def generate_question_table(initial_questions, context):
    """
    gets a list of questions, and asks them to questionAnswering one by one based on the text (context).
    This process takes a while. Therefore, to enhance usability results are appended to the table, such that you don't have to wait too long for something to appear.
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