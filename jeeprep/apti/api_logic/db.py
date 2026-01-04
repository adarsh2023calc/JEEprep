

import os
import datetime
import json


from google.cloud import bigquery
client = bigquery.Client()


from datetime import datetime

def save_to_bigquery(user_id, assessment_id, data, purpose):
    """
    data:
      - For Coding: list of coding problems (JSON-compatible)
      - For Assessment: list of question structs
    """

    
    data = json.loads(data)
    rows=[]
    if purpose == "coding":
        data = data.get("output")
        
        table_id = "locenergy.jeeprep.coding_problems"
        for key in data:
            row = {
                "user_id":user_id,
                "title": key.get("title"),
                "difficulty": key.get("difficulty"),
                "company": key.get("company", []),
                "description": key.get("description"),
                "topics": key.get("topics", []),
                "testcases": key.get("testcases", []),
                "boiler_plate_code": key.get("boiler_plate_code"),

            }
            rows.append(row)
        

    else:
        
        table_id = "locenergy.jeeprep.assessment_questions"
        rows=[]
        Questions=data.get("questions")
        for key in Questions:
            row = {
                "user_id": user_id,
                "assessment_id": assessment_id,
                "question": key.get("question"),
                "options": key.get('options'),
                "difficulty": key.get("difficulty"),     
                "topic": key.get('topic')[0],
                "created_at": datetime.utcnow().isoformat(),
                "answer": key.get("answer"),
                "purpose":purpose
            }
            rows.append(row)

    errors = client.insert_rows_json(
            table_id,
            rows   # must always be a list
    )

    if errors:
        print("Insert errors:", errors)
        return False

    print("Inserted successfully")
    return True
