import google.generativeai as genai
from django.conf import settings
import json

genai.configure(api_key=settings.GEMINI_API_KEY)


def fetch_questions(number, difficulty, company):
    """
    Fetch coding questions (title, difficulty, description, topics, company tag, testcases)
    with strict JSON output.
    """

    prompt = f"""
    Generate {number} coding interview questions.

    Requirements:
    - Difficulty must be: {difficulty}
    - Company tag: {company}
    - Each question must include EXACTLY two testcases.
    - Output ONLY valid JSON.

    JSON Format:
    [
      {{
        "title": "string",
        "difficulty": "easy/medium/hard",
        "company": ["{company}"],
        "description": "4–6 sentence clear problem statement.",
        "topics": ["arrays", "dp", "graphs", ...],
        "testcases": [
            {{
                "input": "Input in plain text as LeetCode style",
                "output": "Expected output"
            }},
            {{
                "input": "Second testcase",
                "output": "Expected output"
            }}
        ]
      }}
    ]

    EXTRA RULES:
    - Testcases must match the description and logic of the problem.
    - No markdown. No text outside JSON.
    - Ensure the JSON parses correctly.
    """

    model = genai.GenerativeModel("gemini-2.0-flash")

    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )

    try:
        raw = response.candidates[0].content.parts[0].text
        return json.loads(raw)

    except Exception as e:
        print("---- Gemini Raw Response ----")
        print(response)
        print("-----------------------------")
        raise ValueError(f"Failed to parse JSON from Gemini: {e}")
