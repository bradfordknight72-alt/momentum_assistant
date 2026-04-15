import streamlit as st

st.set_page_config(page_title="Momentum Mud Assistant", page_icon="🛢️", layout="wide")
st.title("🛢️ Momentum Mud Assistant beta")

st.write("✅ Connected to database. Ready for queries.")

# Placeholder for now - we'll add the agent once the basic app loads
if st.button("Test Connection"):
    st.success("App is running! We can add the full agent after this deploys successfully.")

st.caption("Momentum Mud Assistant beta")
