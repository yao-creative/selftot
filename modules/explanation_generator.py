import google.generativeai as genai

def generate_explanations(topics):
    model = genai.GenerativeModel('gemini-1.5-flash', generation_config=genai.GenerationConfig(
        max_output_tokens=50,
        temperature=0.9,
    ))


    explanations = []
    for topic in topics:
        topic_prompt = f"Provide a brief summary of: {topic}"
        explanation = model.generate_content(topic_prompt).text
        print(f"explanation: {explanation}")
        explanations.append({
            "topic": topic,
            "explanation": explanation
        })
    return explanations
