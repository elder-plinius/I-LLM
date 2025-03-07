import streamlit as st
from agents import MovieConceptAgent, StyleGuideAgent, NarrativeOutlineAgent, ScreenplayDraftingAgent, VoiceMatchingAgent, DialogueParsingAgent, ScenePlanningAgent, DirectorOfPhotographyAgent
from openai_vision import OpenAIVision
from gemini_chat import GeminiChat
from utils import generate_speech
import os
from tempfile import NamedTemporaryFile

# Initialize AI client and vision client
ai_client = GeminiChat()
vision_client = OpenAIVision()
xi_api_key = os.getenv("ELEVENLABS_API_KEY")  # Make sure your API key is correctly set up

# Initialize agents
concept_agent = MovieConceptAgent(ai_client)
style_guide_agent = StyleGuideAgent(ai_client)
outline_agent = NarrativeOutlineAgent(ai_client)
screenplay_agent = ScreenplayDraftingAgent(ai_client)
voice_matching_agent = VoiceMatchingAgent(ai_client)
dialogue_agent = DialogueParsingAgent(ai_client)
scene_planning_agent = ScenePlanningAgent(ai_client)
photography_agent = DirectorOfPhotographyAgent(ai_client)

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
                os.remove(temp_image_path)

    generate_button = st.button("Generate Movie Elements")
    if generate_button:
        if user_idea or visual_style_description:
            with st.spinner('Generating concept...'):
                concept = concept_agent.generate_concept(user_idea or visual_style_description)
                st.write("Movie Concept:", concept)

            with st.spinner('Creating style guide...'):
                style_guide = style_guide_agent.create_style_guide(concept, visual_style_description)
                st.write("Style Guide:", style_guide)

            with st.spinner('Drafting narrative outline...'):
                narrative_outline = outline_agent.generate_outline(concept, style_guide, number_of_scenes)
                st.write("Narrative Outline:", narrative_outline)

            # Scene Planning Integration
            with st.spinner('Planning scenes...'):
                scene_plans = scene_planning_agent.plan_scenes(narrative_outline)
                st.write("Scene Plans:", scene_plans)

            # Director of Photography Integration
            with st.spinner('Planning visuals...'):
                visuals_plan = photography_agent.plan_visuals(concept, scene_plans)
                st.write("Visuals Plan:", visuals_plan)

            with st.spinner('Drafting screenplay...'):
                screenplay_context = concept + " " + visual_style_description
                screenplay = screenplay_agent.draft_screenplay(screenplay_context, narrative_outline, scene_plans)
                st.text_area("Screenplay Draft:", screenplay, height=800)

                screenplay_filename = "screenplay.txt"
                with open(screenplay_filename, "w") as file:
                    file.write(screenplay)
                with open(screenplay_filename, "rb") as file:
                    st.download_button(label="Download Screenplay", data=file, file_name=screenplay_filename, mime='text/plain')

                dialogues_json = dialogue_agent.parse_screenplay(screenplay)

                with st.spinner('Matching voices and generating audio...'):
                    matched_voices = voice_matching_agent.match_voices(concept)
                    for dialogue_entry in dialogues_json:
                        character = dialogue_entry["character"]
                        voice_id = matched_voices.get(character, "default_voice_id_if_unmatched")
                        for line in dialogue_entry["dialogue"]:
                            temp_file_path = generate_speech(line, voice_id, xi_api_key, character)
                            if temp_file_path:
                                with open(temp_file_path, "rb") as audio_file:
                                    st.audio(audio_file.read(), format='audio/mp3')
                                    st.download_button(f"Download {character}'s Voice", data=audio_file.read(), file_name=f"{character}_voice.mp3")
                                os.remove(temp_file_path)

                os.remove(screenplay_filename)

if __name__ == "__main__":
    app_main()
