from flask import Flask, request, jsonify, send_from_directory
from pymongo import MongoClient
import os
import spacy
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
nlp = spacy.load("en_core_web_md")

# Connect to the MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client.recruitment_db

# Define HR questions and answers
hr_questions = {
    "What is your greatest strength?": "My greatest strength is my ability to learn quickly and adapt to new situations.",
    "Describe a challenge you faced and how you overcame it.": "I faced a challenge when I had to meet a tight deadline, but I organized my tasks and prioritized effectively."
}

# Define the job description
job_description = """
We are looking for a candidate who is adaptable and can handle challenges.
The ideal candidate will have experience in software development and a strong understanding of web technologies, including Python and Docker.
"""
job_description = job_description.lower()

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
    # Normalize both the job description and user response to lowercase
    job_words = set(job_description.lower().split())
    response_words = set(user_response.lower().split())
    
    # Find the intersection of job words and response words
    matching_words = job_words.intersection(response_words)
    
    # Return the count of matching words
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
        # Calculate similarity with the provided answer
        similarity = calculate_similarity(user_response, hr_questions[question])
        
        if similarity >= 0.5:  # Adjust threshold as needed
            total_score += len(user_response)  # Increment score by length of answer
        else:
            # Compare with job description
            score_increment = compare_with_job_description(user_response)
            total_score += score_increment  # Increment total score by the number of matching words
        
        return question  # Return the next question
    else:
        return f"Total Score: {total_score}. Thank you for your responses!"

@app.route('/')
def home():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = start_hr_conversation(user_input)  # Start the HR conversation
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)