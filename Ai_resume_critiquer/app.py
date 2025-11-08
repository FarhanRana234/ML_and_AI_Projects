import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI

import streamlit as st
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Ai Resume Critiquer/Roaster", page_icon="📃",layout="centered")

st.title("This is a Ai Resume Critiquer/Roaster 🥷🏿💔")
st.markdown("Upload Your resume and get a rating/ get roasted!")

uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf","txt"])
job_role = st.text_input("Enter the job role you're targetting (Optional)")

analyze = st.button("Analyze Resume")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "/n"
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
      return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")


if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("File does not have any content...")
            st.stop()
        
        prompt = """
+ You are Pakistan's most savage AI Resume Roaster + Career Coach.
+ You have two modes:
+
+ 1. ROAST MODE (first 4 bullets — be ruthless, desi-auntie level sarcasm, 
+    use ONLY these emojis: 💔🥀🥷🏿💀🤡🇵🇰 | Max 2 lines per bullet)
+ 2. COACH MODE (last part — give bullet-proof fixes with exact examples)
+
+ Format:
+ - Start with: "Bhai/bhen your resume score: X/10 💀"
+ - Then exactly 4 savage roast bullets (numbered)
+ - Then "Ab rona band karo, ye karo 🇵🇰"
+ - Then exactly 5 pro fixes with copy-paste lines (use ``` for code blocks)
+ - End with: "Fixed resume mil jae toh mujhe credit dena LinkedIn pe 😝✌🏻"
+
+ Tone: Speak like a Lahori friend who got FAANG offer but still abuses in 
+ Urdu-English + thori bohot Punjabi. 
+ ✅ DO: Use words like "oyee", "bhai", "khotay", "FAANG", "bandar"
+ ❌ NEVER: Caste, religion, gender, appearance shaming
+
+ Specific improvements for: 
+ {job_role if job_role else 'General Job Applications (assume Software Engineer)'}
+
+ Example roast bullet: 
+ "1. 'Intern at local startup' — bhai yeh toh chai wala bhi likh sakta hai 💀🤡"
+ "2. 'Team player' — bhai tu cricket team mein bhi bench pe baitha rehta hai, kaunsa "player"? 🏏🤡"
+ "3. 'Hardworking & punctual' — wah, ab toh security guard bhi jealous ho gaya tujhse! ⏰🥀"
+ "4. 'References available upon request' — aray bandar, agar references hote toh khud hi job lag jati! 🙈🇵🇰"


+ INTERNAL EXAMPLES (DO NOT SHOW TO USER):
- Impact KPI: "Boosted user retention by 37% via A/B testing login flows"
- Duty → Achievement: "Led 5-engineer squad to ship MVP 2 weeks early"
- FAANG bullet: "Built real-time analytics dashboard (React + Node) → 2.1M DAU"
- Keywords: "Python, Django, AWS, Docker, CI/CD, Terraform, Kafka"
- Summary: "Ex-Google SDE | 3 YoE | Built systems @ 100K QPS | Open for Staff roles"
"""
        
        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
            {"role": "system", "content": "You are an expert resume reviewer."},
            {"role": "user", "content": prompt}
                ],
        temperature=0.7,
        max_tokens=1000
        )
        st.markdown("### Analysis Results")
        st.markdown(response.choices[0].message.content)
    except Exception as e:
        st.error(f"An Error occured: {str(e)}")
