import streamlit as st
import random
import string

st.header("🤖Generate Password ")
st.write('🔒 "Secure Every Login - Generate Strong Passwords Instantly!" 🚀')

length = st.slider("Select Password Length",min_value=8,max_value=25)
isUpper = st.checkbox("Include Uppercase")
isLower = st.checkbox("Include LowerCase")
isNums = st.checkbox("Include Numbers")
isSpec = st.checkbox("Include Special Charachters")

def Generate_pass(length , isUpper , isLower, isNums, isSpec):
    charachters = ''
    if isUpper | isLower | isNums | isSpec:
        if isUpper:
            charachters = charachters + string.ascii_uppercase
        if isLower:
            charachters = charachters + string.ascii_lowercase
        if isNums:
            charachters = charachters + string.digits
        if isSpec:
            charachters = charachters + string.punctuation
        password = ''
        for i in range(length):     
            password = password + random.choice(charachters)
        return password
    else:
        st.error("Plz Select atleast one checkBox")
    
        



if st.button("🔢Generate"):
    output_password = Generate_pass(length,isUpper,isLower,isNums,isSpec)
    if output_password:
        st.code(output_password,language='')

