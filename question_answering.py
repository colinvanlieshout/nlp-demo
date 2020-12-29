### imports
import torch
from transformers import pipeline
import streamlit as st


### function with a string of context and a string of question

@st.cache()#suppress_st_warning=True)
def questionAnswering(context, question):
  
  ### create pipeline
  nlp = pipeline("question-answering", 
                 model='henryk/bert-base-multilingual-cased-finetuned-dutch-squad2', 
                 tokenizer='henryk/bert-base-multilingual-cased-finetuned-dutch-squad2')
  
  result = nlp(question=question, context=context)

  return result['answer'], result['score']
