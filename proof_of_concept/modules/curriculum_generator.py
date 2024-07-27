import google.generativeai as genai
import json

def configure_api(api_key):
    genai.configure(api_key=api_key)

def generate_topics(input_prompt):
    model = genai.GenerativeModel('gemini-1.5-flash',generation_config={"response_mime_type": "application/json"})
    prompt = f"""
    Generate curriculum topics for {input_prompt}
    Using this JSON schema:
        Topics = "topic_name": str
    Return a `list[str]`
    eg: ["topic1_name", "topic2_name"]
    """
    # model.generate_content(prompt).text is string with list format ["topic1_name", "topic2_name"], json load to convert to list
    topics = json.loads(model.generate_content(prompt).text)
    print(f"topics: {topics}")
    return topics

    
    
