"""
🚀 AI Job Tailor 🚀 

My new AI-powered app. An app designed to make creating cover letters a breeze! 🌟

With just a few simple steps, you can generate a personalized cover letter tailored to your job application:

1️⃣ Upload your resume (PDF or DOCX)
2️⃣ Provide job details (via URL or copy-paste)

Our app will generate suggestions, and if you're happy with them, you can instantly download your cover letter 
in DOCX format for easy editing and final touches.
"""

import streamlit as st
from io import BytesIO
from docx import Document
import fitz  # PyMuPDF
import openai
from bs4 import BeautifulSoup
import requests
from background import add_bg_from_local, show_gif_overlay, analyze_match, add_adjustment, create_cv, extract_text_from_pdf, extract_text_from_docx, scrape_website, create_docx

add_bg_from_local('images/bg5.jpg')

st.markdown("""
<div style='text-align: center;'>
     <h1> AI Job Tailor </h1>
</div>
""", unsafe_allow_html=True)

linkedin = "https://raw.githubusercontent.com/kailash19961996/icons-and-images/main/linkedin.gif"
github =   "https://raw.githubusercontent.com/kailash19961996/icons-and-images/main/gitcolor.gif"
Youtube =  "https://raw.githubusercontent.com/kailash19961996/icons-and-images/main/371907120_YOUTUBE_ICON_TRANSPARENT_1080.gif"
email =    "https://raw.githubusercontent.com/kailash19961996/icons-and-images/main/emails33.gif"
website =  "https://raw.githubusercontent.com/kailash19961996/icons-and-images/main/www.gif"

coll1,coll2,coll3 = st.columns(3)
with coll2:
    st.write(
        f"""
            <div style='display: flex; align-items: center;'>
            <a href = 'https://kailash.london/'><img src='{website}' style='width: 35px; height: 35px; margin-right: 25px;'></a>
            <a href = 'https://www.youtube.com/@kailashbalasubramaniyam2449/videos'><img src='{Youtube}' style='width: 28px; height: 28px; margin-right: 25px;'></a>
            <a href = 'https://www.linkedin.com/in/kailash-kumar-balasubramaniyam-62b075184'><img src='{linkedin}' style='width: 35px; height: 35px; margin-right: 25px;'></a>
            <a href = 'https://github.com/kailash19961996'><img src='{github}' style='width: 28px; height: 32px; margin-right: 32px;'></a>
            <a href = 'mailto:kailash.balasubramaniyam@gmail.com''><img src='{email}' style='width: 31px; height: 31px; margin-right: 25px;'></a>
        </div>""", unsafe_allow_html=True,)


st.markdown("""
<div style='text-align: center;'>
     <h4>60-Second Intro</h4>
</div>
""", unsafe_allow_html=True)

video_id = "5G2mpR0QvN0?si=RM0P4ids15yF4fwH"
youtube_embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=0"
st.markdown(f"""
    <style>
        .video-outer-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            padding-top: 1px; 
        }}
        .video-container {{
            position: relative;
            width: 50%;
            padding-bottom: 28.125%;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .video-container iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border-radius: 15px;
        }}
    </style>
    <div class="video-outer-container">
        <div class="video-container">
            <iframe src="{youtube_embed_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
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

    /* Style for download button */
    .stDownloadButton > button {
        background-color: black !important;
        color: white !important;
        border: 1px solid white !important;
    }
    
    /* Hover effect for download button */
    .stDownloadButton > button:hover {
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

# Initialize session state variables
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'job_details' not in st.session_state:
    st.session_state.job_details = ""
if 'new_cv' not in st.session_state:
    st.session_state.new_cv = ""
if 'adjustment_text' not in st.session_state:
    st.session_state.adjustment_text = ""
if 'adjustment_CV' not in st.session_state:
    st.session_state.adjustment_CV = ""
if 'analysis' not in st.session_state:
    st.session_state.analysis = ""
if 'job_scrape_error' not in st.session_state:
    st.session_state.job_scrape_error = False
if 'cover_letter_generated' not in st.session_state:
    st.session_state.cover_letter_generated = False
if 'happy_clicked' not in st.session_state:
    st.session_state.happy_clicked = False
if 'not_happy_clicked' not in st.session_state:
    st.session_state.not_happy_clicked = False

# Step 1: Upload Resume
st.header("Step 1: Upload Your Resume")
uploaded_resume = st.file_uploader("Choose your resume file", type=["pdf", "docx"])
if uploaded_resume is not None:
    if uploaded_resume.name.endswith('.pdf'):
        resume_text = extract_text_from_pdf(uploaded_resume)
    elif uploaded_resume.name.endswith('.docx'):
        resume_text = extract_text_from_docx(uploaded_resume)
    st.session_state.resume_text = resume_text

# Step 2: Enter Job Details
st.header("Step 2: Enter Job Details")
is_gated = st.radio("Is the job posted site gated?", ("Yes (like Linkedin or Indeed)", "No (Anyone can access the site without logging in)"))

if is_gated == "Yes (like Linkedin or Indeed)":
    st.session_state.job_details = st.text_area("Paste the job details here:", value=st.session_state.job_details)
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
                    st.session_state.job_scrape_error = True
            else:
                st.session_state.job_scrape_error = True

    if st.session_state.job_scrape_error:
        st.error("Failed to retrieve the data from the specified URL.")
    
    if st.session_state.job_details:
        st.session_state.job_details = st.text_area("Job Details (Enter the missing information, if any)", 
                                                    value=st.session_state.job_details, 
                                                    height=200)

# Step 3: Analyze Match Potential  
with st.form(key='suggestions_form'):
    suggestions_button = st.form_submit_button("Suggestions")
    if suggestions_button:
        if st.session_state.resume_text and st.session_state.job_details:
            st.session_state.analysis = analyze_match(st.session_state.resume_text, st.session_state.job_details)
            show_gif_overlay('images/stars2.gif', duration=2)
        else:
            st.write("Please add the resume and job details to continue further")

# Display analysis outside the form
if st.session_state.analysis:
    st.write(st.session_state.analysis)

# Step 4: Create Cover Letter
with st.form(key='create_cv_form'):
    create_cv_button = st.form_submit_button("Create Cover Letter")
    if create_cv_button:
        if st.session_state.resume_text and st.session_state.job_details:
            st.session_state.new_cv = create_cv(st.session_state.resume_text, st.session_state.job_details)
            st.session_state.cover_letter_generated = True
        else:
            st.write("Please add the resume and job details to continue further")

# Display generated cover letter and options
if st.session_state.cover_letter_generated:
    st.subheader("Generated Cover Letter")
    st.write(st.session_state.new_cv)
    
    coll1, coll2 = st.columns([1,1])
    with coll1:
        if st.button("Happy 👍🏻"):
            st.session_state.happy_clicked = True
            st.session_state.not_happy_clicked = False
    with coll2:
        if st.button("Not happy 👎🏻"):
            st.session_state.not_happy_clicked = True
            st.session_state.happy_clicked = False

    # Show download button if "Happy" was clicked
    if st.session_state.happy_clicked:
        docx_file = create_docx(st.session_state.new_cv)
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            st.download_button(
                label="Download Cover Letter",
                data=docx_file,
                file_name="cover_letter.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            show_gif_overlay('images/stars2.gif', duration=2)

    # Show adjustment text area if "Not happy" was clicked
    if st.session_state.not_happy_clicked:
        st.session_state.adjustment_text = st.text_area("Let me know what you want to change:", value=st.session_state.adjustment_text)
        if st.button("Apply Adjustments"):
            st.subheader("Adjusted Cover Letter")
            st.session_state.adjustment_CV = add_adjustment(st.session_state.resume_text, st.session_state.job_details, st.session_state.new_cv, st.session_state.adjustment_text)
            st.write(st.session_state.adjustment_CV)
            
        # Always show the download button for the adjusted CV
        if st.session_state.adjustment_CV:
            docx_file = create_docx(st.session_state.adjustment_CV)
            col1, col2, col3 = st.columns([1,1,1])
            with col2:
                st.download_button(
                    label="Download Final Cover Letter",
                    data=docx_file,
                    file_name="cover_letter.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

st.markdown("""
<div style='text-align: center;'>
    Built by <a href="https://kailash.london/">Kai</a>. Like this? <a href="https://kailash.london/">Hire me!</a>
</div>
""", unsafe_allow_html=True)
