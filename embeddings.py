import pandas as pd
import requests
import time

# Load the CSV file
df = pd.read_csv(r"C:\Users\Dan's PC\Desktop\testset.csv")

# Transforming the dataset from wide to long format
# Adjust 'ProviderID' to the actual column name that uniquely identifies each provider in your CSV
df_long = pd.melt(df, id_vars=["ProviderID"], var_name="Service", value_name="Description")


# Function to generate embedding for a single piece of text
def generate_embedding(description, api_key):
    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "input": description,
            "model": "text-embedding-ada-002"
        }
    )
    try:
        response.raise_for_status()
        # Adjusted to match the actual structure of the response
        embedding = response.json()
        return embedding
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None


# Load the CSV file
file_path = r"C:\Users\Dan's PC\Desktop\testset.csv"
df = pd.read_csv(file_path)

# Assuming 'service_description' is the column with the text you want embeddings for
# Replace 'service_description' with your actual column name
texts = df_long['Description'].tolist()  # This is correct

api_key = "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"

# Assuming df_long is already created by melting df

# Generate embeddings for each service description
# Assuming generate_embedding is defined correctly
embeddings = [generate_embedding(text, api_key) for text in texts]

# Store embeddings in the long-format DataFrame
df_long['Embedding'] = embeddings

# Save the updated DataFrame to a new CSV file
df_long.to_csv(r"C:/Users/Dan's PC/Desktop/testset_with_embeddings.csv", index=False)

