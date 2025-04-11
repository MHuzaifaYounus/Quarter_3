import streamlit as st
from cryptography.fernet import Fernet
import hashlib
import time
import json


key = st.secrets["key"]["cipher_key"].encode() 
cipher = Fernet(key)

with open('stored_data.json', 'r') as file:
    data = json.load(file)

if "stored_data" not in st.session_state:
    st.session_state.stored_data = data
    
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text, passkey):
    hashed_passkey = hash_passkey(passkey)

    for key, value in st.session_state.stored_data.items():
        if value["encrypted_text"] == encrypted_text and value["passkey"] == hashed_passkey:
            st.session_state.failed_attempts = 0
            return cipher.decrypt(encrypted_text.encode()).decode()
       
    st.session_state.failed_attempts += 1
    return None



if "islogin" not in st.session_state:
    st.session_state.islogin = False


if st.session_state.islogin == False:
    choice = "Login"
    

else:
    choice = st.sidebar.radio("Navigation", ["Home", "Store Data", "Retrieve Data"])


st.title("Secure Data Encryption")
if choice == "Home":
    st.subheader("🏠 Welcome to the Secure Data System")
    st.write("Use this app to **securely store and retrieve data** using unique passkeys.")
    display_data = {
        "Data": {title: info["encrypted_text"] for title, info in st.session_state.stored_data.items()} 
    }
    st.table(display_data)
        

elif choice == "Store Data":
    st.subheader("📂 Store Data Securely")
    title = st.text_input("Enter Title")
    user_data = st.text_area("Enter Data:")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.button("Encrypt"):
        if title and user_data and passkey:
            encrypted_text = encrypt_data(user_data)
            st.session_state.stored_data[title] = {"encrypted_text": encrypted_text, "passkey":hash_passkey(passkey)}

            with open('stored_data.json', 'w') as f:
                json.dump(st.session_state.stored_data, f)

            st.success("Successfully Stored Data")
          
        else:
            st.error("Both Fields Are Required")

elif choice == "Retrieve Data":
    st.subheader("🔍 Retrieve Your Data")
    encrypted_text = st.text_area("Enter Encrypted Data:")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.button("Decrypt"):
        if encrypted_text and passkey:
            decrypted_text = decrypt_data(encrypted_text, passkey)

            if decrypted_text:
                st.success(f"✅ Decrypted Data: {decrypted_text}")
            else:
                st.error(f"❌ Incorrect passkey! Attempts remaining: {3 - st.session_state.failed_attempts}")

                if st.session_state.failed_attempts >= 3:
                    st.warning("🔒 Too many failed attempts! Redirecting to Login Page.")
                    time.sleep(1)
                    st.session_state.islogin = False
                    st.rerun()
        else:
            st.error("⚠️ Both fields are required!")


elif choice == "Login":
    st.subheader("🔑 Reauthorization Required")
    login_pass = st.text_input("Enter Master Password:", type="password")

    if st.button("Login"):
        entered_hash = hash_passkey(login_pass)
        stored_hash = st.secrets["auth"]["admin_pass_hash"]

        if entered_hash == stored_hash:
            st.session_state.failed_attempts = 0
            st.success("✅ Reauthorized successfully! Redirecting to Retrieve Data...")
            time.sleep(1)
            st.session_state.islogin = True
            st.rerun()
        else:
            st.error("❌ Incorrect password!")

