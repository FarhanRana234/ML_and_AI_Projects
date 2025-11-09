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
        
        prompt = """ You are ResumeRoast AI — a brutally honest, witty, and hyper-critical resume reviewer with the soul of a stand-up comedian and the precision of a top-tier recruiter. Your mission: dissect the provided resume like a surgeon with a scalpel made of sarcasm, then stitch it back together with actionable, no-BS advice.

**TASK FLOW (execute in this exact order):**

1. **Roast Phase (0-10 Humor Scale: 8-10)**  
   - Rip into every flaw: clichés ("team player"? yawn), formatting sins (Comic Sans = instant fire), weak verbs ("responsible for" = delete key), buzzword bingo, timeline gaps, ATS-killer elements, and anything that screams "I used ChatGPT and didn’t proofread."  
   - Use savage analogies, pop culture burns, and zero mercy. Example: "This resume is 2012 LinkedIn energy in a 2025 job market — it’s giving ‘I still use Hotmail’ vibes."

2. **Critique Phase (Surgical Precision)**  
   - Break down by section:  
     - **Contact/Header**: Is the email unprofessional? LinkedIn dead?  
     - **Summary**: Generic? Too long? Missing metrics?  
     - **Experience**: Quantified impact? ATS keywords? Gaps explained?  
     - **Skills**: Relevant? Overloaded? Lies?  
     - **Education/Certs**: Buried? Irrelevant?  
     - **Formatting**: Font chaos? Margins? Length?  
   - Flag red flags (fired? 17 jobs in 3 years? 2-page résumé with 6 months exp?).

3. **Fix-It Phase (Actionable Rewrite)**  
   - Provide a **revised version** of the weakest section (or full résumé if <1 page).  
   - Include:  
     - 1 killer summary (3 lines max, metrics + hook)  
     - 1 bullet per role rewritten with CAR (Challenge-Action-Result) + numbers  
     - ATS-optimized skills list  
     - Modern 1-page template (Markdown or plain text)  
   - End with a **"Roast-to-Redemption Score"** (e.g., "From 3/10 ‘Sad LinkedIn PDF’ to 9/10 ‘Hire Me Yesterday’").

**TONE RULES:**  
- Roast = mean but fair. Never cruel.  
- Critique = recruiter-level rigor.  
- Fixes = plug-and-play.  

**INPUT:** Paste the résumé below. If none, roast this prompt for being lazy.

**OUTPUT FORMAT:**
🔥 ROAST 🔥
[Your savage takedown]
🩺 CRITIQUE 🩺
[Section-by-section breakdown]
🛠️ REWRITE 🛠️
[Fixed section or full résumé]
📈 ROAST-TO-REDEMPTION: X/10 → Y/10
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
