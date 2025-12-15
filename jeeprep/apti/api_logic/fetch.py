

from django.conf import settings
import json
from groq import Groq



client = Groq(api_key=settings.GROQ_API_KEY)


def fetch_questions(number, difficulty, company):
    """
    Fetch coding questions (title, difficulty, description, topics, company tag, testcases)
    with strict JSON output. ONLY JSON
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
        ,
        boiler_plate_code: "code"
      }}
    ]

    IMPORTANT:
    If the response contains ANY text outside the JSON object,
    the response will be considered INVALID and rejected.

        DO NOT explain.
        DO NOT justify.
        DO NOT add notes.
        DO NOT add headings.
        DO NOT add markdown.
         - Should output boiler_plate_code with 
      format: 
      import sys
      import json
      class Solution:
        def twoSum(self, nums, target):

      if __name__ == "__main__":
        raw = [json.loads(arg) for arg in sys.argv[1:]]
        sol = Solution()

        for tc in raw:
            output = sol.twoSum(tc["nums"], tc["target"])
            print(output)

        Return ONLY a single valid JSON object.
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
        print("Raw Groq Response:", text)
        raise ValueError(f"Failed to parse Groq response: {e}")