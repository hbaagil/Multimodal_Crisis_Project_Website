import streamlit as st
import datetime
import requests

st.title("Crisis Helper 🚨")

with st.form(key='params_for_api'):
    tweet = st.text_input('What is your tweet?', '')

    submitted = st.form_submit_button('Make prediction')

# Check if the form was submitted
if submitted:
    params = dict(tweet=tweet)
    api_url = 'https://crisishelper-qlahvylymq-ew.a.run.app/predict'

    # Send a GET request to the external API
    response = requests.get(api_url, params=params)

    # Check if the API request was successful
    if response.status_code == 200:
        result = response.json()
        st.success("Prediction Result:")

        # Display the prediction result with improved formatting
        for key, value in result.items():
            st.write(f"**{key}:** {value}")
    else:
        st.error("Prediction failed. Please try again later.")
