import json
import os
from difflib import SequenceMatcher
def sim_question(user_q, data):
    best_match = None
    highest_score = 0
    for q in data.keys():
        score = SequenceMatcher(None, user_q, q).ratio()
        if score > highest_score:
            highest_score = score
            best_match = q
    return best_match, highest_score
question_data_path= "C:/Users/User/VoidAI/VoidAI_Datas/question_data.json"
if not os.path.exists(question_data_path):
    with open(question_data_path, 'w', encoding='utf-8') as file:
        json.dump({}, file)
with open(question_data_path, 'r', encoding='utf-8') as file:
    try:
        existing_questions = json.load(file)
    except json.JSONDecodeError:
        existing_questions = {}
while True:
    question = input("Enter your question: ").strip().lower()
    if question in ["exit", "quit", "bye"]:
        print("VoidAI: Goodbye, user!")
        break
    similar_question, similarity_score = sim_question(question, existing_questions)
    if similarity_score >= 0.7:
        print(existing_questions[similar_question])
    elif question not in existing_questions:
        existing_questions[question] = question
        print(f"New question added to the database.")
        answer = input("Enter the answer for this question: ").strip()
        existing_questions[question] = answer
        print("Thanks a lot, user. Answer added.")
    else:
        print("This question already exists in the database.")
    with open(question_data_path, 'w', encoding='utf-8') as file:
        json.dump(existing_questions, file)

