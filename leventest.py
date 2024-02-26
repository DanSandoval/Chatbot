import Levenshtein

# Sample database of questions and answers (could be replaced with actual database queries)
database = {
    "What's the capital of France?": "Paris",
    "France capital city?": "Paris",
    "Capital of France": "Paris",
    "What's the largest planet in our solar system?": "Jupiter",
    "Largest planet in solar system?": "Jupiter",
    "Biggest planet in our solar system?": "Jupiter"
}

def find_similar_question(incoming_question, database_questions, threshold=0.8):
    similar_questions = []
    for db_question in database_questions:
        similarity = Levenshtein.ratio(incoming_question, db_question)
        if similarity >= threshold:
            similar_questions.append((db_question, similarity))
    return similar_questions

def get_answer(question, database):
    similar_questions = find_similar_question(question, database.keys())
    if similar_questions:
        best_match, _ = max(similar_questions, key=lambda x: x[1])  # Choose the most similar question
        return database[best_match]
    else:
        return None

# Example usage
# incoming_question = "What is the capital of France?"
# answer = get_answer(incoming_question, database)
# if answer:
#     print("Answer:", answer)
# else:
#     print("Answer not found in the database.")
