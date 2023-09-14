import streamlit as st
import pandas as pd
import requests
import time
import base64
import os

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


# Styling the app title with added space and centering
st.markdown("<h1 style='text-align: center;'><b>Crisis Helper 🚨</b></h1>", unsafe_allow_html=True)

# Adding space after the title
st.markdown("<br>", unsafe_allow_html=True)

# Styling the app description with enhanced formatting and design
description = """
<div style='font-size: 20px; color: #444; text-align: center;'>
    <b><i>Classification of crisis-related content to facilitate rapid resource allocation</i></b>
</div>
"""

st.markdown(description, unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)

# Create a single form for both text and image classification
with st.form(key='params_for_api'):
    st.markdown("### Crisis-Helper Text Classifier")
    tweet = st.text_input('What is your tweet?', '')
    text_classification_button = st.form_submit_button('Classify Text')
    text_prediction_output = st.empty()  # Placeholder for text classification output

    st.markdown("### Crisis-Helper Image Classifier")
    img_file_buffer = st.file_uploader('Upload an image')
    image_classification_button = st.form_submit_button('Classify Image')
    image_prediction_output = st.empty()  # Placeholder for image classification output


if text_classification_button:
    # Handle text classification here
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

    label_messages = {
        'other_relevant_information': "Relevant information",
        'not_humanitarian': "Not related to humanitarian aid",
        'rescue_volunteering_or_donation_effort': "Information about rescue, volunteering, or donation efforts",
        'infrastructure_and_utility_damage': "Infrastructure and utility damage",
        'injured_or_dead_people': "Injured or dead individuals",
        'affected_individuals': "Affected individuals",
        'vehicle_damage': "Vehicle damage",
        'missing_or_found_people': "Missing or found people"
    }

    params = {'tweet': tweet}
    api_url = 'https://crisishelper-qlahvylymq-ew.a.run.app/predict_multi'

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        result = response.json()

        prediction = result.get("tweet_class")[0]

        if prediction in unique_labels:
            if prediction in label_messages:
                message = label_messages[prediction]
                if prediction == 'not_humanitarian':
                    text_prediction_output.markdown(
                        f"<p style='font-size: 18px; color: blue;font-weight: bold;'>{message}</p>",
                        unsafe_allow_html=True
                    )
                else:
                    text_prediction_output.markdown(
                        f"<p style='font-size: 18px; color: red; font-weight: bold;'>🚨{message}🚨</p>",
                        unsafe_allow_html=True
                    )
            else:
                text_prediction_output.error("No message defined for this prediction label.")
        else:
            text_prediction_output.error("Invalid prediction value received from the API.")
    else:
        text_prediction_output.error("Text classification prediction failed. Please try again later.")


if image_classification_button:
    # Handle image classification here
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
    label_messages = {
        'other_relevant_information': "Relevant information",
        'not_humanitarian': "Not related to humanitarian aid",
        'rescue_volunteering_or_donation_effort': "Information about rescue, volunteering, or donation efforts",
        'infrastructure_and_utility_damage': "Infrastructure and utility damage",
        'injured_or_dead_people': "Injured or dead individuals",
        'affected_individuals': "Affected individuals",
        'vehicle_damage': "Vehicle damage",
        'missing_or_found_people': "Missing or found people"
    }

    if img_file_buffer is not None:
        files = {'img': img_file_buffer.read()}
        api_url_image = 'https://crisishelper-qlahvylymq-ew.a.run.app/upload_image'

        response = requests.post(api_url_image, files=files)

        if response.status_code == 200:
            result = response.json()

            prediction = result.get("img_class")[0]

            if prediction in unique_labels:
                if prediction in label_messages:
                    message = label_messages[prediction]
                    st.image(img_file_buffer, use_column_width=True)  # Display the image

                    if prediction == 'not_humanitarian':
                        st.markdown(
                            f"<p style='font-size: 18px; color: blue;'>{message}</p>",
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"<p style='font-size: 18px; color: red; font-weight: bold;'>🚨{message}🚨</p>",
                            unsafe_allow_html=True
                        )
                else:
                    image_prediction_output.error("No message defined for this prediction label.")
            else:
                image_prediction_output.error("Invalid prediction value received from the API.")
        else:
            image_prediction_output.error("Image classification prediction failed. Please try again later.")



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

label_messages = {
    'other_relevant_information': "Relevant information",
    'not_humanitarian': "Not related to humanitarian aid",
    'rescue_volunteering_or_donation_effort': "Information about rescue, volunteering, or donation efforts",
    'infrastructure_and_utility_damage': "Infrastructure and utility damage",
    'injured_or_dead_people': "Injured or dead individuals",
    'affected_individuals': "Affected individuals",
    'vehicle_damage': "Vehicle damage",
    'missing_or_found_people': "Missing or found people"
}

st.markdown("<h1><b>Crisis Helper Real-Time 🌐</b></h1>", unsafe_allow_html=True)

# Adding space after the title
st.markdown("<br>", unsafe_allow_html=True)

# Load a DataFrame with a "tweet_text" column
df = pd.read_csv('/media/hamzah/Ubud/code/00_Data_Science/.crisis_helper/mlops/data/raw/df_test_binary.csv')

# Limit the simulation to the first 10 rows
df = df.sample(n=5)

# Create two columns for button alignment
col1, col2 = st.columns(2)

# Create a button to start the text simulation
if col1.button("Start Text Feed"):
    for index, row in df.iterrows():
        st.subheader("Tweet:")
        st.write(row['tweet_text'])  # Display the tweet text

        params = dict(tweet=row['tweet_text'])
        api_url = 'https://crisishelper-qlahvylymq-ew.a.run.app/predict_multi'

        try:
            # Send a GET request to the API
            response = requests.get(api_url, params=params)

            print("API Request URL:", response.url)  # Debug print to see the API request URL

            # Check if the API request was successful
            if response.status_code == 200:
                result = response.json()
                prediction = result.get("tweet_class")[0]

                if 'tweet_class' in result:
                    tweet_class = result['tweet_class'][0]
                    print("Classification Result:", tweet_class)  # Debug print to see the classification result

                    if prediction in unique_labels:
                        if prediction in label_messages:
                            message = label_messages[prediction]

                            # Introduce a 2-second delay before displaying the prediction
                            time.sleep(2)

                            if prediction == 'not_humanitarian':
                                st.markdown(
                                    f"<p style='font-size: 18px; color: blue;font-weight: bold;'>{message}</p>",
                                    unsafe_allow_html=True)
                            else:
                                st.markdown(
                                    f"<p style='font-size: 18px; color: red; font-weight: bold;'>🚨{message}🚨</p>",
                                    unsafe_allow_html=True)
                        else:
                            st.error("No message defined for this prediction label.")
                    else:
                        st.error("Invalid prediction value received from the API.")
                else:
                    st.error("Text classification prediction failed. Please try again later.")
            else:
                st.error("Prediction failed for this tweet. Please try again later.")
        except Exception as e:
            st.error(f"Error: {e}")

        st.markdown("---")

# Add a stop button to end the text simulation
if col1.button("Stop Text Feed"):
    st.warning("Feed stopped.")


# Specify the directory where the images are located
image_directory = '/media/hamzah/Ubud/code/00_Data_Science/Multimodal_Crisis_Project_Website/data/images'

# Get a list of image file paths in the directory
image_files = [os.path.join(image_directory, filename) for filename in os.listdir(image_directory) if filename.endswith(('.jpg', '.png', '.jpeg'))]

# Create a button to start the image simulation
if col2.button("Start Image Feed"):
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

    label_messages = {
        'other_relevant_information': "Relevant information",
        'not_humanitarian': "Not related to humanitarian aid",
        'rescue_volunteering_or_donation_effort': "Information about rescue, volunteering, or donation efforts",
        'infrastructure_and_utility_damage': "Infrastructure and utility damage",
        'injured_or_dead_people': "Injured or dead individuals",
        'affected_individuals': "Affected individuals",
        'vehicle_damage': "Vehicle damage",
        'missing_or_found_people': "Missing or found people"
    }

    for image_file in image_files:
        st.image(image_file, width=500)  # Display the image with a smaller width

        # Prepare the image for API upload
        with open(image_file, 'rb') as f:
            img_file_buffer = f.read()

        api_url_image = 'https://crisishelper-qlahvylymq-ew.a.run.app/upload_image'

        try:
            # Send a POST request to the API
            response = requests.post(api_url_image, files={'img': img_file_buffer})

            # Check if the API request was successful
            if response.status_code == 200:
                result = response.json()

                prediction = result.get("img_class")[0]

                if prediction in unique_labels:
                    if prediction in label_messages:
                        message = label_messages[prediction]

                        # Introduce a 2-second delay before displaying the prediction
                        time.sleep(2)

                        if prediction == 'not_humanitarian':
                            st.markdown(
                                f"<p style='font-size: 18px; color: blue;'>{message}</p>",
                                unsafe_allow_html=True
                            )
                        else:
                            st.markdown(
                                f"<p style='font-size: 18px; color: red; font-weight: bold;'>🚨{message}🚨</p>",
                                unsafe_allow_html=True
                            )
                    else:
                        st.error("No message defined for this prediction label.")
                else:
                    st.error("Invalid prediction value received from the API.")
            else:
                st.error("Image classification prediction failed. Please try again later.")
        except Exception as e:
            st.error(f"Error: {e}")

        st.markdown("---")

# Add a stop button to end the image simulation
if col2.button("Stop Image Feed"):
    st.warning("Feed stopped.")
