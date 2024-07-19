from flask import Flask, request, jsonify, send_from_directory
from pymongo import MongoClient
import os
import re
import spacy
from fuzzywuzzy import process

app = Flask(__name__)
nlp = spacy.load("en_core_web_md")
# Connect to the MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client.recruitment_db

# Load job description
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

# Function to parse the job description and create FAQ keywords
def parse_job_description(jd):
    faq_keywords = {}
    lines = jd.strip().split('\n')
    current_keyword = None
    response = ""

    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        
        # Check if the line is a keyword (bold text)
        if line.startswith("**") and ":" in line:
            # If we have a current keyword, save it before moving to the next
            if current_keyword:
                faq_keywords[current_keyword.lower()] = response.strip()  # Store keyword in lowercase
            
            # Set the new keyword and extract the response
            parts = line.split(":", 1)  # Split on the first colon
            current_keyword = parts[0][2:-2].strip()  # Remove the bold markers
            response = parts[1].strip()  # Start response with the text after the colon
        else:
            # Append the line to the current response
            response += " " + line.strip()  # Add a space before appending

    # Don't forget to add the last keyword and response
    if current_keyword:
        faq_keywords[current_keyword.lower()] = response.strip()  # Store last keyword in lowercase

    return faq_keywords

# Initialize faq_keywords at the start of the file
faq_keywords = parse_job_description(job_description)

# Function to find the best matching keyword based on semantic similarity
def find_best_matching_keyword(user_input, faq_keywords):
    user_doc = nlp(user_input.lower().strip())  # Normalize user input
    best_match = None
    highest_similarity = 0.0

    # Iterate through the keywords and calculate similarity
    for keyword in faq_keywords.keys():
        keyword_doc = nlp(keyword)  # Create a SpaCy document for the keyword
        similarity = user_doc.similarity(keyword_doc)  # Calculate similarity
        print(f"Comparing '{user_input}' with '{keyword}': Similarity = {similarity}")  # Debugging statement
        
        # Check if the similarity is the highest found so far
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = keyword

    # Return the best match if the similarity is above a threshold
    if highest_similarity >= 0.5:  # Adjust threshold as needed
        return best_match

    return None

def answer_question(user_input):
    user_input_lower = user_input.lower().strip()  # Normalize user input
    print(f"User Input: {user_input_lower}")  # Debugging statement

    # Find the best matching keyword based on semantic similarity
    best_match = find_best_matching_keyword(user_input_lower, faq_keywords)

    if best_match:
        return faq_keywords[best_match]  # Return the full response associated with the best match
    
    return "I'm sorry, I don't have an answer for that. You can ask about the job title, company overview, or key responsibilities."

@app.route('/')
def home():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    candidate_id = request.json.get('candidate_id')
    
    # Check eligibility
    if "eligible" in user_input.lower():
        response = check_eligibility(candidate_id)
    else:
        response = answer_question(user_input)
    
    # Log conversation
    log_conversation(candidate_id, user_input, response)
    
    # Add the analyze_response function definition
    def analyze_response(candidate_id, response):
        # Implement analysis logic here
        pass  # Placeholder for actual implementation
    
    # Analyze response
    analyze_response(candidate_id, response)
    
    return jsonify({"response": response})

# Function to check eligibility of the candidate
def check_eligibility(candidate_id):
    # Implement eligibility logic here
    return "Candidate is eligible."  # Example response

# Add the log_conversation function definition
def log_conversation(candidate_id, user_input, response):
    # Implement logging logic here
    pass  # Placeholder for actual implementation

if __name__ == '__main__':
    app.run(debug=True)