from pydoc_data import topics



from pymongo import MongoClient
from datetime import datetime
from django.conf import settings
from rest_framework.response import Response
import json
import os

client = MongoClient(settings.MONGODB_URL)
db = client["jeeprep"]

coding_collection = db["coding_problems"]
assessment_collection = db["assessment_questions"]
score_collection= db["score_collection"]


def save_to_mongodb(user_id, assessment_id, data, purpose):
    """
    data:
      - For Coding: list of coding problems (JSON-compatible)
      - For Assessment: list of question structs
    """

    data = json.loads(data)

    if purpose == "coding":
        data = data.get("output", [])
        documents = []

        for key in data:
            doc = {
                "user_id": user_id,
                "assessment_id":assessment_id,
                "title": key.get("title"),
                "difficulty": key.get("difficulty"),
                "company": key.get("company", []),
                "description": key.get("description"),
                "topics": key.get("topics", []),
                "testcases": key.get("testcases", []),
                "boiler_plate_code": key.get("boiler_plate_code"),
                "created_at": datetime.utcnow()
            }
            documents.append(doc)

        if documents:
            coding_collection.insert_many(documents)

    else:
        questions = data.get("questions", [])
        documents = []

        for key in questions:
            doc = {
                "user_id": user_id,
                "assessment_id": assessment_id,
                "question": key.get("question"),
                "options": key.get("options"),
                "difficulty": key.get("difficulty"),
                "topic": key.get("topic") if key.get("topic") else None,
                "answer": key.get("answer"),
                "purpose": purpose,
                "created_at": datetime.utcnow()
            }
            documents.append(doc)

        if documents:
            assessment_collection.insert_many(documents)

    print("Inserted successfully")
    return True


def fetch_from_mongodb(user_id):
    json_data = {}

    # ---------- CODING ----------
    coding_cursor = coding_collection.aggregate([
    {"$match": {"user_id": user_id}},
    {"$group": {"_id": "$assessment_id"}},
    {"$sort": {"_id": 1}}
    ])


    json_data["coding"] = [
            {"assessment_id": doc["_id"]}
            for doc in coding_cursor
        ]

    # ---------- ASSESSMENTS ----------
    for purpose in ["software_quiz", "aptitude", "verbals"]:
        cursor = assessment_collection.aggregate([
            {
                "$match": {
                    "user_id": user_id,
                    "purpose": purpose
                }
            },
            {
                "$group": {
                    "_id": "$assessment_id"
                }
            },
            {
                "$sort": {"_id": 1}
            }
        ])

        json_data[purpose] = [
            {"assessment_id": doc["_id"]}
            for doc in cursor
        ]


    return json_data


def save_score_to_mongodb(user_id,purpose,assessment_id:str,correct_questions,incorrect_questions\
                          ,unattempted_questions):
    doc = {
    "user_id": user_id,
    "assessment_id": assessment_id,
    "correct": correct_questions,        
    "incorrect": incorrect_questions,    
    "unattempted": unattempted_questions,
    "correct_count": len(correct_questions),
    "incorrect_count": len(incorrect_questions),
    "unattempted_count": len(unattempted_questions),
    "purpose":purpose
    }

    score_collection.insert_one(doc)

    print("Inserted successfully")


def fetch_score_from_mongodb(user_id):
    json_data ={}
    
    for purpose in ["software_quiz", "aptitude", "verbals"]:

        cursor = score_collection.aggregate([
            {
                "$match": {
                    "user_id": user_id,
                    "purpose": purpose
                }
            },
            {
                "$group": {
                    "_id": "$user_id",
                    "total_correct": { "$sum": "$correct_count" },
                    "total_incorrect": { "$sum": "$incorrect_count" },
                    "total_unattempted": { "$sum": "$unattempted_count" }
                }
            },
            {
                "$addFields": {
                    "accuracy": {
                        "$cond": [
                            { "$eq": [{ "$add": ["$total_correct", "$total_incorrect"] }, 0] },
                            0,
                            {
                                "$multiply": [
                                    {
                                        "$divide": [
                                            "$total_correct",
                                            { "$add": ["$total_correct", "$total_incorrect"] }
                                        ]
                                    },
                                    100
                                ]
                            }
                        ]
                    }
                }
            }
        ])

        
        json_data[purpose] = next(cursor, {}).get("accuracy", 0)
        print(json_data)
    return json_data




def fetch_purpose_pipeline_from_mongodb(user_id):
    json_data ={}
    cursor = score_collection.aggregate([
        {
            "$match": { "user_id": user_id }
        },
        {
            "$project": {
                "all_questions": {
                    "$concatArrays": [
                        {
                            "$map": {
                                "input": "$correct",
                                "as": "c",
                                "in": {
                                    "topic": "$$c.topic",
                                    "status": "correct"
                                }
                            }
                        },
                        {
                            "$map": {
                                "input": "$incorrect",
                                "as": "i",
                                "in": {
                                    "topic": "$$i.topic",
                                    "status": "incorrect"
                                }
                            }
                        }
                    ]
                }
            }
        },
        { "$unwind": "$all_questions" },
        {
            "$group": {
                "_id": "$all_questions.topic",
                "total_correct": {
                    "$sum": {
                        "$cond": [
                            { "$eq": ["$all_questions.status", "correct"] },
                            1,
                            0
                        ]
                    }
                },
                "total_incorrect": {
                    "$sum": {
                        "$cond": [
                            { "$eq": ["$all_questions.status", "incorrect"] },
                            1,
                            0
                        ]
                    }
                }
            }
        },
        {
            "$addFields": {
                "accuracy": {
                    "$cond": [
                        { "$eq": [{ "$add": ["$total_correct", "$total_incorrect"] }, 0] },
                        0,
                        {
                            "$multiply": [
                                {
                                    "$divide": [
                                        "$total_correct",
                                        { "$add": ["$total_correct", "$total_incorrect"] }
                                    ]
                                },
                                100
                            ]
                        }
                    ]
                }
            }
        }
    ])
    
        
    json_data = {}
    topics=["Reading_comprehension","Sentence_correction","grammar","vocabulary", 
            "error_spotting","os","dbms","networks","DS","algorithms","cyber","oops" ,
            "compiler","dsa","ai","ml","dl","dsml","architecture","cloud","devops",
            "software", "web","linux","sql","aptitude","systemdesign","arithemetic",
            "number_system","algebra","probability","data_interpretation"]
    
    for doc in cursor:
        if type(doc["_id"]) == list:
            for topic in doc["_id"]:
                json_data[topic] = doc["accuracy"]
        else:   
            json_data[doc["_id"]] = doc["accuracy"]
        

    # Ensure all topics exist (default 0)
    for topic in topics:
        if topic not in json_data:
            if type(topic)==list:
                for t in topic:
                    json_data[t] = 0
            else:
                json_data[topic] = 0

    print(json_data)
    return json_data





