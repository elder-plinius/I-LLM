import streamlit as st
from dalle import DalleImageGenerator  # Ensure this matches the filename or import path of the class
from agents import DoPAgent
from gemini_chat import GeminiChat  # This should be your Gemini client setup

# Initialize the DalleImageGenerator and DoPAgent with the Gemini client
gemini_client = GeminiChat()  # Make sure to initialize your Gemini client correctly
dalle_generator = DalleImageGenerator()
dop_agent = DoPAgent(gemini_client)

def generate_images_for_screenplay(screenplay_text, style_guide):
    """
    Parses a screenplay text into visual moments, and generates images for those moments using DALL·E,
    with each image generated according to a consistent style guide.
    
    Args:
        screenplay_text (str): Text of the screenplay.
        style_guide (str): Description of the visual style to apply to all images.
    """
    st.write("Generating DALL·E prompts from screenplay...")
    dalle_prompts = dop_agent.generate_dalle_prompts(screenplay_text)
    
    if not dalle_prompts or len(dalle_prompts) == 0:
        st.write("No DALL·E prompts generated. Exiting...")
        return
    else:
        st.write(f"Generated {len(dalle_prompts)} DALL·E prompts.")

    for i, prompt in enumerate(dalle_prompts):
        # Append the style guide to each prompt before generating the image
        styled_prompt = f"{prompt}. {style_guide}"
        st.write(f"Generating image for styled prompt {i+1}: {styled_prompt}")
        image_url = dalle_generator.generate_image(styled_prompt)
        
        if image_url:
            st.image(image_url, caption=f"Image {i+1}", use_column_width=True)
        else:
            st.write(f"Failed to generate image for styled prompt {i+1}.")

# Streamlit app
st.title("Screenplay Image Generator")

# Define your style guide here
style_guide = st.text_area("Enter the style guide for the images:", 
                           "Visual style: Shawshank Redemption, cinematic photorealism")

# File uploader allows user to upload a screenplay file
uploaded_file = st.file_uploader("Choose a screenplay file", type=['txt'])
if uploaded_file is not None:
    screenplay_text = uploaded_file.getvalue().decode("utf-8")
    if st.button('Generate Images'):
        generate_images_for_screenplay(screenplay_text, style_guide)
