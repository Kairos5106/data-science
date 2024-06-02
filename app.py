import streamlit as st
import pickle

# For debugging - display status on terminal
def predict_website_status(user_input):
    try:
        # Wrap the user input in a list
        website_status = classifier.predict([user_input])
        print(f"Predicted status: {website_status}")
        return website_status
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None

# Page title & header
st.title("Phishing Website Detector")
st.markdown("A machine learning application used to identify a malicious website from its link. Input a link to get started!")

# Get user input
user_input = st.text_input("Enter a website link here")
st.markdown(f"Your input is: {user_input}")

# Load phishing detector model
try:
    with open("phishing.pkl", "rb") as pickle_in:
        classifier = pickle.load(pickle_in)
except Exception as e:
    st.error(f"Error loading model: {e}")

# Pass data to model & produce output
result = None
if st.button("Predict"):
    result = predict_website_status(user_input)

# Produce output and show in output section
if result is not None:
    if result[0] == 'good':  # Assuming 'good' means safe
        st.success("This website is safe")
    elif result[0] == 'bad':  # Assuming 'bad' means malicious
        st.warning("This website is malicious!")
else:
    st.error("Unable to predict the status of the website.")
