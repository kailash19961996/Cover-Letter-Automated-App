import streamlit as st
from io import BytesIO
from docx import Document
import fitz  # PyMuPDF
import openai
from bs4 import BeautifulSoup
import requests
from background import add_bg_from_local, show_gif_overlay, summarize_text, analyze_match, create_cv, extract_text_from_pdf, extract_text_from_docx, scrape_website, create_docx

add_bg_from_local('images/bg.jpg')

st.markdown("""
<div style='text-align: center;'>
     <h1> Cover Letter Creator </h1>
</div>
""", unsafe_allow_html=True)

# Custom CSS to force white text color
st.markdown("""
    <style>
    /* Target main content area */
    .main .block-container {
        color: white !important;
    }
    
    /* Ensure headers are white */
    .main .block-container h1, 
    .main .block-container h2, 
    .main .block-container h3, 
    .main .block-container h4, 
    .main .block-container h5, 
    .main .block-container h6 {
        color: white !important;
    }
    
    /* Make sure paragraphs and lists are white */
    .main .block-container p,
    .main .block-container li {
        color: white !important;
    }
    
    /* Style for text input (URL input) */
    .main .block-container .stTextInput input {
        background-color: black !important;
        color: white !important;
        border: 1px solid white !important;
    }

    /* Ensure the label for text areas is white */
    .main .block-container .stTextArea label,
    .main .block-container .stTextInput label {
        color: white !important;
    }
    
    /* Style for file uploader text */
    .main .block-container .stFileUploader label {
        color: white !important;
    }
    
    /* Style for buttons */
    .stButton > button {
        background-color: black !important;
        color: white !important;
        border: 1px solid white !important;
    }
    
    /* Hover effect for buttons */
    .stButton > button:hover {
        background-color: #333 !important;
        color: white !important;
        border: 1px solid white !important;
    }
            
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .stButton {
        display: flex;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Set OpenAI API key
api_key = st.secrets["openai"]["api_key"]
if api_key is None:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")
openai.api_key = api_key

if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'job_details' not in st.session_state:
    st.session_state.job_details = ""



# Step 1: Upload Resume
st.header("Step 1: Upload Your Resume")
uploaded_resume = st.file_uploader("Choose your resume file", type=["pdf", "docx"])
if uploaded_resume is not None:
    if uploaded_resume.name.endswith('.pdf'):
        resume_text = extract_text_from_pdf(uploaded_resume)
    elif uploaded_resume.name.endswith('.docx'):
        resume_text = extract_text_from_docx(uploaded_resume)
    st.session_state.resume_text = resume_text

    # if resume_text:
    #     st.text_area("Uploaded Resume", resume_text, height=200)

    # Step 2: Enter Job Details
    st.header("Step 2: Enter Job Details")
    is_gated = st.radio("Is the job posted site gated?", ("Yes (like Linkedin or Indeed)", "No (Anyone can access the site without logging in)"))

    if is_gated == "Yes (like Linkedin or Indeed)":
        # st.info("Please copy and paste the job details in the text box below.")
        st.session_state.job_details = st.text_area("Paste the job details here:")
    else:
        job_url = st.text_input("Enter the URL of the job posting:")
        if st.button("Scrape Job Details"):
            if job_url:
                soup = scrape_website(job_url)
                if soup:
                    job_details = ' '.join(p.get_text() for p in soup.find_all('p'))
                    if job_details:
                        st.session_state.job_details = job_details
                    else:
                        st.error("No text content found to summarize.")
                else:
                    st.error("Failed to retrieve the data from the specified URL.")

        if 'job_details' in st.session_state and st.session_state.job_details:
            st.session_state.job_details = st.text_area("Job Details (Enter the missing information, if any)", 
                                                        value=st.session_state.job_details, 
                                                        height=200)
    
    #Step 3: Analyze Match Potential  
    if st.button("Suggestions"):
        if st.session_state.resume_text and st.session_state.job_details:
            analysis = analyze_match(st.session_state.resume_text, st.session_state.job_details)
            st.write(analysis)
            show_gif_overlay('images/stars2.gif', duration=2)
        else:
            st.write(f"Please add the resume and job details to continue further")
        
    if st.button("Create Cover Letter"):
        if st.session_state.resume_text and st.session_state.job_details:
            new_cv = create_cv(st.session_state.resume_text, st.session_state.job_details)
            st.subheader("Generated CV")
            st.write(new_cv)
            # Create DOCX file
            docx_file = create_docx(new_cv)
            show_gif_overlay('images/stars2.gif', duration=2)

            col1, col2, col3 = st.columns([1,1,1])
            with col2:
                st.download_button(
                    label="Download Cover Letter",
                    data=docx_file,
                    file_name="cover_letter.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            
        else:
            st.write(f"Please add the resume and job details to continue further")

    
                
    