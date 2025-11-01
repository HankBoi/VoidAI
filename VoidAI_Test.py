import json
import os
import torch
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer("all-MiniLM-L6-v2")
question_data_path= "C:/Users/User/VoidAI/VoidAI_Datas/question_data.json"
if not os.path.exists(question_data_path):
    with open(question_data_path, 'w', encoding='utf-8') as file:
        json.dump({}, file, indent=4)
with open(question_data_path, 'r', encoding='utf-8') as file:
    try:
        existing_questions = json.load(file)
    except json.JSONDecodeError:
        existing_questions = {}
questions = list(existing_questions.keys())
embeddings = model.encode(questions, convert_to_tensor=True) if questions else None
while True:
    question = input("Enter your question: ").strip().lower()
    if question in ["exit", "quit", "bye"]:
        print("Goodbye, user!")
        break
    if embeddings is not None and len(questions) > 0:
        user_embedding = model.encode(question, convert_to_tensor=True)
        cosine_scores = util.cos_sim(user_embedding, embeddings)
        best_score, idx = torch.max(cosine_scores, dim=1)
        best_score = best_score.item()
        if best_score >= 0.7:
            print(f"{existing_questions[questions[idx]]}")
            continue
    existing_questions[question] = question
    print(f"New question added to the database.")
    answer = input("Enter the answer for this question: ").strip()
    existing_questions[question] = answer
    new_embedding = model.encode(question, convert_to_tensor=True)
    embeddings = torch.cat((embeddings, new_embedding.unsqueeze(0)), dim=0) if embeddings is not None else new_embedding.unsqueeze(0)
    print("Thanks a lot, user. Answer added.")
    with open(question_data_path, 'w', encoding='utf-8') as file:
        json.dump(existing_questions, file)
