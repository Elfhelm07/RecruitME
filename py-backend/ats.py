from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import spacy
from fuzzywuzzy import process
import os

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Connect to the MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client.recruitment_db

# Job description
JOB_DESCRIPTION_PDF = r'C:\Users\manas\Desktop\web\py-backend\Job Description.pdf'  # Update with the actual path

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)  # Ensure this line uses PdfReader
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def calculate_similarity(text1, text2):
    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    return cosine_similarity(vectors)[0, 1]

def extract_meaningful_words(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    words = [word for word in words if word.isalnum()]  # Remove punctuation
    words = [word for word in words if word.lower() not in stop_words]  # Remove stopwords
    tagged_words = pos_tag(words)
    meaningful_words = [word for word, pos in tagged_words if pos in ['NN', 'VB', 'JJ']]  # Keep nouns, verbs, adjectives
    return meaningful_words

def count_meaningful_words(text1, text2):
    words1 = extract_meaningful_words(text1)
    words2 = extract_meaningful_words(text2)
    
    counter1 = Counter(words1)
    counter2 = Counter(words2)
    
    common_words = set(counter1.keys()) & set(counter2.keys())
    total_common_count = sum(min(counter1[word], counter2[word]) for word in common_words)
    
    return total_common_count, common_words

@app.route('/upload', methods=['POST'])
def upload_file():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    resume_file = request.files['resume']
    
    job_description_text = extract_text_from_pdf(JOB_DESCRIPTION_PDF)
    resume_text = extract_text_from_pdf(resume_file)
    
    similarity_score = calculate_similarity(job_description_text, resume_text)
    common_word_count, common_words = count_meaningful_words(job_description_text, resume_text)
    
    adjusted_score = similarity_score * 100 + common_word_count * 10
    
    db.candidates.insert_one({
        'name': name,
        'phone': phone,
        'email': email,
        'ats_score': adjusted_score,
        'total_score': adjusted_score
    })
    
    return jsonify({'score': adjusted_score, 'common_words': list(common_words)})

# Chatbot functionality
nlp = spacy.load("en_core_web_md")

job_description = """
**Job Title**: 
Software Engineer

**Company Overview**: 
XYZ Corp is a leading tech company focused on innovation and excellence. We strive to create cutting-edge solutions that empower businesses and enhance user experiences.


**Job Summary**:
 We are seeking a Software Engineer to develop and maintain our web applications. The ideal candidate will have a passion for technology and a desire to work in a collaborative environment.

  

**Key Responsibilities**:

- Design, develop, and implement software solutions that meet business needs.

- Collaborate with cross-functional teams to define and design new features.

- Troubleshoot and debug applications to ensure optimal performance.

- Participate in code reviews and contribute to team knowledge sharing.

  

**Required Qualifications**:

- Bachelor's degree in Computer Science or a related field.

- 3+ years of experience in software development.

- Proficiency in JavaScript, Python, and SQL.

- Strong understanding of web development technologies and frameworks.

  

**Preferred Qualifications**:

- Experience with cloud technologies (AWS, Azure).

- Familiarity with Agile methodologies and version control systems (Git).

- Knowledge of front-end frameworks like React or Angular.

  

**Tech Stack**:

- Frontend: HTML, CSS, JavaScript, React

- Backend: Python, Flask, Node.js

- Database: MongoDB, PostgreSQL

- Tools: Git, Docker, Jenkins

  

**Work Environment**: 
This position is remote-friendly with occasional in-office meetings to foster team collaboration.

  

**Salary and Benefits**: 
Competitive salary, comprehensive health insurance, retirement plan, and flexible working hours.

  

**Application Process**: 
To apply, please submit your resume and cover letter to careers@xyzcorp.com.
"""

def parse_job_description(jd):
    faq_keywords = {}
    lines = jd.strip().split('\n')
    current_keyword = None
    response = ""

    for line in lines:
        line = line.strip()
        if line.startswith("**") and ":" in line:
            if current_keyword:
                faq_keywords[current_keyword.lower()] = response.strip()
            parts = line.split(":", 1)
            current_keyword = parts[0][2:-2].strip()
            response = parts[1].strip()
        else:
            response += " " + line.strip()

    if current_keyword:
        faq_keywords[current_keyword.lower()] = response.strip()

    return faq_keywords

faq_keywords = parse_job_description(job_description)

def find_best_matching_keyword(user_input, faq_keywords):
    user_doc = nlp(user_input.lower().strip())
    best_match = None
    highest_similarity = 0.0

    for keyword in faq_keywords.keys():
        keyword_doc = nlp(keyword)
        similarity = user_doc.similarity(keyword_doc)
        print(f"Comparing '{user_input}' with '{keyword}': Similarity = {similarity}")
        if (similarity > highest_similarity):
            highest_similarity = similarity
            best_match = keyword

    if highest_similarity >= 0.5:
        return best_match

    return None

def answer_question(user_input):
    user_input_lower = user_input.lower().strip()
    print(f"User Input: {user_input_lower}")

    best_match = find_best_matching_keyword(user_input_lower, faq_keywords)

    if best_match:
        return faq_keywords[best_match]
    
    return "I'm sorry, I don't have an answer for that. You can ask about the job title, company overview, or key responsibilities."


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    candidate_id = request.json.get('candidate_id')
    
    if "eligible" in user_input.lower():
        response = check_eligibility(candidate_id)
    else:
        response = answer_question(user_input)
    
    log_conversation(candidate_id, user_input, response)
    
    return jsonify({"response": response})  # Ensure jsonify is used correctly



def check_eligibility(candidate_id):
    return "Candidate is eligible."

def log_conversation(candidate_id, user_input, response):
    pass

if __name__ == '__main__':
    app.run(debug=True)
