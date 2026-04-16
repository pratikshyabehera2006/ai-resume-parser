import spacy
import re
from PyPDF2 import PdfReader

nlp = spacy.load("en_core_web_sm")


#  Extract full text from PDF
def extract_text(file):
    text = ""
    pdf = PdfReader(file)
    for page in pdf.pages:
        if page.extract_text():
            text += page.extract_text()
    return text


#  Extract Email (robust)
def extract_email(text):
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return emails[0] if emails else "Not Found"


#  Extract Phone 
def extract_phone(text):
    import re

    phone = re.findall(r'(\+?\d[\d\s\-]{8,15}\d)', text)

    if phone:
        number = phone[0].replace(" ", "").replace("-", "")

        # Mask last 4 digits
        if len(number) >= 4:
            masked = number[:-4] + "****"
            return masked

        return number

    return "Not Found"


#  Extract Name 
def extract_name(text):
    import re

    # Find email first
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)

    if email_match:
        start_index = email_match.start()

        # Take text before email
        before_email = text[:start_index]

        # Split into words
        words = before_email.strip().split()

        # Take last 2 valid words as name
        name = []
        for word in reversed(words):
            if word.isalpha():
                name.append(word)
            if len(name) == 2:
                break

        if len(name) == 2:
            return " ".join(reversed(name))

    return "Not Found"


#  Extract Skills (better matching)
def extract_skills(text):
    skills_db = [
        "python", "java", "c++", "c", "machine learning", "deep learning",
        "artificial intelligence", "ai", "sql", "mysql", "html", "css",
        "javascript", "flask", "tensorflow", "pandas", "numpy"
    ]

    text_lower = text.lower()
    found_skills = []

    for skill in skills_db:
        if skill in text_lower:
            found_skills.append(skill)

    return list(set(found_skills))


#  Extract Education (basic)
def extract_education(text):
    lines = text.split("\n")

    college_keywords = [
        "university", "college", "institute", "school"
    ]

    education = []

    for line in lines:
        line_clean = line.strip()

        if any(keyword in line_clean.lower() for keyword in college_keywords):
            education.append(line_clean)

    # Remove duplicates
    return list(set(education))


#  Extract Sections (optional advanced)
def extract_sections(text):
    sections = {}
    current_section = "General"
    sections[current_section] = []

    for line in text.split("\n"):
        line = line.strip()

        if line.isupper() and len(line.split()) < 5:
            current_section = line
            sections[current_section] = []
        else:
            sections[current_section].append(line)

    return sections


#  Main function
def parse_resume(file):
    text = extract_text(file)

    return {
        "text": text,
        "Name": extract_name(text),
        "Email": extract_email(text),
        "Phone": extract_phone(text),
        "Skills": extract_skills(text),
        "Education": extract_education(text)
    }

def match_score(resume_text, job_desc):
    resume_words = set(resume_text.lower().split())
    job_words = set(job_desc.lower().split())

    if len(job_words) == 0:
        return 0

    score = len(resume_words & job_words) / len(job_words)
    return round(score * 100, 2)