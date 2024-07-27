from flask import Flask, render_template, request, jsonify
from modules.curriculum_generator import configure_api, generate_topics
from modules.explanation_generator import generate_explanations
from utils.config import API_KEY

app = Flask(__name__)

# Configure the Generative AI API
configure_api(API_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Debugging: Check if the form is being submitted
    print("Form submitted to /generate")

    # Debugging: Check if the form data is being received
    print(f"Form data received: {request.form}")

    input_prompt = request.form.get('prompt')
    print(f"Received prompt: {input_prompt}")  # Debugging line
    if not input_prompt:
        return "No prompt provided", 400

    topics = generate_topics(input_prompt)
    explanations = generate_explanations(topics)
    # Zip topics and explanations before passing to the template

    return render_template('curriculum.html', explanations= explanations, course_topic=input_prompt)

# make sure in login.html /login_user action prints the form data to the console
@app.route('/login_user', methods=['POST'])
def login_user():
    print(f"Form data received: {request.form}")
    return jsonify(request.form)
if __name__ == '__main__':
    app.run(debug=True)
