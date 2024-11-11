
import streamlit as st
from pyresparser import ResumeParser
import tempfile
import google.generativeai as genai
import os

# API key setup (should be replaced with your own key)
os.environ['GOOGLE_API_KEY'] = 'AIzaSyAESvmCIk9GI5nZIwgBK8ghZX41oUIbbew'
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Function to parse the resume and extract skills
def parse_resume(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file.read())
        temp_file_path = temp_file.name
    data = ResumeParser(temp_file_path).get_extracted_data()
    return data.get('skills', [])

# Function to generate questions for each skill
def generate_questions(skills):
    message = "Give 10 questions for each skill:\n"
    for skill in skills:
        message += f"- {skill}\n"
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(message)
    
    # Assuming the first candidate response
    return response.candidates[0].content.parts[0].text

# Streamlit app layout
st.title("Resume Skill Extractor and Question Generator")

# Upload the resume file
uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

if uploaded_file is not None:
    skills = parse_resume(uploaded_file)
    
    if skills:
        st.write("Extracted Skills:")
        st.write(skills)
        
        # Generate questions based on the extracted skills
        with st.spinner("Generating questions..."):
            questions = generate_questions(skills)
            st.subheader("Generated Questions")
            st.write(questions)
    else:
        st.write("No skills were extracted from the resume.")
else:
    st.write("Please upload a PDF resume.")
