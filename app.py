from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
app = Flask(__name__)

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
    curriculum = query_openai(course_topic)
    return render_template('curriculum.html', course_topic=course_topic, curriculum=curriculum)

def query_openai(course_topic):
    # Query OpenAI GPT-3 to generate a curriculum
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Generate a detailed curriculum for a course on {course_topic}. Include topics and brief descriptions.",
        max_tokens=500
    )
    curriculum = response.choices[0].text.strip()
    return curriculum

@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(app.static_folder, 'robots.txt')

if __name__ == '__main__':
    app.run(debug=True)
