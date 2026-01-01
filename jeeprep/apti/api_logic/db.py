

import os
import datetime

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"

from google.cloud import bigquery
client = bigquery.Client()


def save_to_bigquery(user_id,assesment_id,data):
    table_id="locenergy.jeeprep.user_assessments"





    row = {
    "user_id": user_id,
    "assessment_id": assesment_id,
    "questions":,
    "created_at": datetime.utcnow()
}

    errors = client.insert_rows_json(
        table_id,
        [row]  # must be a list
    )

    if errors:
        print("Insert errors:", errors)
    else:
        print("Inserted successfully")
        pass