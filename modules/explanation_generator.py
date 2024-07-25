import google.generativeai as genai

def generate_explanations(topics):
    max_output_tokens = 50
    model = genai.GenerativeModel('gemini-1.5-flash', generation_config=genai.GenerationConfig(
        max_output_tokens=max_output_tokens,
        temperature=0.9,
    ))


    explanations = []
    for topic in topics:
        topic_prompt = f"Provide a brief summary in {max_output_tokens} tokens of: {topic}"
        explanation = model.generate_content(topic_prompt).text
        print(f"explanation: {explanation}")
        explanations.append({
            "topic": topic,
            "explanation": explanation
        })
    return explanations
