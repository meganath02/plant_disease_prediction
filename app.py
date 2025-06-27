

import streamlit as st
from utils import predict, translate_text, get_disease_resource

# Set Streamlit page configuration
st.set_page_config(page_title="Plant Disease Detector", layout="centered")


lang = st.sidebar.selectbox(
    "🌐 Select Language", 
    options=[
        ("English", "en"),
        ("Hindi", "hi"),
        ("Telugu", "te"),
        ("Tamil", "ta"),
        ("Kannada", "kn"),
        ("Malayalam", "ml")
    ],
    format_func=lambda x: x[0]
)[1]


# Translate all necessary UI strings
title = translate_text("Plant Disease Classifier", lang)
upload_prompt = translate_text("Upload a leaf image, and the model will predict the plant disease.", lang)
button_label = translate_text("Predict", lang)
analyzing_text = translate_text("Analyzing image...", lang)
predicted_label = translate_text("Predicted Disease:", lang)
confidence_label = translate_text("Confidence", lang)
uploaded_caption = translate_text("Uploaded Image", lang)
choose_text = translate_text("Choose an image...", lang)

# UI layout
st.title(title)
st.markdown(upload_prompt)

# Image uploader with unique key
uploaded_file = st.file_uploader(choose_text, type=["jpg", "jpeg", "png"], key="image_uploader")

if uploaded_file is not None:
    st.image(uploaded_file, caption=uploaded_caption, use_container_width=True)
    if st.button(button_label):
        with st.spinner(analyzing_text):
            class_name, confidence = predict(uploaded_file)
            resource = get_disease_resource(class_name)

            st.markdown("### 📄 Disease Description")
            st.write(translate_text(resource["description"], lang))

            if resource["video"]:
                st.markdown("### 🎥 Watch Treatment/Info Video")
                st.video(resource["video"])

            class_name_trans = translate_text(class_name.replace("___", " ").replace("_", " "), lang)
            st.success(f"{predicted_label} **{class_name_trans}**")
            st.info(f"{confidence_label}: {confidence:.2f}%")
