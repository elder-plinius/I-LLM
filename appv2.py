import streamlit as st
from agents import MovieConceptAgent, StyleGuideAgent, NarrativeOutlineAgent, ScreenplayDraftingAgent
from openai_vision import OpenAIVision
from gemini_chat import GeminiChat
import os
from tempfile import NamedTemporaryFile

# Initialize GeminiChat and OpenAIVision
ai_client = GeminiChat()
vision_client = OpenAIVision()

# Initialize agents
concept_agent = MovieConceptAgent(ai_client)
style_guide_agent = StyleGuideAgent(ai_client)
outline_agent = NarrativeOutlineAgent(ai_client)
screenplay_agent = ScreenplayDraftingAgent(ai_client)

def save_uploaded_file(uploaded_file):
    try:
        with NamedTemporaryFile(delete=False, suffix="."+uploaded_file.name.split('.')[-1], dir="temp") as tmp:
            tmp.write(uploaded_file.getvalue())
            return tmp.name  # Return the path to the saved file
    except Exception as e:
        st.error(f"Error saving uploaded file: {e}")
        return None

def app_main():
    st.title("AI Movie Maker")

    idea_input_method = st.radio("How would you like to input your movie concept?",
                                 ('Type an Idea', 'Upload Image'))
    
    if idea_input_method == "Type an Idea":
        user_idea = st.text_area("Type your movie concept here:")
        if user_idea and st.button("Generate Movie Elements"):
            with st.spinner('Generating concept...'):
                concept = concept_agent.generate_concept(user_idea)
                st.write("Movie Concept:", concept)
            # Style guide generation based on the text concept
            with st.spinner('Creating style guide...'):
                style_guide = style_guide_agent.generate_style_guide(concept)
                st.write("Style Guide:", style_guide)

            # Narrative outline generation
            with st.spinner('Drafting narrative outline...'):
                narrative_outline = outline_agent.generate_outline(concept)
                st.write("Narrative Outline:", narrative_outline)

            # Screenplay drafting
            with st.spinner('Drafting screenplay...'):
                screenplay = screenplay_agent.draft_screenplay(concept, narrative_outline)
                st.write("Screenplay Draft:", screenplay)

    elif idea_input_method == "Upload Image":
        uploaded_image = st.file_uploader("Upload an image for inspiration", type=['jpg', 'jpeg', 'png'])
        if uploaded_image is not None:
            with st.spinner('Analyzing image...'):
                temp_image_path = save_uploaded_file(uploaded_image)
                if temp_image_path:
                    visual_style = vision_client.analyze_image(temp_image_path)
                    os.remove(temp_image_path)  # Clean up the temporary file
                    st.write("Visual Style Analysis:", visual_style)

                    # Proceed with generating movie elements based on visual style
                    style_guide = style_guide_agent.generate_style_guide(visual_style)
                    st.write("Style Guide based on image:", style_guide)

                    # Assuming the user provides additional input for concept after image analysis
                    user_idea = st.text_area("Refine your movie concept based on the image analysis:")
                    if user_idea and st.button("Generate Movie Elements from Image"):
                        concept = concept_agent.generate_concept(user_idea)
                        st.write("Movie Concept:", concept)

                        narrative_outline = outline_agent.generate_outline(concept)
                        st.write("Narrative Outline:", narrative_outline)

                        screenplay = screenplay_agent.draft_screenplay(concept, narrative_outline)
                        st.write("Screenplay Draft:", screenplay)

if __name__ == "__main__":
    app_main()
