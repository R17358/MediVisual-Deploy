import streamlit as st
import time
import textGenModel
import re
from PIL import Image
import datetime
import cv2
import numpy as np
import requests
import PyPDF2
import pytesseract
from imgGen import ImageGenerator as IG

imageSwitch = False

def stream_data(data, delay: float = 0.1):
    placeholder = st.empty()  # Create an empty placeholder to update text
    text = ""
    for word in data.split():
        text += word + " "
        placeholder.markdown(f"""{text}""", unsafe_allow_html= True)  # Display progressively in markdown
        time.sleep(delay)

def recognize_text(image):
    try:
        image = np.array(image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, lang='hin+eng')            # lang='hin+eng'
        return text.strip()
    except Exception as e:
        st.error(e)
        return None

def process(prompt):
    if hindi:
        prompt+= "Use hindi language for response"
    prompt = f"""This is a medical Report of a victim as following text form: {prompt}.You have to explain 
    the report in simple way so anyone can understand it but give complete information. but write everything in html format so I can display it 
    in streamlit markdown. you have to use the format as follow and write these all content: <h2>name of patient</h2><br>
    <h2> the most possible disease name</h2><br><br>
    <li in bold>the factors which are less or more in simple way</li><br>
    <li>diet</li>
    <li>precautions</li>
    <p>and other important advices</p>You can give suitable styles and colors. use visible light font colours such as bluish green, yellow, orange, rgb(56 189 248), #1deae3,  #0fef29 .don't use other colour than these. and fonts for better present.
    use font size of 20px. provide bits of spaces between 2 sentences. Don't write anything else and don't repeat anything. Don't use asteriks"""
   
    response = textGenModel.chatResponse(prompt)
    stream_data(response.text, delay=0.02)
    if imageSwitch:
        img_prompt_list = []
        img_prompt = f"""Generate best 3D image generating prompts for disease and body parts mentioned in {response}. 
        Don't write anything else. only write single prompt"""
        for i in range (0,3):
            Iprompt = textGenModel.chatResponse(img_prompt)
            img_prompt_list.append(Iprompt.text)

        with st.spinner("Image Generating...."):
            for p in img_prompt_list:
                img, f = IG(p)
                st.image(img)


def is_image(file_path):
    try:
        img = Image.open(file_path)
        img.verify()
        return True
    except (IOError, SyntaxError):
        return False

def read_pdf(file):
    
    reader = PyPDF2.PdfReader(file)
    text = ''
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text

st.title("MediVisual")
st.divider()
hindi = st.toggle("Hindi")
imageSwitch = st.toggle("Images")
st.divider()
sidebar = st.sidebar
sidebar.title("Menu")
file = sidebar.file_uploader("Choose a file")

home, health, about, contact = st.tabs(["Home", "Health tips", "About", "Contact"])

with home:
    st.subheader("Medical ChatBot")
    prompt = home.text_input("Ask Something...", placeholder="Key of Knowledge...")

    if prompt:
        go = True
        with home.chat_message("user"):
            home.markdown(f"""<h3>You: {prompt}</h3>""", unsafe_allow_html=True)

        with st.spinner("Thinking...."):
            if prompt:
                go = True     
                home, right = st.columns(2)
                with home:
                    if st.button("ResetChat"):
                        go = False 
                with right:
                    if st.button("RestartChat"):
                        go = True
                process(prompt)          

    elif file:
        go = True
        placeholder = sidebar.empty()
        if is_image(file):
            file = Image.open(file)
            placeholder.success("File Uploaded successfully")
            time.sleep(1)
            placeholder.empty()
            home.image(file, caption='Uploaded File.', width= 500)
            with st.spinner("Thinking...."):
                text = recognize_text(file)
                process(text)
        else:
            text = read_pdf(file)
            placeholder.success("File Uploaded successfully")
            time.sleep(1)
            placeholder.empty()
            with st.spinner("Thinking...."):
                process(text)


with health:
    st.subheader("Health Tips")
    st.markdown("""
<h2 style="color: orange;">Health Tips</h2>
<ol style="color: yellow;">
    <li><b>Stay Hydrated:</b> Drink at least 8-10 glasses of water daily to stay hydrated.</li>
    <li><b>Balanced Diet:</b> Focus on a diet rich in fruits, vegetables, whole grains, and lean proteins.</li>
    <li><b>Limit Sugar and Processed Foods:</b> Reduce the intake of sugary drinks and highly processed foods.</li>
    <li><b>Adequate Sleep:</b> Aim for 7-9 hours of quality sleep each night to support recovery and mental clarity.</li>
    <li><b>Manage Stress:</b> Practice relaxation techniques like meditation, deep breathing, or mindfulness.</li>
    <li><b>Regular Health Check-ups:</b> Visit your doctor for routine health check-ups and screenings.</li>
    <li><b>Moderate Alcohol and Avoid Smoking:</b> Limit alcohol consumption and avoid smoking.</li>
    <li><b>Daily Movement:</b> Incorporate at least 30 minutes of physical activity into your daily routine.</li>
    <li><b>Mental Health:</b> Take time to disconnect from technology and connect with loved ones.</li>
</ol>

<!-- Exercises Section -->
<h2 style="color: saffron;">Exercises</h2>
<ul style="color: lightgreen;">
    <li><b>Cardio (Aerobic) Exercises:</b>
        <ul>
            <li><b>Running/Walking:</b> 20-30 minutes of jogging or brisk walking daily for cardiovascular health.</li>
            <li><b>Cycling:</b> Strengthens leg muscles and improves endurance.</li>
            <li><b>Swimming:</b> A full-body workout that's easy on the joints and great for cardiovascular fitness.</li>
        </ul>
    </li>
    <li><b>Strength Training:</b>
        <ul>
            <li><b>Squats:</b> Helps build lower body strength (legs, glutes, core).</li>
            <li><b>Push-ups:</b> Strengthens upper body muscles (arms, chest, shoulders).</li>
            <li><b>Planks:</b> Builds core stability and strength.</li>
            <li><b>Lunges:</b> Enhances balance and strengthens legs and core.</li>
        </ul>
    </li>
    <li><b>Flexibility and Mobility:</b>
        <ul>
            <li><b>Stretching:</b> Include dynamic stretches before a workout and static stretches afterward.</li>
            <li><b>Hip Circles and Arm Circles:</b> Help improve mobility in joints.</li>
        </ul>
    </li>
    <li><b>Core Exercises:</b>
        <ul>
            <li><b>Crunches:</b> Strengthens abdominal muscles.</li>
            <li><b>Bicycle Crunches:</b> Engages the core muscles, including obliques.</li>
            <li><b>Mountain Climbers:</b> A dynamic core and cardio exercise.</li>
        </ul>
    </li>
</ul>

<!-- Yoga Section -->
<h2 style="color: bluishgreen;">Yoga Practices</h2>
<ul style="color: lightgreen;">
    <li><b>Sun Salutation (Surya Namaskar):</b> A complete sequence that stretches and strengthens the body.</li>
    <li><b>Tree Pose (Vrikshasana):</b> A balancing pose that improves focus, strengthens the legs, and enhances posture.</li>
    <li><b>Downward Dog (Adho Mukha Svanasana):</b> A foundational pose that stretches the body, especially the hamstrings, calves, and shoulders.</li>
    <li><b>Child’s Pose (Balasana):</b> A gentle resting pose that stretches the lower back and relaxes the mind.</li>
    <li><b>Warrior Pose (Virabhadrasana):</b> Strengthens the legs, opens the chest and hips, and improves balance.</li>
    <li><b>Bridge Pose (Setu Bandhasana):</b> A backbend that opens the chest and strengthens the back, glutes, and legs.</li>
    <li><b>Corpse Pose (Savasana):</b> A resting pose done at the end of a yoga practice to help the body relax fully.</li>
</ul>
""", unsafe_allow_html=True)
    
    
with about:
    left, right = st.columns([1,2])
    with left:
        st.markdown("""
        <h5>Name</h5><br>
        <h5>Email</h5><br>
        <h5>Description</h5><br>
        <h5>Other links</h5><br>            
""", unsafe_allow_html=True)
    with right:
        st.markdown("""
        <h6>Ritesh Pandit</h6><br>
        <h6>karanstdio1234@gmail.com</h6><br>
        <h6>AI software automates computer related tasks such as controlling operating System and browsing.
                    It also have capability to talk using voice and answers all questions smartly using ML model</h6><br>
        <h6>https://www.linkedin.com/in/ritesh-pandit-408557269/</h6><br>   
        <h6>https://github.com/</h6>         
""", unsafe_allow_html=True)
    st.divider()

    # Generate the markdown content with improved CSS styling
    about_text = f"""
    <div style="background-color: rgb(40 40 40); padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); font-family: Arial, sans-serif; color: white;">
        <h2 style="font-size: 24px; color: white; margin-bottom: 15px;">About This Virtual Assistant</h2>
        <p>This virtual assistant, built using Streamlit, is capable of performing various tasks to assist you with your daily activities and queries. Below are some of its capabilities:</p>

        <ul style="list-style-type: disc; padding-left: 20px;">
    """
    about_text += """
        </ul>
    </div>
    """

    # Display the styled markdown in the About tab
    st.markdown(about_text, unsafe_allow_html=True)

with contact:
    st.header("Contacts of top Doctors")
