import streamlit as st
import pandas as pd
import requests
import time
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
    # Unique values for classification
    unique_labels = [
        'other_relevant_information',
        'not_humanitarian',
        'rescue_volunteering_or_donation_effort',
        'infrastructure_and_utility_damage',
        'injured_or_dead_people',
        'affected_individuals',
        'vehicle_damage',
        'missing_or_found_people'
    ]

    # Dictionary mapping labels to messages
    label_messages = {
        'other_relevant_information': "This text is about other relevant information.",
        'not_humanitarian': "This text is not related to humanitarian aid.",
        'rescue_volunteering_or_donation_effort': "This text contains information about rescue, volunteering, or donation efforts.",
        'infrastructure_and_utility_damage': "This text discusses infrastructure and utility damage.",
        'injured_or_dead_people': "This text mentions injured or dead individuals.",
        'affected_individuals': "This text is related to affected individuals.",
        'vehicle_damage': "This text indicates vehicle damage.",
        'missing_or_found_people': "This text involves missing or found people."
    }

    # Set up API parameters
    params = {'tweet': tweet}
    api_url = 'https://crisishelper-qlahvylymq-ew.a.run.app/predict_multi'

    # Send a GET request to the API
    response = requests.get(api_url, params=params)

    # Check if the API request was successful
    if response.status_code == 200:
        result = response.json()
        st.success("Text Classification Prediction Result:")

        # Extract and directly use the prediction from the list
        prediction = result.get("tweet_class")[0]

        if prediction in unique_labels:
            if prediction in label_messages:
                message = label_messages[prediction]
                st.markdown(f"**{message}**")
            else:
                st.error("No message defined for this prediction label.")
        else:
            st.error("Invalid prediction value received from the API.")
    else:
        st.error("Text classification prediction failed. Please try again later.")


if image_classification_button:
    # Handle image classification here
    st.info("Image classification.")


# Function to simulate real time prediction
def style_and_display_result(result):
    # Unique values for classification
    unique_labels = [
        'other_relevant_information',
        'not_humanitarian',
        'rescue_volunteering_or_donation_effort',
        'infrastructure_and_utility_damage',
        'injured_or_dead_people',
        'affected_individuals',
        'vehicle_damage',
        'missing_or_found_people'
    ]

    # Dictionary mapping labels to messages
    label_messages = {
        'other_relevant_information': "This text is about other relevant information.",
        'not_humanitarian': "This text is not related to humanitarian aid.",
        'rescue_volunteering_or_donation_effort': "This text contains information about rescue, volunteering, or donation efforts.",
        'infrastructure_and_utility_damage': "This text discusses infrastructure and utility damage.",
        'injured_or_dead_people': "This text mentions injured or dead individuals.",
        'affected_individuals': "This text is related to affected individuals.",
        'vehicle_damage': "This text indicates vehicle damage.",
        'missing_or_found_people': "This text involves missing or found people."
    }

    print("API Response:", result)  # Debug print to see the API response

    # Extract and directly use the prediction from the list
    prediction = result.get("tweet_class")[0]

    if 'tweet_class' in result:
        tweet_class = result['tweet_class'][0]
        print("Classification Result:", tweet_class)  # Debug print to see the classification result

        if prediction in unique_labels:
            if prediction in label_messages:
                message = label_messages[prediction]
                st.markdown(f"**{message}**")
            else:
                st.error("No message defined for this prediction label.")
        else:
            st.error("Invalid prediction value received from the API.")
    else:
        st.error("Text classification prediction failed. Please try again later.")

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
        api_url = 'https://crisishelper-qlahvylymq-ew.a.run.app/predict_multi'

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
