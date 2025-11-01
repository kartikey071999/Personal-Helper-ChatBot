import google.generativeai as genai
import os

# --- Put your functions from Step 2 here ---
# def add_task(description: str) -> str: ...
# def complete_task(task_id: int) -> str: ...
# def list_tasks() -> str: ...
# ... and a function to create the table ...

# 1. Configure your API key
genai.configure(api_key="YOUR_API_KEY")

# 2. Define your list of available tools
my_tools = [add_task, complete_task, list_tasks]

# 3. Initialize the model and tell it about your tools
model = genai.GenerativeModel(
    model_name='gemini-1.5-pro-latest',
    tools=my_tools
)

# 4. Start a chat session
chat = model.start_chat(enable_automatic_function_calling=True)

print("Hello! I'm Tasky-AI. How can I help you with your to-do list?")

# 5. The Main Loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        print("Goodbye!")
        break
    
    # Send the user's message to the model
    response = chat.send_message(user_input)
    
    # The SDK's `enable_automatic_function_calling=True` handles
    # the back-and-forth for you. Gemini will call your Python
    # functions as needed and then generate a final, natural
    # language response.
    
    print(f"Bot: {response.text}")