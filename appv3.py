import streamlit as st
from agents import MovieConceptAgent, StyleGuideAgent, NarrativeOutlineAgent, ScreenplayDraftingAgent
from openai_vision import OpenAIVision
from gemini_chat import GeminiChat
import os
from tempfile import NamedTemporaryFile

# Initialize AI client and vision client
ai_client = GeminiChat()
vision_client = OpenAIVision()

# Initialize agents
concept_agent = MovieConceptAgent(ai_client)
style_guide_agent = StyleGuideAgent(ai_client)
outline_agent = NarrativeOutlineAgent(ai_client)
screenplay_agent = ScreenplayDraftingAgent(ai_client)

def save_uploaded_file(uploaded_file):
    try:
        with NamedTemporaryFile(delete=False, suffix="." + uploaded_file.name.split('.')[-1], dir="temp") as tmp:
            tmp.write(uploaded_file.getvalue())
            return tmp.name  # Return the path to the saved file
    except Exception as e:
        st.error(f"Error saving uploaded file: {e}")
        return None

def app_main():
    st.title("AI Movie Maker")
    user_idea = st.text_area("Type your movie concept here (Optional if uploading an image):", "")
    uploaded_image = st.file_uploader("Upload an image for inspiration (Optional if typing an idea):", type=['jpg', 'jpeg', 'png'])
    number_of_scenes = st.number_input("Number of scenes (for screenplay generation):", min_value=1, max_value=100, value=10)

    visual_style_description = ""
    if uploaded_image is not None:
        with st.spinner('Analyzing image...'):
            temp_image_path = save_uploaded_file(uploaded_image)
            if temp_image_path:
                visual_style_description = vision_client.analyze_image(temp_image_path)
                st.write("Visual Style Analysis:", visual_style_description)
                os.remove(temp_image_path)  # Clean up the temporary file

    generate_button = st.button("Generate Movie Elements")
    if generate_button:
        if user_idea or visual_style_description:
            with st.spinner('Generating concept...'):
                concept = concept_agent.generate_concept(user_idea) if user_idea else ""
                if concept:
                    st.write("Movie Concept:", concept)

            with st.spinner('Creating style guide...'):
                style_guide = style_guide_agent.create_style_guide(concept, visual_style_description)
                st.write("Style Guide:", style_guide)

            with st.spinner('Drafting narrative outline...'):
                narrative_outline = outline_agent.generate_outline(concept, style_guide, number_of_scenes)
                st.write("Narrative Outline:", narrative_outline)

            with st.spinner('Drafting screenplay...'):
                screenplay_context = concept + " " + visual_style_description  # Combine for richer context
                screenplay = screenplay_agent.draft_screenplay(screenplay_context, narrative_outline, number_of_scenes)
                st.text_area("Screenplay Draft:", screenplay, height=300)

                # Convert screenplay to a downloadable file
                screenplay_filename = "screenplay.txt"
                with open(screenplay_filename, "w") as file:
                    file.write(screenplay)
                with open(screenplay_filename, "rb") as file:
                    st.download_button(label="Download Screenplay", data=file, file_name=screenplay_filename, mime='text/plain')
                os.remove(screenplay_filename)  # Clean up the screenplay file

if __name__ == "__main__":
    app_main()
