import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key='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')

OPENAI_THREAD_ID: str = "thread_00QhnzAIFe7iV6XMQRxqxFuB"
# # Step 1: Create an Assistant
# my_assistant = client.beta.assistants.create(
#     model="gpt-3.5-turbo",
#     instructions="You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
#     name="Math Tutor111111",
#     tools=[{"type": "code_interpreter"}],
# )
# print(f"This is the assistant object: {my_assistant} \n")



# # Step 2: Create a Thread
# my_thread = client.beta.threads.create()
# print(f"This is the thread object: {my_thread} \n")

# # Step 3: Add a Message to a Thread
# my_thread_message = client.beta.threads.messages.create(
#   thread_id=OPENAI_THREAD_ID,
#   role="user",
#   content="I need to solve the equation `3x + 11 = 14`. Can you help me?",
# )
# print(f"This is the message object: {my_thread_message} \n")

# Step 4: Run the Assistant
my_run = client.beta.threads.runs.create(
  thread_id=OPENAI_THREAD_ID,
  assistant_id=os.environ.get("OPENAI_ASSISTANT_ID")
)
print(f"This is the run object: {my_run} \n")

# Step 5: Periodically retrieve the Run to check on its status to see if it has moved to completed
while my_run.status != "completed":
    keep_retrieving_run = client.beta.threads.runs.retrieve(
        thread_id=OPENAI_THREAD_ID,
        run_id=my_run.id
    )
    print(f"Run status: {keep_retrieving_run.status}")

    if keep_retrieving_run.status == "completed":
        print("\n")
        break

# Step 6: Retrieve the Messages added by the Assistant to the Thread
all_messages = client.beta.threads.messages.list(
  thread_id=OPENAI_THREAD_ID
)

print("------------------------------------------------------------ \n")

# print(f"User: {my_thread_message.content[0].text.value}")
# print(f"Assistant: {all_messages}")