<div align="center">

# 🦜 SQL Chatbot using LangChain + Streamlit

### AI-powered chatbot for interacting with SQL databases using natural language

</div>

---

## 🚀 Overview

This project is an AI-powered SQL chatbot that allows users to interact with SQLite or MySQL databases using natural language queries.

The application uses:
- LangChain SQL Agent
- Groq LLM
- Streamlit interface

Users can ask questions in plain English, and the chatbot automatically generates and executes SQL queries to retrieve results from the database.

---

## ✨ Features

✅ Chat with SQLite database using natural language  
✅ MySQL database support  
✅ Streamlit-based interactive UI  
✅ LangChain SQL Agent integration  
✅ Groq LLM support  
✅ Real-time response streaming  
✅ Intermediate agent reasoning display  

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Frontend web application |
| LangChain | AI agent framework |
| Groq API | LLM inference |
| SQLite | Local database |
| MySQL | External database support |
| SQLAlchemy | Database connectivity |

---

## 📁 Project Structure

```text
8-Chat-SQL/
│
├── app.py
├── sqlite.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🗄️ Database Schema

### STUDENT Table

```sql
STUDENT(
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
)
```

Sample records are inserted using `sqlite.py`.

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/RudraChouhan03/langchain-database-chatbot.git
cd langchain-database-chatbot
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv myvenv
```

### Activate Virtual Environment

#### Windows

```bash
myvenv\Scripts\activate
```

#### Linux / Mac

```bash
source myvenv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Create SQLite Database

```bash
python sqlite.py
```

This creates `student.db` with sample records.

---

### 5️⃣ Run Application

```bash
streamlit run app.py
```

---

## 🔑 Groq API Key Setup

Get your API key from:

👉 https://console.groq.com/keys

Paste the API key into the sidebar input field after starting the application.

---

## 💬 Sample Questions

- Show all students
- Who scored the highest marks?
- Show students from Data Science class
- List all students from section A
- What is the average marks of students?

---

## 🧠 How It Works

```text
User Query
   ↓
LangChain SQL Agent
   ↓
LLM generates SQL query
   ↓
Database execution
   ↓
Results returned to user
```

---

## 🔮 Future Improvements

- Chat memory support
- CSV upload support
- Query result visualization
- Download query results
- Multi-database connection support
- Authentication system

---

## 👨‍💻 Author

### Rudra Chouhan

Computer Science Engineering Student  
Interested in Data Science, Generative AI, and Agentic AI

---

## 📄 License

This project is licensed under the MIT License.