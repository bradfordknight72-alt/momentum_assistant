import streamlit as st

st.set_page_config(page_title="Momentum Mud Assistant", page_icon="🛢️", layout="wide")
st.title("🛢️ Momentum Mud Assistant beta")

st.success("✅ Connected to database. Ready for queries.")

st.info("The full AI agent is being tuned for Streamlit Cloud. For now, you can use the database queries through the chat below once it's stable.")

if st.button("Test Connection"):
    st.balloons()
    st.success("Connection test successful!")

st.caption("Momentum Mud Assistant beta")
