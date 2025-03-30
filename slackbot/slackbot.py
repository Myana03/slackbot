import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.llms import OpenAI  # or Ollama(model="llama2")
import requests
import os
import json

# ✅ Load LLM
os.environ["OPENAI_API_KEY"] = 'openai token'
SLACK_BOT_TOKEN = "slack_bot_token"
SLACK_APP_TOKEN = "slack_app_token"

llm = OpenAI(temperature=0)

# ✅ Define Tools
def get_all_users(_=None):
    r = requests.get("http://localhost:8081/students")
    data = r.json()
    return f"There are {len(data)} students.\n\n{json.dumps(data, indent=2)}"

def get_by_dept(dept):
    dept = dept.strip().replace("'", "").replace('"', "")
    r = requests.get(f"http://localhost:8081/students/by-dept?dept={dept}")
    data = r.json()
    return f"There are {len(data)} in {dept}:\n\n{json.dumps(data, indent=2)}"

def create_student(input):
    try:
        cleaned = input.replace("'", "").replace('"', "").strip()
        parts = cleaned.split(",")
        data = {k.strip(): v.strip() for k, v in [p.split("=") for p in parts]}
        r = requests.post("http://localhost:8081/students", json=data)
        return "✅ Student created!" if r.status_code == 200 else r.text
    except Exception as e:
        return f"❌ Error: {e}"

tools = [
    Tool(name="GetAllUsers", func=get_all_users, description="Get all students"),
    Tool(name="GetStudentsByDepartment", func=get_by_dept, description="Input a department like 'CSE'"),
    Tool(name="CreateStudent", func=create_student, description="Format: 'name=Riya, department=ECE'")
]

# ✅ Initialize Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=4,
    early_stopping_method="generate"
)

# # ✅ Streamlit UI
# st.title("🎓 Student Chatbot Agent")

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# query = st.chat_input("Ask me anything about students...")

# if query:
#     with st.spinner("Thinking..."):
#         response = agent.invoke(query)
#         st.session_state.chat_history.append(("user", query))
#         st.session_state.chat_history.append(("ai", response["output"]))

# # 💬 Display Chat
# for role, message in st.session_state.chat_history:
#     st.chat_message(role).write(message)



from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# ✅ Set up Slack Bot
app = App(token=SLACK_BOT_TOKEN)

# @app.event("message")
# def handle_any_message(event, say):
#     print("📩 Got a message:", event)
#     say("👋 I saw your message!")

# ✅ Mentioned in a public channel
@app.event("app_mention")
def handle_mention(event, say):
    text = event.get("text", "")
    user_input = text.split(">", 1)[-1].strip()
    print(f"📣 Mention Handler Input: {user_input}")
    response = agent.invoke(user_input)
    say(response["output"])

# ✅ Direct message to bot (not using @mention)
@app.event("message")
def handle_message(event, say):
    # Skip messages from the bot itself to avoid loops
    if event.get("subtype") == "bot_message":
        return

    user_input = event.get("text", "")
    print(f"📩 DM Handler Input: {user_input}")
    response = agent.invoke(user_input)
    say(response["output"])

# ✅ Start Slack bot using Socket Mode
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()