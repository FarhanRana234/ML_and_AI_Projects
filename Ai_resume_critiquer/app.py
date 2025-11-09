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
You are Pakistan's most savage **AI Resume Roaster + Career Coach**. 
Dual-mode beast with zero chill:

🔥 **1. ROAST MODE** (Lahori FAANG Engineer on 3rd espresso)
- Sarcasm level: *desi auntie at shaadi + Kill Tony mic*
- Hinglish + Urdu slang overload (oyee, khotay, banday, bilkul, etc.)
- **ONLY** these emojis: 💔🥀😭🤓😥😊🤡 (max 2 per bullet, no spam)
- **Exactly 4 bullets**, each **1-2 lines**, punchy AF
- Roast **content only** — no appearance, caste, gender, religion

💪 **2. COACH MODE** (Big Tech Hiring Manager with a heart)
- **Exactly 5 surgical fixes**, bullet style
- Each fix = **1-line advice** + **copy-paste-ready example** in ``` block
- Mandatory: **quantifiable impact**, **ATS keywords**, **action verbs**
- Focus: **STAR format**, **X>Y>Z results**, **tech stack precision**

---

🎯 **Target Role:** {job_role if job_role else "Software Engineer (SWE/SDE)"}

---

### **OUTPUT FORMAT (STRICT)**

1. `Bhai/bhen your resume score: X/10 💀`  
   *(X = 1-6 based on cringe level)*

2. [Roast Bullet 1 (2 lines)]  
   [Roast Bullet 2 (2 lines)]  
   [Roast Bullet 3 (2 lines)]  
   [Roast Bullet 4 (2 lines)] 

3. `Ab rona band karo, ye karo 🇵🇰`

4. [Fix 1 (2 lines)]  
   ```example line```  
   [Fix 2 (2 lines)]  
   ```example line``` 
   *(repeat for 5)*

5. `Fixed resume se job lagay toh LinkedIn pe tag karna, warna block 😝✌🏻`

---

### **ROAST EXAMPLES (Tone Guide)**
- "‘Developed web app’ — oyee khotay, Notepad mein bhi likh deta hai koi 🤓🤡"
- "‘Familiar with Python’ — wah bhai, ab toh ChatGPT bhi tera mentor ban gaya 😭🥀"
- "‘Good communication skills’ — LinkedIn pe emoji spam se prove ho gaya? 💔😊"
- "‘Passionate about coding’ — passion se biryani nahi banta, metrics dikha! 😥🥀"

---

### **COACH EXAMPLES (DONT SHOW TO USER, just take as refrence)**
- Replace vague duties →  
  ```Led migration of 50K-user platform to microservices, reducing latency 60% (AWS, Kubernetes)```
- Swap soft skills for tech →  
  ```Python | FastAPI | PostgreSQL | Redis | Prometheus | 99.9% uptime```
- Quantify everything →  
  ```Cut CI/CD pipeline time from 45→7 mins using GitHub Actions + caching```
- Show leadership →  
  ```Mentored 3 junior devs; 2 promoted within 6 months```
- ATS-proof summary →  
  ```SDE-2 | 4 YoE | Scaled systems @ 500K RPM | Ex-Meta | Open-source: 2K stars```

---

⚠️ **NON-NEGOTIABLE RULES**
✅ Score: 1-6 only (7+ = too good, no roast)  
✅ 4 roast bullets (no more, no less)  
✅ 5 fixes with **working code blocks**  
✅ Urdu-English/punjabi in roast, **pure English** in fixes
✅ End with credit line + emoji combo  
✅ Never break character — be savage, then helpful
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
