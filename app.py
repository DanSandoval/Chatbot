from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI


app = Flask(__name__)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load instructions from file
def load_instructions():
    with open('instructions.txt', 'r') as file:
        instructions = file.read().strip()
    return instructions

instructions = load_instructions()

import time  # Make sure to import time at the top of your script



def interact_with_bot(question):
    assistant_id = os.getenv('OPENAI_ASSISTANT_ID')

    try:
        thread = client.beta.threads.create()

        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id,
            instructions=instructions
        )

        # Wait for the run to complete
        count = 0
        while run.status in ["queued", "in_progress"] and count < 5:
            time.sleep(2)  # Wait for 2 seconds before checking again
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            count += 1

        print(f"Final Run Status: {run.status}")

        if run.status == "completed":
            messages_response = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            messages = messages_response.data

            # Assuming we want the last assistant message
            last_message_text = None
            for message in reversed(messages):
                if message['role'] == 'assistant':
                    # Assuming 'content' is structured as expected; may need adjustment
                    last_message_text = message['content']
                    break

            if last_message_text is not None:
                return last_message_text
            else:
                return "I couldn't find a response, please try again."
        else:
            return "I'm sorry, I'm having trouble processing your request right now."

    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while processing your request."



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    if user_input.lower() == 'exit':
        return jsonify({'response': 'Goodbye!'})
    else:
        answer = interact_with_bot(user_input)
        # Ensure the response is a string or a structure that can be serialized to JSON
        return jsonify({'response': answer})


if __name__ == '__main__':
    app.run(debug=True)
