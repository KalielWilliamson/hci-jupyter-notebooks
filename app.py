import os
import time

import boto3
import pandas as pd
import streamlit as st
from botocore.client import Config
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.resource('s3',
                    endpoint_url='https://' + os.environ.get('AH_S3_OBJECT_STORAGE_STACKHERO_BLACK_HOST'),
                    aws_access_key_id=os.environ.get('AH_S3_OBJECT_STORAGE_STACKHERO_BLACK_ROOT_ACCESS_KEY'),
                    aws_secret_access_key=os.environ.get('AH_S3_OBJECT_STORAGE_STACKHERO_BLACK_ROOT_SECRET_KEY'),
                    config=Config(signature_version='s3v4'),
                    region_name='us-east-1')


def read_svg(file_name, width=50, height=50, margin="10px", color="black"):
    with open(os.path.join(file_name), 'r') as file:
        svg_content = file.read()
    # Add inline styles to the SVG tag
    svg_content = svg_content.replace('<svg', f'<svg width="{width}" height="{height}" style="fill:{color};"')
    # Wrap the SVG content in a span with margin
    wrapped_svg = f'<span style="display:inline-block; margin:{margin};">{svg_content}</span>'
    return wrapped_svg


# Dictionary of icons with corresponding SVG file names
icons = {
    "Care Plan": "icons/bed-pulse-solid.svg",
    "Schedule": "icons/calendar-solid.svg",
    "Alarm": "icons/clock-solid.svg",
    "Discharge": "icons/house-solid.svg",
    "Notes": "icons/notes-medical-solid.svg",
    "Prescription Orders": "icons/prescription-bottle-medical-solid.svg",
    "Diagnosis": "icons/stethoscope-solid.svg",
    "Timeline": "icons/timeline-solid.svg",
    "Vitals": "icons/vials-solid.svg",
    "Imaging Orders": "icons/x-ray-solid.svg",
}

# Define the content for each card
card_contents = [
    {"title": "J. Doe",
     "icons": [("Timeline", "red"), ("Notes", "orange"), ("Imaging Orders", "green"), ("Diagnosis", "green"), ("Discharge", "orange")],
     "background_color": "#e0f7fa"},
    {"title": "R. Rowley",
     "icons": [("Alarm", "orange"), ("Care Plan", "red")],
     "background_color": "#ffebee"},
    {"title": "A. Collier",
     "icons": [("Prescription Orders", "red"), ("Vitals", "orange"), ("Care Plan", "green")],
     "background_color": "#f3e5f5"},
    {"title": "D. Jones",
     "icons": [("Imaging Orders", "green"), ("Care Plan", "orange"), ("Schedule", "red")],
     "background_color": "#e8f5e9"},
    {"title": "C. Chen",
     "icons": [("Diagnosis", "red"), ("Notes", "green"), ("Alarm", "orange")],
     "background_color": "#fff3e0"},
    {"title": "D. Molak",
     "icons": [("Care Plan", "red"),
               ("Prescription Orders", "green")],
     "background_color": "#e0f2f1"},
    {"title": "E. Lowrey",
     "icons": [("Vitals", "green"), ("Care Plan", "orange"), ("Imaging Orders", "red")],
     "background_color": "#ede7f6"},
    {"title": "V. Taylor",
     "icons": [("Care Plan", "red"), ("Schedule", "green"), ("Timeline", "orange")],
     "background_color": "#fbe9e7"},
    {"title": "S. Pachuke",
     "icons": [("Diagnosis", "orange"), ("Notes", "red"), ("Alarm", "green")],
     "background_color": "#fffde7"},
    {"title": "I. Sutsky",
     "icons": [("Care Plan", "orange"),
               ("Prescription Orders", "red")],
     "background_color": "#f1f8e9"},
    {"title": "Y. Lecuun",
     "icons": [("Vitals", "orange"), ("Care Plan", "green"), ("Imaging Orders", "red")],
     "background_color": "#e0f7fa"},
    {"title": "J. Bengio",
     "icons": [("Care Plan", "red"), ("Schedule", "orange"), ("Timeline", "green")],
     "background_color": "#fff3e0"},
]

st.session_state['card_state'] = card_contents.copy()

patient_info = {
    "J. Doe": {
        "age": 35,
        "fullname": "John Doe",
        "sex": "male",
    },
    "R. Rowley": {
        "age": 45,
        "fullname": "Rachel Rowley",
        "sex": "female"
    },
    "A. Collier": {
        "age": 25,
        "fullname": "Alice Collier",
        "sex": "female"
    },
    "D. Jones": {
        "age": 55,
        "fullname": "David Jones",
        "sex": "male"
    },
    "C. Chen": {
        "age": 65,
        "fullname": "Catherine Chen",
        "sex": "female"
    },
    "D. Molak": {
        "age": 75,
        "fullname": "David Molak",
        "sex": "male"
    },
    "E. Lowrey": {
        "age": 85,
        "fullname": "Emily Lowrey",
        "sex": "female"
    },
    "V. Taylor": {
        "age": 95,
        "fullname": "Victoria Taylor",
        "sex": "female"
    },
    "S. Pachuke": {
        "age": 105,
        "fullname": "Samantha Pachuke",
        "sex": "female"
    },
    "I. Sutsky": {
        "age": 115,
        "fullname": "Ivan Sutsky",
        "sex": "male"
    },
    "Y. Lecuun": {
        "age": 125,
        "fullname": "Yvonne Lecuun",
        "sex": "female"
    },
    "J. Bengio": {
        "age": 135,
        "fullname": "Joshua Bengio",
        "sex": "male"
    }
}

# Initialize session state
if 'expanded_card' not in st.session_state:
    st.session_state['expanded_card'] = None


# Function to create a card with icons
def create_card(title, icon_keys, card_index, background_color):
    is_expanded = st.session_state['expanded_card'] == card_index

    icon_html = ''.join(
        [read_svg(icons[icon[0]], width=50, height=50, margin="10px", color=icon[1]) for icon in icon_keys])

    with st.container(border=True):
        button_clicked = st.button(f"{title} {'▼' if is_expanded else '▲'}", key=card_index)
        if button_clicked:
            st.session_state['expanded_card'] = card_index if not is_expanded else None

        if st.session_state['expanded_card'] == card_index:
            info = patient_info[title]
            st.write(f"Name: {info['fullname']} | Age: {info['age']} | Sex: {info['sex']}")

            num_cols = len(icon_keys)
            columns = st.columns(num_cols)
            buttons = {}

            for i in range(num_cols):
                with columns[i]:
                    key = st.session_state.card_state[card_index]["icons"][i][0]
                    btn = st.button(key)
                    buttons.update({key: btn})

        st.markdown(
            f"""
            <div style="padding: 20px; border-radius: 10px; background-color: {background_color}; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom: 20px; height: 100px; color: black;">
                <p style="font-size: 20px; color: black">{icon_html}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.session_state['expanded_card'] == card_index:
            def send_to_back(card_index, title):
                patient_state = st.session_state.card_state[card_index]
                icon_index = [i for i, j in enumerate(patient_state['icons']) if j[0] == title][0]
                item = patient_state['icons'].pop(icon_index)
                item = (item[0], "green")
                patient_state['icons'].append(item)
                st.session_state.card_state[card_index] = patient_state

            if buttons.get("Timeline"):
                st.subheader("Patient Timeline")
                send_to_back(card_index, "Timeline")

                with open('images/timeline.png', 'rb') as file:
                    timeline_image = file.read()

                st.image(timeline_image, use_column_width=True)
                st.write("""
                 The patient was admitted to the hospital on 2024-07-05 at 10:00 AM.
                 The patient was seen by a nurse at 11:00 AM.
                 """)

            if buttons.get("Notes"):
                send_to_back(card_index, "Notes")
                st.subheader("Patient Notes")
                st.write("""
                 The patient has a history of heart disease and is allergic to penicillin.
                 """)
                st.text_input("Add a note")

            if buttons.get("Imaging Orders"):
                send_to_back(card_index, "Imaging Orders")
                st.subheader("Imaging Orders")
                st.image('images/catscan.png', use_column_width=True)
                st.multiselect("Select imaging orders", ["CT Scan", "MRI", "X-Ray"])
                st.text_input("Notes")

            if buttons.get("Diagnosis"):
                send_to_back(card_index, "Diagnosis")
                st.subheader("Diagnosis")
                st.text_area("Notes",
                             "The patient, a 45-year-old male, presents with a subdural hematoma following a high-impact car accident. Initial assessment revealed a significant head injury with loss of consciousness at the scene. Upon arrival at the emergency department, the patient exhibited altered mental status, severe headache, and signs of increased intracranial pressure, including nausea and vomiting. A CT scan confirmed the presence of a subdural hematoma with midline shift, indicating substantial bleeding between the dura mater and the brain. The patient was promptly stabilized and prepared for urgent surgical intervention to evacuate the hematoma and alleviate pressure on the brain. Post-operatively, the patient will require close monitoring in the intensive care unit, with frequent neurological assessments and supportive care to manage potential complications such as seizures, brain swelling, and infection. Long-term prognosis will depend on the extent of the brain injury and the patient's response to treatment.")

                diagnosis_icon_html = ''.join(
                    [
                        read_svg(icon, width=50, height=50, margin="10px", color="black")
                        for icon in ["icons/droplet-solid.svg", "icons/brain-solid.svg"]
                    ]
                )

                st.markdown(f"""
                    <div style="padding: 20px; border-radius: 10px; background-color: #fff3e0; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom: 20px; height: 100px; color: black;">
                        <p style="font-size: 20px; color: black">{diagnosis_icon_html}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            if buttons.get("Discharge"):
                send_to_back(card_index, "Discharge")
                st.subheader("Discharge")
                st.write(f"""
                 The patient was discharged on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}.
                 """)


# Create a 3x4 grid
rows = len(st.session_state['card_state'])

for card_index in range(rows):
    if card_index < len(st.session_state['card_state']):
        create_card(st.session_state['card_state'][card_index]["title"], st.session_state['card_state'][card_index]["icons"], card_index,
                    st.session_state['card_state'][card_index]["background_color"])

if __name__ == '__main__':
    os.system('streamlit run app.py --server.port=8501 --server.address=0.0.0.0')
