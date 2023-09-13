import streamlit as st
import pandas as pd
import requests
import time
import base64

import streamlit as st
import requests

import streamlit as st
import base64

import streamlit as st
import base64

import streamlit as st
import base64

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_jpg_as_page_bg(jpg_file):
    bin_str = get_base64_of_bin_file(jpg_file)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/jpeg;base64,%s");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)

set_jpg_as_page_bg('76827.jpg')


st.title("Crisis Helper 🚨")

# Create a single form for both text and image classification
with st.form(key='params_for_api'):
    st.markdown("### Text classification for disaster-related event 👇")
    tweet = st.text_input('What is your tweet?', '')
    text_classification_button = st.form_submit_button('Make text classification prediction')

    st.markdown("### Image classification for disaster-related event 👇")
    img_file_buffer = st.file_uploader('Upload an image')
    image_classification_button = st.form_submit_button('Make image classification prediction')

# Check which button was clicked and handle the request accordingly
if text_classification_button:
    params = dict(tweet=tweet)
    api_url = 'https://crisishelper-qlahvylymq-ew.a.run.app/predict_binary'

    # Send a GET request to the API
    response = requests.get(api_url, params=params)

    # Check if the API request was successful
    if response.status_code == 200:
        result = response.json()
        st.success("Text Classification Prediction Result:")

        # Extract and directly use the prediction from the list
        prediction = result.get("tweet_class")[0]

        if prediction == 'informative':
            st.markdown('<span style="color: green; font-weight: bold; font-size: 20px;">🚨 The text is informative for humanitarian aid and belongs to....</span>', unsafe_allow_html=True)
        elif prediction == 'not informative':
            st.markdown("**The text is not informative for humanitarian aid.**")
        else:
            st.error("Invalid prediction value.")
    else:
        st.error("Text classification prediction failed. Please try again later.")

if image_classification_button:
    # Handle image classification here
    st.info("Image classification.")


# Function to simulate real time prediction
def style_and_display_result(result):
    print("API Response:", result)  # Debug print to see the API response

    if 'tweet_class' in result:
        tweet_class = result['tweet_class'][0]
        print("Classification Result:", tweet_class)  # Debug print to see the classification result

        if tweet_class == 'informative':
            message = "The information provided is useful for humanitarian aid."
            # Style and display the message with red color for informative tweets
            st.markdown(f'<div style="color: red; font-weight: bold; font-size: 20px;">{message}</div>', unsafe_allow_html=True)
        elif tweet_class == 'not informative':
            message = "The information provided is not useful for humanitarian aid."
            # Style and display the message with black color for not informative tweets
            st.markdown(f'<div style="color: black; font-weight: bold; font-size: 20px;">{message}</div>', unsafe_allow_html=True)
        else:
            message = "Unknown classification result."
            # Style and display the message with a neutral color for unknown results
            st.markdown(f'<div style="font-weight: bold; font-size: 20px;">{message}</div>', unsafe_allow_html=True)
    else:
        st.error("Prediction result is missing 'tweet_class' key.")

st.title("Crisis Helper Real-Time Simulation 🌐")

# Load a DataFrame with a "tweet_text" column
df = pd.read_csv('/media/hamzah/Ubud/code/00_Data_Science/.crisis_helper/mlops/data/raw/df_test_binary.csv')

# Limit the simulation to the first 10 rows
df = df.sample(n=10)

# Create a button to start the simulation
if st.button("Start Simulation"):
    for index, row in df.iterrows():
        st.subheader("Tweet:")
        st.write(row['tweet_text'])

        params = dict(tweet=row['tweet_text'])
        api_url = 'https://crisishelper-qlahvylymq-ew.a.run.app/predict_binary'

        try:
            # Send a GET request to the API
            response = requests.get(api_url, params=params)

            print("API Request URL:", response.url)  # Debug print to see the API request URL

            # Check if the API request was successful
            if response.status_code == 200:
                result = response.json()
                style_and_display_result(result)
            else:
                st.error("Prediction failed for this tweet. Please try again later.")
        except Exception as e:
            st.error(f"Error: {e}")

        st.markdown("---")

# Add a stop button to end the simulation
if st.button("Stop Simulation"):
    st.warning("Simulation stopped.")

# Add a container div for the attribution link
st.markdown(
    """
    <div style="position: absolute; bottom: 0; right: 0; padding: 10px;">
        <a href="http://www.freepik.com" style="color: #555;">Designed by rawpixel.com / Freepik</a>
    </div>
    """,
    unsafe_allow_html=True
)
