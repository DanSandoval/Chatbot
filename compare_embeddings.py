import pandas as pd
import requests
import json
from scipy.spatial.distance import cosine
import os

# Function to generate an embedding using OpenAI's API
def generate_embedding(text, api_key):
    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"input": text, "model": "text-embedding-ada-002"}
    )
    response.raise_for_status()
    # Assuming the API returns the embedding directly under 'data' then 'embedding'
    embedding = response.json()['data'][0]['embedding']
    return embedding


# Updated function to calculate the cosine similarity score
def calculate_cosine_similarity(vec1, vec2):
    # Calculate cosine distance
    cosine_dist = cosine(vec1, vec2)
    # Convert cosine distance to similarity score
    cosine_similarity_score = 1 - cosine_dist
    return cosine_similarity_score

# Function to extract the actual embedding vector from the JSON-like string
def extract_embedding(embedding_str):
    try:
        embedding_dict = json.loads(embedding_str)
    except json.JSONDecodeError:
        # Attempt to fix common formatting issues and retry parsing
        fixed_str = embedding_str.replace("'", '"')
        embedding_dict = json.loads(fixed_str)
    
    embedding_vector = embedding_dict['data'][0]['embedding']
    return embedding_vector

# Generate Embedding for User Input (Pseudo code, replace with actual embedding generation)
user_input = "sun and rain and cloud snow"
api_key = os.getenv("OPENAI_API_KEY")  # Replace with your actual API key
user_embedding = generate_embedding(user_input, api_key)  # Replace with actual embedding generation code

# Load Saved Embeddings and Parse Them
df_embeddings = pd.read_csv("C:/Users/Dan's PC/Desktop/tinyWeatherSet_with_embeddings.csv")
df_embeddings['ParsedEmbedding'] = df_embeddings['Embedding'].apply(extract_embedding)

# Calculate cosine similarity between user input embedding and each saved embedding
similarities = df_embeddings['ParsedEmbedding'].apply(lambda emb: calculate_cosine_similarity(user_embedding, emb))

# Create a DataFrame with similarities for better manipulation
df_similarities = pd.DataFrame({'Similarity': similarities})
df_similarities['ProviderID'] = df_embeddings['ProviderID']
df_similarities['Service'] = df_embeddings['Service']

# Sort the DataFrame by similarity and get the top 3 matches
top_3_matches = df_similarities.nlargest(3, 'Similarity')

print("Top 3 matching providers and services with similarity scores:")
print(top_3_matches)
