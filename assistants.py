import json
from IPython.display import display
from openai import OpenAI
import os

assistant_id = os.getenv("OPENAI_ASSISTANT_ID") # or a hard-coded ID like "asst-..."

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))

def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )


def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(assistant_id, thread, user_input)
    return thread, run


# Emulating concurrent user requests
thread1, run1 = create_thread_and_run(
    "i need a service provider who has emergency rooms and physicians offices"
)
thread2, run2 = create_thread_and_run("I want one with physicians offices but no emergency department?")
thread3, run3 = create_thread_and_run("I want it in a hospital but not with attending ltpac physicians")

import time

# Pretty printing helper
def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()


# Waiting in a loop
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


# Wait for Run 1
run1 = wait_on_run(run1, thread1)
pretty_print(get_response(thread1))

# Wait for Run 2
run2 = wait_on_run(run2, thread2)
pretty_print(get_response(thread2))

# Wait for Run 3
run3 = wait_on_run(run3, thread3)
pretty_print(get_response(thread3))

# Thank our assistant on Thread 3 :)
run4 = submit_message(os.getenv("OPENAI_ASSISTANT_ID"), thread3, "Thank you!")
run4 = wait_on_run(run4, thread3)
pretty_print(get_response(thread3))

# Now all Runs are executing...


# import json
# from IPython.display import display
# from openai import OpenAI
# import os

# def show_json(obj):
#     display(json.loads(obj.model_dump_json()))

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))

# assistant = client.beta.assistants.create(
#     name="Math Tutor",
#     instructions="You are a personal math tutor. Answer questions briefly, in a sentence or less.",
#     model="gpt-4-1106-preview",
# )
# show_json(assistant)

# thread = client.beta.threads.create()
# show_json(thread)

# message = client.beta.threads.messages.create(
#     thread_id=thread.id,
#     role="user",
#     content="I need to solve the equation `3x + 11 = 14`. Can you help me?",
# )
# show_json(message)

# run = client.beta.threads.runs.create(
#     thread_id=thread.id,
#     assistant_id=assistant.id,
# )
# show_json(run)

# import time

# def wait_on_run(run, thread):
#     while run.status == "queued" or run.status == "in_progress":
#         run = client.beta.threads.runs.retrieve(
#             thread_id=thread.id,
#             run_id=run.id,
#         )
#         time.sleep(0.5)
#     return run

# run = wait_on_run(run, thread)
# show_json(run)

# # Create a message to append to our thread
# message = client.beta.threads.messages.create(
#     thread_id=thread.id, role="user", content="Could you explain this to me?"
# )

# # Execute our run
# run = client.beta.threads.runs.create(
#     thread_id=thread.id,
#     assistant_id=assistant.id,
# )

# # Wait for completion
# wait_on_run(run, thread)

# # Retrieve all the messages added after our last user message
# messages = client.beta.threads.messages.list(
#     thread_id=thread.id, order="asc", after=message.id
# )
# show_json(messages)

# # Create a message to append to our thread
# message = client.beta.threads.messages.create(
#     thread_id=thread.id, role="user", content="Could you explain this to me?"
# )

# # Execute our run
# run = client.beta.threads.runs.create(
#     thread_id=thread.id,
#     assistant_id=assistant.id,
# )

# # Wait for completion
# wait_on_run(run, thread)

# # Retrieve all the messages added after our last user message
# messages = client.beta.threads.messages.list(
#     thread_id=thread.id, order="asc", after=message.id
# )
# show_json(messages)