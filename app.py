from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import google.generativeai as genai
import requests
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-1.5-flash')



app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for flashing messages

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    # Process search query here
    return f"Search results for: {query}"

@app.route('/auth/login', methods=['POST'])
def auth_login():
    username = request.form['username']
    password = request.form['password']
    # Authentication logic here
    return redirect(url_for('index'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/auth/signup', methods=['POST'])
def auth_signup():
    username = request.form['username']
    password = request.form['password']
    # Signup logic here
    return redirect(url_for('index'))

@app.route('/generate', methods=['POST'])
def generate_curriculum():
    course_topic = request.form['course_topic']
    try:
        curriculum = query_gemini(course_topic)
        return render_template('curriculum.html', course_topic=course_topic, curriculum=curriculum)
    except Exception as e:
        logging.error(f"Error generating curriculum: {e}")
        flash('An error occurred while generating the curriculum. Please try again.')
        return redirect(url_for('index'))

def query_gemini(course_topic):
    try:
        headers = {
            'Authorization': f'Bearer {gemini_api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': 'gemini-model',
            'prompt': f"Generate a detailed curriculum for a course on {course_topic}. Include topics and brief descriptions.",
            'max_tokens': 500
        }
        response = requests.post('https://api.gemini.com/v1/completions', headers=headers, json=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        response_json = response.json()
        
        # Debug: Print the entire response JSON
        print("API Response:", response_json)

        # Check if 'choices' key exists in the response
        if 'choices' in response_json:
            curriculum = response_json['choices'][0]['text'].strip()
            return curriculum
        else:
            raise ValueError("The 'choices' key is not in the response JSON")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to Gemini API failed: {e}")
        raise
    except ValueError as ve:
        logging.error(f"Unexpected response format: {ve}")
        raise

@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(app.static_folder, 'robots.txt')

if __name__ == '__main__':
    app.run(debug=True)
