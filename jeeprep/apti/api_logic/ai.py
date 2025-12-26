
from django.conf import settings
import json
from groq import Groq


client = Groq(api_key=settings.GROQ_API_KEY)

def generate_questions(topics, number, difficulty):
    selected_topics = [t for t, selected in topics.items() if selected]
    
    prompt = f"""
    Generate {number} multiple choice questions (MCQs) from the following topics:
    Topics: {', '.join(selected_topics)}
    Difficulty: {difficulty}

    Here the questions should be of standard asked in placement tests like TCS NQT, GATE,
    JEE MAINS, JEE Advanced, Infosys.

    Verify that these questions are not duplicates of GATE/JEE/TCS NQT archives.
    
    STRICT OUTPUT:
    - Output ONLY valid JSON.
    - Format:
    [
      {{
        "question": "string",
        "options": ["opt1", "opt2", "opt3", "opt4"],
        "answer": "string",
        "topic": "{selected_topics}",
        "difficulty": "{difficulty}"
      }}
    ]
    """
    
    completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
      {
        "role": "user",
        "content": prompt
      }
    ],
    temperature=1,
    max_completion_tokens=8192,
    top_p=1,
    stream=True,
    stop=None
    )


    try:  
      text =""
      for chunk in completion:
        text+= chunk.choices[0].delta.content or ""
      return json.loads(text)
        
    except Exception as e:
        
       print("Raw LLM Response:\n", text)

    # 1️⃣ Try regex first (cheap + fast)
    try:
        return extract_json_regex(text)
    except Exception: 
      try:
          return ai_extract_json(text, client)
      except Exception as ai_error:
          raise ValueError(
              f"Failed to parse JSON.\nOriginal error: {e}\nAI error: {ai_error}"
          )


import json
import re

def extract_json_regex(text: str):
    """
    Fast fallback using regex (no AI call).
    """
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError("No JSON object found")



def ai_extract_json(raw_text, client):
    
    prompt = f"""
      You are a JSON extractor.

      Rules:
      - Extract ONLY valid JSON
      - Do NOT add explanations
      - Do NOT change keys or values
      - If multiple JSON objects exist, return the most complete one
      - Output MUST be pure JSON

      Text:
      {raw_text}
      """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b", 
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    extracted = response.choices[0].message.content.strip()
    return json.loads(extracted)
