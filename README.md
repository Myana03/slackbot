# Building an AI Student Chatbot with LangChain, Spring Boot, and Slack

## Introduction

- A **Java Spring Boot** backend exposing student-related APIs
- An **OpenAI GPT-powered agent** using **LangChain**
- A **Slack bot** interface to communicate in natural language

No prior experience in AI or Slack APIs? No worries! This is written for absolute beginners.

---

## Project Overview

> Talk to your backend using natural language inside Slack.

You can:
- Add a student: `@studentbot Add student name=Riya, department=ECE`
- List by department: `@studentbot Show all CSE students`
- Get total count: `@studentbot How many students are there?`

### What We’re Using

| Component           | Tech Used                      |
|---------------------|--------------------------------|
| Backend             | Java + Spring Boot (H2 DB)     |
| LLM (AI Brain)      | OpenAI GPT-3.5                 |
| Agent Framework     | LangChain                      |
| Chat Interface      | Slack (with Bolt + SocketMode) |
| Optional UI         | Streamlit                      |

---

## Part 1: Set Up Spring Boot API

Build a Spring Boot app with:

- `GET /students`
- `GET /students/by-dept?dept=ECE`
- `POST /students` (JSON: `{"name": "Riya", "department": "ECE"}`)

Use `H2` in-memory DB and `EntityManager` for persistence. Test it locally on `http://localhost:8081`.

---

## Part 2: Python Agent + Slack Bot

### A. Environment Setup

```bash
cd slackbot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### B. LangChain Agent Code

We define tools that wrap around our backend APIs:

```python
def get_all_users(_=None):
    r = requests.get("http://localhost:8081/students")
    return json.dumps(r.json(), indent=2)

# Other tools for by-dept and create-student
```

Register these tools with `LangChain` and `OpenAI()` like this:

```python
agent = initialize_agent(
    tools=tools,
    llm=OpenAI(temperature=0),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)
```

### C. Slack Bot Setup

1. Create a Slack app at https://api.slack.com/apps
2. Enable:
   - Socket Mode
   - Bot Token Scopes: `app_mentions:read`, `chat:write`, `im:history`
3. Install it to your workspace
4. Get tokens and use this code:

```python
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.event("app_mention")
def mention_handler(event, say):
    user_input = event["text"].split(">", 1)[-1].strip()
    response = agent.invoke(user_input)
    say(response["output"])

SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
```

Now run your bot with:
```bash
python slackbot.py
```

Go to Slack and chat with your bot!

---

## Part 3: (Optional) Streamlit Chat UI

```python
st.title("🎓 Student Chatbot Agent")
query = st.chat_input("Ask me anything about students...")
if query:
    response = agent.invoke(query)
    st.write(response["output"])
```

Run it with:
```bash
streamlit run slackbot.py
```

---

## Project Structure

```
student-chatbot/
├── springboot-backend/  # Java project
├── slackbot/            # Python LangChain + Slack
│   ├── slackbot.py
│   └── requirements.txt
└── README.md
```

---

## Summary

In this beginner-friendly guide, we built a full AI assistant for managing students that:
- Uses GPT to understand natural language
- Maps requests to backend API tools
- Interacts from Slack and (optionally) Streamlit

Whether you're a developer, student, or curious learner — this project is a great way to bridge APIs, AI, and chat interfaces.

---

## Bonus Ideas

- Add SQL instead of in-memory H2
- Add LangGraph for workflows
- Add memory (ChatBuffer) to carry context
- Deploy using Docker + Ngrok

---

## Author

Built with ❤️ by **Myana Sai Nath**

GitHub: [github.com/myanasainath](https://github.com/myanasainath)
