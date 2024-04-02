#Input JD
#Upload PDF
#convert PDF to Image --> Processing --> Google Gemini pro
#Prompts Template

from dotenv import load_dotenv

load_dotenv()

import os
import streamlit as st
import pdf2image
from PIL import Image
import io
import base64
import google.generativeai as genai


genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

#Taking some content and giving it to the model based on the prompt
#Prompt describes what the model needs to do
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt]) 
    return response.text

#convert PDF to Image               
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]
        #convert to bytes
        img_byte_array = io.BytesIO()
        first_page.save(img_byte_array, format = 'JPEG')
        img_byte_array = img_byte_array.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data" : base64.b64encode(img_byte_array).decode() #encode image to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No PDF file uploaded")
    

#Streamlit App
    
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS System")
input_text = st.text_area("Job Description: ",key = "input")
uploaded_file = st.file_uploader("Upload your Resume(PDF)", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me about the resume")

#submit2 = st.button("How can I Improvise my skills")

#submit3 = st.button("What are the keywords that are missing in the resume")

submit2 = st.button("Percentage Match")

                    
input_prompt1 = """You are an experienced Technical Human Resource Manager in the field of Data Science, Machine Learning, Data Engineering, Data Analyst
    your task is to review the provided resume against the job description for this profiles. 
    Please share your professional evaluation on whether the candidate's profile aligns with the role. 
    Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements"""

input_prompt2 = """
    You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science, Machine Learning,Data Engineering, Data Analyst and deep ATS functionality, 
    Your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
    the job description. First the output should come as percentage and then keywords missing and last final thoughts."""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is: ")
        st.write(response)
    else:
        st.write("Please uplaod the resume")
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is: ")
        st.write(response)
    else:
        st.write('Please upload the resume')
            