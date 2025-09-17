import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime as dt
import os

#configure the model
key=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=key)
model=genai.GenerativeModel('gemini-2.5-flash-lite')


st.sidebar.title(':blue[UPLOAD YOUR IMAGE HERE]')
uploaded_image=st.sidebar.file_uploader('Here',type=['jpeg','jpg','png'])
if uploaded_image:
    image=Image.open(uploaded_image)
    st.sidebar.subheader('UPLOADED IMAGE')
    st.sidebar.image(image)

# create main page
st.title(':orange[STRUCTURAL DEFECTS:] :blue[AI assisted structural defect identifier in construction buisness]')
tips = '''To use the application follow the steps below:
* Upload the image
* Click on the button to generate summary
* Click download to save the report generated'''
st.write(tips)

rep_title = st.text_input('Report Title:', None)
prep_by = st.text_input('Report Prepared by:', None)
prep_for = st.text_input('Report Prepared for:', None)

prompt = f'''Assume that you are a structural engineer. The user has provided an image 
of a structure. You need to identify the structural defects in the image and generate a report.
The report should contain the following:

It should start with the title, prepared by and prepared for details. Provided by the user.
use{rep_title} as title, {prep_by} as prepared by, {prep_for} as prepared for the same.
Also mention the current date from {dt.datetime.now().date()}

* Identify and classify the defect for exsample: cracking, sampling, corrosion, honeycombing, etc.
* There could be more than one defect in the image. Identify all the defect separartely.
* For each measure the severity of the defect as low, medium aor high. Also mention if the defect is inveitable or avoidable.
* Also mention the time before the defect leads to permament damage to the structure.
* Provide a short term and long term solution along with their estimate cost in Rupees and time to implement.
* What precationary measures can be taken to avoid such defect in future.
* The report generated should be in the word format.
* Show the data in bullet points and create table format wherever needed.
* Make sure the report must not exceed 3 pages.'''

if st.button('Generate Report'):
    if uploaded_image is None:
        st.error('Please upload an image first.')
    else:
        with st.spinner('Generating Report...'):
            response = model.generate_content([prompt, image])
            st.write(response.text)
            st.download_button(
                label = 'Downlaod Report',
                data = response.text,
                file_name = 'Structural_Defect_Report.txt',
                mime = "text/plain"
                )
