import streamlit as st


st.header("📀Save Password ")
st.write('🔐 "Secure Today, Access Anytime - Save Your Passwords Safely!" 🚀')

if "passwords" not in st.session_state:
    st.session_state.passwords = []


title = st.text_input("Give it a Name:")
password = st.text_input("Enter Your Password Here:",type="password")
if st.button("🔑Save"):
    if password and title:
        if len(st.session_state.passwords) != 0:
            for entry in st.session_state.passwords:
                if entry["password"] == password:
                    st.error("Password Already Exit Plz Set a Different One")
                    break
                else:
                    st.session_state.passwords.append({"title":title, "password":password})
                    st.success("Password Successfully Saved")
                    break
        else:
            st.session_state.passwords.append({"title":title, "password":password})
            st.success("Password Successfully Saved")
            
    else:
        st.error("Plz fill all the fields")
        
if st.button("Show Passwords"):
    st.table(st.session_state.passwords)
    