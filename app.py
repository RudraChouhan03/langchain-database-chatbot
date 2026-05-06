# Import Streamlit library for building web apps with Python
import streamlit as st

# Path is used to handle file paths in an OS-independent way
from pathlib import Path

# This function helps create an agent that can interact with SQL databases
from langchain.agents import create_sql_agent

# Wrapper that allows LangChain to interact with SQL databases
from langchain.sql_database import SQLDatabase

# Defines different types of agents (how agent behaves)
from langchain.agents.agent_types import AgentType

# Used to display intermediate steps of agent in Streamlit UI
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

# Toolkit provides tools (like query execution) to the agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit

# SQLAlchemy is used to create database engine/connection
from sqlalchemy import create_engine

# sqlite3 is used to connect SQLite databases
import sqlite3

# ChatGroq is LLM wrapper to use Groq API (Llama models)
from langchain_groq import ChatGroq


# Set page configuration (title and icon of web app)
st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🦜")

# Title displayed on the main page
st.title("🦜 LangChain: Chat with SQL DB")


# Constants to identify which database user selects
LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"


# Options shown in sidebar radio button
radio_opt = ["Use SQLLite 3 Database- Student.db", "Connect to you MySQL Database"]

# Sidebar radio button for selecting database type
selected_opt = st.sidebar.radio(
    label="Choose the DB which you want to chat",
    options=radio_opt
)


# If user selects MySQL option (index 1)
if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL  # Set DB type as MySQL

    # Take MySQL connection details from user
    mysql_host = st.sidebar.text_input("Provide MySQL Host")
    mysql_user = st.sidebar.text_input("MYSQL User")
    mysql_password = st.sidebar.text_input("MYSQL password", type="password")
    mysql_db = st.sidebar.text_input("MySQL database")

else:
    # Otherwise use local SQLite DB
    db_uri = LOCALDB


# Take Groq API key from user (hidden input)
api_key = st.sidebar.text_input(label="GRoq API Key", type="password")


# If API key not provided
if not api_key:
    st.info("Please add the groq api key")
    st.stop()


## Initialize LLM model
# ChatGroq connects to Groq API using Llama3 model
# streaming=True means response will come token-by-token (live typing effect)
llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.1-8b-instant",
    streaming=True
)


# Cache database connection (to avoid reconnecting every time)
# ttl="2h" means cache will be valid for 2 hours
@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):

    # If using local SQLite DB
    if db_uri == LOCALDB:

        # Get absolute path of student.db file
        dbfilepath = (Path(__file__).parent / "student.db").absolute()

        # Print path (for debugging in terminal)
        print(dbfilepath)

        # Create a read-only SQLite connection
        # mode=ro ensures database cannot be modified
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)

        # Create SQLAlchemy engine using this connection
        return SQLDatabase(create_engine("sqlite:///", creator=creator))


    # If using MySQL database
    elif db_uri == MYSQL:

        # Check if all required credentials are provided
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MySQL connection details.")
            st.stop()  # Stop execution if details missing

        # Create connection string for MySQL
        return SQLDatabase(
            create_engine(
                f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
            )
        )


# Configure database based on selection
if db_uri == MYSQL:
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
else:
    db = configure_db(db_uri)


## Create toolkit
# Toolkit gives agent ability to:
# - run SQL queries
# - inspect tables
toolkit = SQLDatabaseToolkit(db=db, llm=llm)


# Create SQL agent
agent = create_sql_agent(
    llm=llm,                       # LLM brain
    toolkit=toolkit,               # tools for DB interaction
    verbose=True,                  # shows reasoning steps in console
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    # ZERO_SHOT means no prior examples needed
    # REACT means Reason + Act (agent thinks and acts step-by-step)
    handle_parsing_errors=True
)


# Initialize chat history
# If no previous messages OR user clicks "Clear message history"
if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]


# Display chat history on screen
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


# Input box for user query
user_query = st.chat_input(placeholder="Ask anything from the database")


# When user enters a query
if user_query:

    # Save user message in session history
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Display user message
    st.chat_message("user").write(user_query)


    # Assistant response block
    with st.chat_message("assistant"):

        # Streamlit callback handler (shows agent thinking steps)
        streamlit_callback = StreamlitCallbackHandler(st.container())

        # Run agent on user query
        # Agent will:
        # 1. Understand question
        # 2. Generate SQL query
        # 3. Execute query
        # 4. Return result
        response = agent.run(user_query, callbacks=[streamlit_callback])

        # Save response in chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Display response
        st.write(response)