from flask import Flask, request, render_template
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from pymongo import MongoClient  # Import MongoDB client

# Download necessary NLTK data files
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB URI
db = client['ats_database']  # Replace with your database name
candidates_collection = db['candidates']  # Replace with your collection name

# Fixed job description PDF link
JOB_DESCRIPTION_PDF = r'C:\Users\Lenovo\Downloads\Job Description.pdf'  # Update with the actual path

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

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        name = request.form['name']  # Get name from form
        phone = request.form['phone']  # Get phone from form
        email = request.form['email']  # Get email from form
        resume_file = request.files['resume']  # Only resume upload
        
        job_description_text = extract_text_from_pdf(JOB_DESCRIPTION_PDF)  # Use fixed job description
        resume_text = extract_text_from_pdf(resume_file)
        
        similarity_score = calculate_similarity(job_description_text, resume_text)
        common_word_count, common_words = count_meaningful_words(job_description_text, resume_text)
        
        # Adjust similarity score based on common meaningful words
        adjusted_score = similarity_score * 100 + common_word_count * 10
        
        # Insert candidate details into MongoDB with total_score equal to ats_score
        candidates_collection.insert_one({
            'name': name,
            'phone': phone,
            'email': email,
            'ats_score': adjusted_score,
            'total_score': adjusted_score  # Set total score equal to ats_score
        })
        
        return render_template('result.html', score=adjusted_score, common_words=common_words)
    
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)