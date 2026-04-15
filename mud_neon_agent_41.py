# mud_neon_agent_41.py - CLEAN BETA (9/10 version - better context & focus)
import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_xai import ChatXAI

st.set_page_config(page_title="Momentum Mud Assistant", page_icon="🛢️", layout="wide")
st.title("🛢️ Momentum Mud Assistant beta")

llm = ChatXAI(
    model="grok-4-1-fast-non-reasoning",
    temperature=0.0,
    xai_api_key=st.secrets["XAI_API_KEY"],
    stop=None,
)

DATABASE_URL = "postgresql://MomentumDB:npg_VkXJWtT3GBO0@ep-blue-wind-anin6o30-pooler.c-6.us-east-1.aws.neon.tech:5432/neondb?sslmode=require"
db = SQLDatabase.from_uri(DATABASE_URL, schema="public")

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

CUSTOM_PREFIX = """You are the Momentum Mud Assistant beta. Stay focused on the current conversation and previous questions.

Answer ONLY with real data from the database. Be intelligent and flexible.

Key facts:
- BARITE and related products are in IntervalProducts (product, quantity, cost, uom, well_id). Search with ILIKE '%BARITE%'.
- Join to Wells on well_id to get well_name or "Pad".
- For pad names (Tres Equis, Dos Equis, Roosterfish, etc.), use LOWER("Pad") LIKE LOWER('%tres equis%') or similar for flexible matching.
- Always calculate totals with SUM(quantity) and SUM(cost). Include uom.
- If the user asks a follow-up, refer back to the previous context (e.g., the barite on Tres Equis pad).
- If no records, say "No records found for that query".

Use clean bullet points. Keep answers concise and relevant to the conversation."""

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

if prompt := st.chat_input("Ask about barite usage, product costs on any pad, follow-up questions, etc..."):
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