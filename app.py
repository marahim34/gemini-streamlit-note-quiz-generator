import streamlit as st
from api_calling import note_generator, audio_transcription, quiz_generator
from PIL import Image


st.title("**Note Summary and Quiz Generator**")
st.markdown("Upload up to 3 images to generate Note Summary and Quizes")

st.divider()

with st.sidebar:
    st.header("Controls")
    images = st.file_uploader(
        "Choose up to 3 images", 
        accept_multiple_files=True, 
        type=["png", "jpg", "jpeg"]
    )

    # Display uploaded images
    if images:
        if len(images) > 3:
            st.error("Please upload a maximum of 3 images.")
            images = images[:3]  # Keep only the first 3 images
        else:
            col = st.columns(len(images))

            st.subheader("Uploaded Images")

            for i, img in enumerate(images):
                with col[i]:
                    st.image(img, caption=f"Image {i+1}")          

    # Difficulty level for quiz generation
    selected_options = st.selectbox(
        "Select Quiz Difficulty Level",
        options=("Easy", "Medium", "Hard"),
        index=None,
        key="difficulty"
    )

    if selected_options:
        st.markdown(f"Selected Difficulty Level: **{selected_options}**")

    # Button to trigger quiz generation
    pressed = st.button("Generate Note Summary and Quiz", type="primary")

# Moved this OUTSIDE the sidebar but still accessible
# Convert images to PIL only when needed
if pressed:
    if not images:
        st.error("Please upload at least one image to generate the quiz.")
    elif not selected_options:
        st.error("Please select a difficulty level to generate the quiz.")
    else:
        # Convert images to PIL format here
        pil_images = []
        for img in images:
            pil_img = Image.open(img)
            pil_images.append(pil_img)
        
        # note summary
        with st.container(border=True):
            st.subheader("Note Summary")

            # Generated notes
            with st.spinner("AI is generating notes for you..."):
                note_summary = note_generator(pil_images)
                st.markdown(note_summary)


        # Audio transcription
        with st.container(border=True):
            st.subheader("Audio Transcription")

            with st.spinner("AI is generating audio transcription for you..."):
                clean_text = note_summary.replace('\n', ' ')
                clean_text = clean_text.replace('#', ' ')
                clean_text = clean_text.replace('*', ' ')
                clean_text = clean_text.replace('`', ' ')
                clean_text = clean_text.replace('"', ' ')
                clean_text = clean_text.replace('-', ' ')
                audio = audio_transcription(clean_text)
                st.audio(audio, format='audio/mp3')


        # Quiz Generation
        with st.container(border=True):
            st.subheader(f"Quiz ({selected_options}) Difficulty")

            with st.spinner("AI is generating quiz for you..."):
                quiz = quiz_generator(pil_images, selected_options)
                st.markdown(quiz)