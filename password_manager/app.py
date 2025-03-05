import streamlit as st

st.header("🔑Huza Password Manager")

check_pg = st.Page("check.py",title="Check Password", icon="✅")
generate_pg = st.Page("generate.py" , title="Generate Password" , icon="🤖")
save_pg = st.Page("save.py" , title="Save Password" , icon="📀")

pg = st.navigation([check_pg, generate_pg,save_pg])
pg.run()