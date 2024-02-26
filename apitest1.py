import os
import Levenshtein
import leventest
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Sample database of questions and answers (could be replaced with actual database queries)


response = input("Bot: Hello I am a chatbot. I can answer your questions. Nice to meet you.\nUser: ")
while response != "exit":
    answer = leventest.get_answer(response, leventest.database)
    if answer:
        print("Bot: ", answer)
    else:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": response,
                }
            ],
            model="gpt-3.5-turbo",
        )

        print("Bot(from ChatGPT): " ,completion.choices[0].message.content)
    response = input("User: ")



# completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Say this is a test",
#         }
#     ],
#     model="gpt-3.5-turbo",
# )

# print(completion.choices[0].message.content)
