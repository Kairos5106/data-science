import streamlit as st
import pickle

# Useful functions
def predict_website_status(user_input):
    website_status = classifier.predict(user_input)
    print(website_status)
    return website_status

# Page title & header
st.title("Phishing Website Detector")
st.markdown("A machine learning application used to identify a malicious website from its link. Input a link to get started!")

# Get user input
user_input = st.text_input("Enter a website link here")
st.markdown(f"Your input is: {user_input}")

# Load phishing detector model
pickle_in = open("phishing.pkl", "rb")
classifier = pickle.load(pickle_in)

# Pass data to model & produce output
result = ""
if st.button("Predict"):
    result = predict_website_status(user_input)

# Produce output
if result == 0:
    st.success("This website is safe")
elif result == 1:
    st.warning("This website is malicious!")
