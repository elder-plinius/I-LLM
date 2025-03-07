# Import necessary libraries
import streamlit as st
from agents import MovieConceptAgent, StyleGuideAgent, NarrativeOutlineAgent, ScreenplayDraftingAgent, VoiceMatchingAgent, DialogueParsingAgent
from openai_vision import OpenAIVision
from gemini_chat import GeminiChat
from utils import generate_speech
import os
from tempfile import NamedTemporaryFile
from io import BytesIO

# Initialize AI and vision clients
ai_client = GeminiChat()
vision_client = OpenAIVision()
xi_api_key = os.getenv("ELEVENLABS_API_KEY")  # Ensure this is set in your environment variables

# Initialize AI agents
concept_agent = MovieConceptAgent(ai_client)
style_guide_agent = StyleGuideAgent(ai_client)
outline_agent = NarrativeOutlineAgent(ai_client)
screenplay_agent = ScreenplayDraftingAgent(ai_client)
voice_matching_agent = VoiceMatchingAgent(ai_client)
dialogue_agent = DialogueParsingAgent(ai_client)

def save_uploaded_file(uploaded_file):
    """Saves the uploaded file to a temporary directory and returns the file path."""
    try:
        with NamedTemporaryFile(delete=False, suffix="." + uploaded_file.name.split('.')[-1], dir="temp") as tmp:
            tmp.write(uploaded_file.getvalue())
            return tmp.name
    except Exception as e:
        st.error(f"Error saving uploaded file: {e}")
        return None

def app_main():
    st.title("AI Movie Maker")

    # User inputs for movie concept or image upload
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
                os.remove(temp_image_path)  # Cleanup

    generate_button = st.button("Generate Movie Elements")
    if generate_button:
        with st.spinner('Generating movie elements...'):
            concept = concept_agent.generate_concept(user_idea) if user_idea else ""
            style_guide = style_guide_agent.create_style_guide(concept, visual_style_description)
            narrative_outline = outline_agent.generate_outline(concept, style_guide, number_of_scenes)
            screenplay_context = concept + " " + visual_style_description
            screenplay = screenplay_agent.draft_screenplay(screenplay_context, narrative_outline, number_of_scenes)

        if concept:
            st.write("Movie Concept:", concept)
        if style_guide:
            st.write("Style Guide:", style_guide)
        if narrative_outline:
            st.write("Narrative Outline:", narrative_outline)
        if screenplay:
            st.text_area("Screenplay Draft:", screenplay, height=500)

        screenplay_filename = "screenplay.txt"
        with open(screenplay_filename, "w", encoding='ISO-8859-1') as file:
            file.write(screenplay)
        with open(screenplay_filename, "rb") as file:
            st.download_button(label="Download Screenplay", data=file, file_name=screenplay_filename, mime='text/plain')
        dialogues_json = dialogue_agent.parse_screenplay(screenplay)
        matched_voices = voice_matching_agent.match_voices(screenplay)

        character_dialogues = {}
        for entry in dialogues_json:
            character = entry["character"]
            if character not in character_dialogues:
                character_dialogues[character] = []
            character_dialogues[character].extend(entry["dialogue"])

        with st.spinner('Matching voices and generating audio...'):
            for character, dialogues in character_dialogues.items():
                voice_id = matched_voices.get(character, None)
                if voice_id:
                    full_dialogue = " ".join(dialogues)
                    temp_file_path = generate_speech(full_dialogue, voice_id, xi_api_key, character)
                    if temp_file_path:
                        try:
                            with open(temp_file_path, "rb") as audio_file:
                                audio_content = audio_file.read()
                                audio_bytes_io = BytesIO(audio_content)
                                audio_bytes_io.seek(0)  # Reset pointer to the start
                                st.audio(audio_bytes_io, format='audio/mp3')
                                audio_bytes_io.seek(0)  # Reset pointer again for download button
                                st.download_button(label=f"Download {character}'s Voice",
                                                data=audio_bytes_io,
                                                file_name=f"{character}_voice.mp3",
                                                mime='audio/mp3')
                        finally:
                            os.remove(temp_file_path)  # Ensure cleanup

        # Cleanup screenplay file
        if os.path.exists(screenplay_filename):
            os.remove(screenplay_filename)

if __name__ == "__main__":
    app_main()
