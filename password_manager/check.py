import streamlit as st
import re


st.header("🔒 Check Password Strength")
st.write("Secure Your Passwords, Strengthen Your Safety! 🔒🚀")
 


def check_password_strength(password):

    score = 0
    
    # Length Check
    if len(password) >= 8:
        st.write("✅ Password should be at least 8 characters long.")
        score += 1
    else:
        st.write("❌ Password should be at least 8 characters long.")
    
    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        st.write("✅ Include both uppercase and lowercase letters.")
        score += 1
    else:
        st.write("❌ Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        st.write("✅ Add at least one number (0-9).")
        score += 1
    else:
        st.write("❌ Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        st.write("✅ Include at least one special character (!@#$%^&*).")
        score += 1
    else:
        st.write("❌ Include at least one special character (!@#$%^&*).")
    
    # Strength Rating
    if password:
        if score == 4:
            st.success("✅ Strong Password!")
            
        elif score == 3:
            st.write("⚠️ Moderate Password - Consider adding more security features.")
            
        else:
            st.error("❌ Weak Password - Improve it using the suggestions above.")
     

password = st.text_input("Enter Your Password Here",type="password")
check_password_strength(password)


   

