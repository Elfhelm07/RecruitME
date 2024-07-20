from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS  # Import CORS
from pymongo import MongoClient
import os
import re
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Download necessary NLTK data files
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

app = Flask(__name__)
CORS(app)  # Enable CORS
nlp = spacy.load("en_core_web_md")

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['recruitment_db']
candidates_collection = db['candidates']
JOB_DESCRIPTION_PDF = r"C:\Users\manas\Desktop\web\py-backend\Job Description.pdf"
# Job description and HR questions
job_description = """
We are looking for a candidate who is adaptable and can handle challenges.
The ideal candidate will have experience in software development and a strong understanding of web technologies, including Python and Docker.
""".lower()

hr_questions = {
    "What is your greatest strength?": "My greatest strength is my ability to learn quickly and adapt to new situations.",
    "Describe a challenge you faced and how you overcame it.": "I faced a challenge when I had to meet a tight deadline, but I organized my tasks and prioritized effectively."
}

# Initialize score and question index
total_score = 0
current_question_index = 0

# Function to calculate similarity between two texts
def calculate_similarity(user_response, correct_answer):
    user_vector = nlp(user_response).vector.reshape(1, -1)
    answer_vector = nlp(correct_answer).vector.reshape(1, -1)
    return cosine_similarity(user_vector, answer_vector)[0][0]

# Function to compare user response with job description
def compare_with_job_description(user_response):
    job_words = set(job_description.split())
    response_words = set(user_response.lower().split())
    matching_words = job_words.intersection(response_words)
    return len(matching_words)

# Function to get the next HR question
def get_next_question():
    global current_question_index
    if current_question_index < len(hr_questions):
        question = list(hr_questions.keys())[current_question_index]
        current_question_index += 1
        return question
    return None

# Function to start HR conversation
def start_hr_conversation(user_response):
    global total_score
    question = get_next_question()
    if question:
        similarity = calculate_similarity(user_response, hr_questions[question])
        if similarity >= 0.5:
            total_score += len(user_response)
        else:
            total_score += compare_with_job_description(user_response)
        return question
    else:
        return f"Thank you for your responses!"

# Function to check eligibility of the candidate
def check_eligibility(candidate_id):
    return "Candidate is eligible."

# Function to log conversation
def log_conversation(candidate_id, user_input, response):
    pass

# Function to parse the job description and create FAQ keywords
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

# Function to find the best matching keyword based on semantic similarity
def find_best_matching_keyword(user_input, faq_keywords):
    user_doc = nlp(user_input.lower().strip())
    best_match = None
    highest_similarity = 0.0
    for keyword in faq_keywords.keys():
        keyword_doc = nlp(keyword)
        similarity = user_doc.similarity(keyword_doc)
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = keyword
    if highest_similarity >= 0.5:
        return best_match
    return None

# Function to answer questions based on parsed job description
def answer_question(user_input):
    user_input_lower = user_input.lower().strip()
    best_match = find_best_matching_keyword(user_input_lower, faq_keywords)
    if best_match:
        return faq_keywords[best_match]
    return "I'm sorry, I don't have an answer for that. You can ask about the job title, company overview, or key responsibilities."

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Function to extract meaningful words from text
def extract_meaningful_words(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    words = [word for word in words if word.isalnum()]
    words = [word for word in words if word.lower() not in stop_words]
    tagged_words = pos_tag(words)
    meaningful_words = [word for word, pos in tagged_words if pos in ['NN', 'VB', 'JJ']]
    return meaningful_words

# Function to count meaningful words
def count_meaningful_words(text1, text2):
    words1 = extract_meaningful_words(text1)
    words2 = extract_meaningful_words(text2)
    counter1 = Counter(words1)
    counter2 = Counter(words2)
    common_words = set(counter1.keys()) & set(counter2.keys())
    total_common_count = sum(min(counter1[word], counter2[word]) for word in common_words)
    return total_common_count, common_words

@app.route('/')
def home():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')

@app.route('/chat_hr', methods=['POST'])
def chat_hr():
    user_input = request.json.get('message')
    response = start_hr_conversation(user_input)
    return jsonify({"response": response})

@app.route('/chat_faq', methods=['POST'])
def chat_faq():
    user_input = request.json.get('message')
    candidate_id = request.json.get('candidate_id')
    if "eligible" in user_input.lower():
        response = check_eligibility(candidate_id)
    else:
        response = answer_question(user_input)
    log_conversation(candidate_id, user_input, response)
    return jsonify({"response": response})

@app.route('/upload_resume', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
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
        return jsonify({"score": float(adjusted_score)})
    return render_template('upload.html')

@app.route('/end_hr_chat', methods=['GET'])
def end_hr_chat():
    global total_score
    return jsonify({"total_score": total_score})

if __name__ == '__main__':
    app.run(debug=True)
