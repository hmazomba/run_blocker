import os
from dotenv import load_dotenv

load_dotenv()
cohere_api_key= os.getenv('COHERE_API_KEY')

from langchain.llms import Cohere
cohere_llm = Cohere(cohere_api_key=cohere_api_key, verbose=True)

import streamlit as st

def generate_response(input_text):
  llm = cohere_llm
  st.info(llm(input_text))

with st.form('my_form'):
  text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
  submitted = st.form_submit_button('Submit')
  if submitted:
    generate_response(text)  