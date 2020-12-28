import streamlit as st
import torch
from transformers import pipeline

#### function block ####
@st.cache
def questionAnswering(context, question):
  
  ### create pipeline
  nlp = pipeline("question-answering", 
                 model='henryk/bert-base-multilingual-cased-finetuned-dutch-squad2', 
                 tokenizer='henryk/bert-base-multilingual-cased-finetuned-dutch-squad2')
  
  result = nlp(question=question, context=context)

  return result['answer']

#### end function #####
st.title('reclassering demo')


uploaded_file = st.file_uploader('pdf_file')
#### call to the pdf to word api ####


context = st.text_area('context')

question = st.text_input('question')

if st.button('Run'):
    result = questionAnswering(context=context, question=question)
    st.write('the answer to the question is: '+ result + '.')
