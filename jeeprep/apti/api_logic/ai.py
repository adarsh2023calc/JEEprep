import google.generativeai as genai
from django.conf import settings
import json

genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_questions(topics, number, difficulty):
    selected_topics = [t for t, selected in topics.items() if selected]
    
    prompt = f"""
    Generate {number} multiple choice questions (MCQs) from the following topics:
    Topics: {', '.join(selected_topics)}
    Difficulty: {difficulty}

    Here the questions should be of standard asked in placement tests like TCS NQT
    
    STRICT OUTPUT:
    - Output ONLY valid JSON.
    - Format:
    [
      {{
        "question": "string",
        "options": ["opt1", "opt2", "opt3", "opt4"],
        "answer": "string",
        "topic": "one of {selected_topics}",
        "difficulty": "{difficulty}"
      }}
    ]
    """
    
    model = genai.GenerativeModel("gemini-2.0-flash")

    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )

   
    # ---- FIX: extract JSON response properly ----
    try:
        text = response.candidates[0].content.parts[0].text
        print(text)
        return json.loads(text)


    except Exception as e:
        # Helpful debug print
        print("Raw Gemini Response:", response)
        raise ValueError(f"Failed to parse Gemini response: {e}")
