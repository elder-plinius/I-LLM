from prompts import (
    IDEA_INTAKE_PROMPT, 
    STYLE_GUIDE_PROMPT, 
    NARRATIVE_OUTLINE_PROMPT, 
    SCREENPLAY_DRAFTING_PROMPT,
    DIALOGUE_PARSING_PROMPT,
    VOICE_MATCHING_PROMPT,
    SCENE_PLANNING_PROMPT,
    DIRECTOR_OF_PHOTOGRAPHY_PROMPT
)
import json
import requests
from elevenlabs_library import elevenlabs_voice_library as voice_library

class BaseAgent:
    def __init__(self, ai_client):
        self.ai_client = ai_client

class MovieConceptAgent(BaseAgent):
    def generate_concept(self, idea):
        prompt = IDEA_INTAKE_PROMPT.format(idea=idea)
        return self.ai_client.send_message(prompt)

class StyleGuideAgent(BaseAgent):
    def create_style_guide(self, concept, visual_description=""):
        prompt = STYLE_GUIDE_PROMPT.format(concept=concept, visual_description=visual_description)
        return self.ai_client.send_message(prompt)

class NarrativeOutlineAgent(BaseAgent):
    def generate_outline(self, concept, style_guide, desired_length_pages):
        # Adjusting the prompt to include desired movie length for better outline planning
        prompt = NARRATIVE_OUTLINE_PROMPT.format(concept=concept, style_guide=style_guide, desired_length_pages=desired_length_pages)
        return self.ai_client.send_message(prompt)

class ScreenplayDraftingAgent(BaseAgent):
    def draft_screenplay(self, screenplay_context, narrative_outline, number_of_scenes=20):
        screenplay = ""
        for scene_number in range(1, number_of_scenes + 1):
            prompt = SCREENPLAY_DRAFTING_PROMPT.format(screenplay_context=screenplay_context, narrative_outline=narrative_outline)
            # Corrected the call to use `self.ai_client` instead of `self.gemini_chat`
            new_scene = self.ai_client.send_message(prompt, temp=0.7)
            screenplay += f"\n\nScene {scene_number}:\n{new_scene}"
            screenplay_context += f" {new_scene}"  # Update context with the new scene
        return screenplay


class DialogueParsingAgent:
    def __init__(self, ai_client):
        self.ai_client = ai_client

    def clean_and_parse_response(self, response):
        # Remove Markdown formatting if present
        cleaned_response = response.replace("```json", "").replace("```", "").strip()
        try:
            response_json = json.loads(cleaned_response)
            print("Parsed AI response successfully.")
            return response_json
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from AI response: {e}. Cleaned response was: '{cleaned_response}'")
            return []

    def parse_screenplay(self, screenplay_text):
        prompt = DIALOGUE_PARSING_PROMPT + screenplay_text
        response = self.ai_client.send_message(prompt)
        
        # Use the clean_and_parse_response method to handle the raw response
        return self.clean_and_parse_response(response)
    
class VoiceMatchingAgent(BaseAgent):
    def match_voices(self, idea_output):
        """
        Matches characters from the screenplay to voice IDs from the ElevenLabs voice library
        using the entire output from the idea generation agent and a special prompt.

        :param idea_output: A string containing the full output from the idea generation agent.
        :return: A dictionary with character names as keys and matched voice IDs as values.
        """
        # Prepare the prompt with the movie concept and voice library details
        prompt = VOICE_MATCHING_PROMPT.format(idea_output=idea_output, voice_library=json.dumps(voice_library, indent=2))
        
        # Send the prompt to the Gemini agent and parse the response
        response = self.ai_client.send_message(prompt)
        try:
            # Clean the response to remove Markdown code block syntax
            cleaned_response = response.replace("```json", "").replace("```", "").strip()
            
            # Parse the cleaned response as JSON
            matched_voices = json.loads(cleaned_response)
            print("Matched voices JSON:", json.dumps(matched_voices, indent=4))  # Pretty print the JSON for verification
            return matched_voices
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON from response: {e}")
            return {}

class ScenePlanningAgent(BaseAgent):
    def plan_scenes(self, narrative_outline):
        prompt = SCENE_PLANNING_PROMPT.format(narrative_outline=narrative_outline)
        response = self.ai_client.send_message(prompt)
        return json.loads(response)

class DirectorOfPhotographyAgent(BaseAgent):
    def plan_visuals(self, screenplay, scene_plans):
        screenplay_and_scene_plans = {"screenplay": screenplay, "scene_plans": scene_plans}
        prompt = DIRECTOR_OF_PHOTOGRAPHY_PROMPT.format(screenplay_and_scene_plans=json.dumps(screenplay_and_scene_plans, indent=2))
        response = self.ai_client.send_message(prompt)
        return json.loads(response)
    

import json
from prompts import DIRECTOR_OF_PHOTOGRAPHY_PROMPT  # Import the specific prompt

class DoPAgent:
    def __init__(self, ai_client):
        self.ai_client = ai_client

    def generate_dalle_prompts(self, screenplay_text):
        """
        Generates prompts for DALL·E based on a screenplay text.

        Args:
            screenplay_text (str): The screenplay text from which to generate image prompts.

        Returns:
            list: A list of prompts for image generation.
        """
        # Use the prompt from prompts.py, formatting it with the screenplay text
        prompt = DIRECTOR_OF_PHOTOGRAPHY_PROMPT.format(screenplay=screenplay_text)
        response = self.ai_client.send_message(prompt)
        
        # Clean and parse the AI's response
        return self.clean_and_parse_response(response)

    def clean_and_parse_response(self, response):
        """
        Cleans the response from the AI model and attempts to parse it as JSON.
        
        Args:
            response (str): The raw response string from the AI model.
            
        Returns:
            list or dict: Parsed JSON object from the response.
        """
        # Remove potential Markdown formatting that might interfere with JSON parsing
        cleaned_response = response.replace("```json", "").replace("```", "").strip()
        
        try:
            # Attempt to parse the cleaned response as JSON
            response_json = json.loads(cleaned_response)
            print("Parsed AI response successfully.")
            return response_json
        except json.JSONDecodeError as e:
            # If parsing fails, log the error and the cleaned response for debugging
            print(f"Error decoding JSON from AI response: {e}. Cleaned response was: '{cleaned_response}'")
            # Depending on your needs, you might return an empty list, dictionary, or None
            return []

    # Add any additional methods your DoPAgent requires
