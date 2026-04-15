# mud_neon_agent_41.py - FIXED FOR STREAMLIT CLOUD
import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_xai import ChatXAI

st.set_page_config(page_title="Momentum Mud Assistant", page_icon="🛢️", layout="wide")
st.title("🛢️ Momentum Mud Assistant beta")

# Load API key safely from secrets
xai_key = st.secrets["XAI_API_KEY"]

llm = ChatXAI(
    model="grok-4-1-fast-non-reasoning",
    temperature=0.0,
    xai_api_key=xai_key,
)

DATABASE_URL = "postgresql://MomentumDB:npg_VkXJWtT3GBO0@ep-blue-wind-anin6o30-pooler.c-6.us-east-1.aws.neon.tech:5432/neondb?sslmode=require"
db = SQLDatabase.from_uri(DATABASE_URL, schema="public")

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

CUSTOM_PREFIX = """You are the Momentum Mud Assistant beta. Answer ONLY with real data from the database.

Key facts:
- Products (including BARITE) are in IntervalProducts. Search with ILIKE '%BARITE%'.
- Join to Wells on well_id for pad/well info.
- For any pad, use LOWER("Pad") LIKE LOWER('%pad name%') for flexible matching.
- Always use SUM(quantity) for totals.

Be precise and use bullet points."""

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    prefix=CUSTOM_PREFIX,
    verbose=False,
    agent_type="zero-shot-react-description",
    handle_parsing_errors=True,
    top_k=100,
    max_iterations=12
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about barite usage, product costs on any pad, wells, etc..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Querying master database..."):
            try:
                response = agent_executor.invoke({"input": prompt})
                answer = response.get("output", "No data found.")
            except Exception as e:
                answer = f"Query error: {str(e)}"
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

st.caption("Momentum Mud Assistant beta")# mud_neon_agent_41.py - FIXED FOR STREAMLIT CLOUD
import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_xai import ChatXAI

st.set_page_config(page_title="Momentum Mud Assistant", page_icon="🛢️", layout="wide")
st.title("🛢️ Momentum Mud Assistant beta")

# Load API key safely from secrets
xai_key = st.secrets["XAI_API_KEY"]

llm = ChatXAI(
    model="grok-4-1-fast-non-reasoning",
    temperature=0.0,
    xai_api_key=xai_key,
)

DATABASE_URL = "postgresql://MomentumDB:npg_VkXJWtT3GBO0@ep-blue-wind-anin6o30-pooler.c-6.us-east-1.aws.neon.tech:5432/neondb?sslmode=require"
db = SQLDatabase.from_uri(DATABASE_URL, schema="public")

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

CUSTOM_PREFIX = """You are the Momentum Mud Assistant beta. Answer ONLY with real data from the database.

Key facts:
- Products (including BARITE) are in IntervalProducts. Search with ILIKE '%BARITE%'.
- Join to Wells on well_id for pad/well info.
- For any pad, use LOWER("Pad") LIKE LOWER('%pad name%') for flexible matching.
- Always use SUM(quantity) for totals.

Be precise and use bullet points."""

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    prefix=CUSTOM_PREFIX,
    verbose=False,
    agent_type="zero-shot-react-description",
    handle_parsing_errors=True,
    top_k=100,
    max_iterations=12
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about barite usage, product costs on any pad, wells, etc..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Querying master database..."):
            try:
                response = agent_executor.invoke({"input": prompt})
                answer = response.get("output", "No data found.")
            except Exception as e:
                answer = f"Query error: {str(e)}"
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

st.caption("Momentum Mud Assistant beta")
