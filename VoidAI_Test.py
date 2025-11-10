import json
import os
import torch
from sentence_transformers import SentenceTransformer, util
from transformers import AutoModelForCausalLM, AutoTokenizer
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B")
model_gen = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B").to(device)
def generate_answer(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model_gen.generate(**inputs, max_new_tokens=200)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
model = SentenceTransformer("all-mpnet-base-v2")
question_data_path= "C:/Users/User/VoidAI/VoidAI_Datas/question_data.json"
if not os.path.exists(question_data_path):
    with open(question_data_path, 'w', encoding='utf-8') as file:
        json.dump({}, file, indent=4)
with open(question_data_path, 'r', encoding='utf-8') as file:
    try:
        existing_questions = json.load(file)
    except json.JSONDecodeError:
        existing_questions = {}
while True:
    questions = list(existing_questions.keys())
    embeddings = model.encode(questions, convert_to_tensor=True) if questions else None
    question = input("Enter your question: ").lower().strip("?!.")
    if question in ["exit", "quit", "bye"]:
        print("Goodbye, user!")
        break
    if embeddings is not None and len(questions) > 0:
        user_embedding = model.encode(question, convert_to_tensor=True)
        cosine_scores = util.cos_sim(user_embedding, embeddings)
        best_score, idx = torch.max(cosine_scores, dim=1)
        best_score = best_score.item()
        if best_score >= 0.8:
            print(f"{existing_questions[questions[idx]]}")
            continue
        elif best_score >= 0.6:
            print(f"Did you mean: '{questions[idx]}'? (Score: {best_score:.2f})")
            confirmation = input("Type 'yes' to confirm, or 'no' to add a new question: ").strip("?!.").lower()
            if confirmation == 'yes':
                print(f"{existing_questions[questions[idx]]}")
                continue
    print("No strong match found. Generating new answer...")
    answer = generate_answer(question)
    print("Generated Answer:", answer)
    save = input("Save this answer to memory? (yes/no): ").lower()
    if save == "yes":
        existing_questions[question] = answer
        print("Thanks a lot, user. Answer added.")
    new_embedding = model.encode(question, convert_to_tensor=True)
    embeddings = torch.cat((embeddings, new_embedding.unsqueeze(0)), dim=0) if embeddings is not None else new_embedding.unsqueeze(0)
    with open(question_data_path, 'w', encoding='utf-8') as file:
        json.dump(existing_questions, file)
