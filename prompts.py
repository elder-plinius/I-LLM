# prompts.py

# Prompt for developing a detailed movie concept from an initial idea
IDEA_INTAKE_PROMPT = """
Develop an EXTREMELY creative and highly detailed movie concept including genre, themes, plot points, and full character sketches based on the following idea: {idea}
"""

# Prompt for generating a style guide, now potentially including visual aesthetic derived from an uploaded image
STYLE_GUIDE_PROMPT = """
Generate a style guide that captures the desired artistic and writing styles for the movie concept: {concept}. This guide should include considerations for tone, pacing, visual style, and thematic elements. If applicable, incorporate the visual aesthetic described by the image analysis: {visual_description}
"""

# Prompt for generating a narrative outline, specifying key scenes and major plot points
NARRATIVE_OUTLINE_PROMPT = """
Generate a narrative outline based on the concept and style guide. The outline should detail key scenes, major plot points, and character arcs that will guide the screenplay drafting process. Ensure the outline supports a coherent and engaging story arc: {concept} {style_guide}
"""

# Updated prompt for drafting scenes, taking into account the narrative outline
SCREENPLAY_DRAFTING_PROMPT = """
You are a professional screenwriter. Given the screenplay context and the narrative outline below, generate the next scene that logically follows. Ensure the scene maintains the established tone, style, and direction of the narrative. Include character interactions, dialogue, and scene descriptions that advance the plot towards the next key moment.

Screenplay Context:
{screenplay_context}

Narrative Outline:
{narrative_outline}

Generate the next scene, maintaining industry-standard best-practice formatting for screenwriting:
"""


# Dialogue Parsing Prompt
DIALOGUE_PARSING_PROMPT = """
Parse the following screenplay text to extract dialogue by characters. For each piece of dialogue, identify the character and the dialogue they speak. Format the output as ONLY a JSON list of character-dialogue pairs, where each pair contains the character's name and ALL of their dialogue in order.
"""

# prompts.py

VOICE_MATCHING_PROMPT = """
Given the following character sketches and our library of voice attributes, match each character to the most suitable "voice ID" number from the voice library based on gender, age, and/or traits. If there's no perfect match for a character, just use your best judgement to assign one. Provide the output as ONLY a cleaned JSON list with pairs of character names and their matched voice IDs.

Idea Output:
{idea_output}

Voice Library:
{voice_library}

Output the matches as a list of JSON pairs with character names as keys and voice IDs as values:
"""

SCENE_PLANNING_PROMPT = """
As the world's leading screenwriter, your task is to develop detailed plans for a series of scenes based on the comprehensive narrative outline provided. Each scene plan should encapsulate the scene's number, a vivid setting, the primary actions, emotional dynamics, significant character developments, and a succinct goal that propels the narrative forward. These plans will serve as the foundation for drafting the screenplay, ensuring each scene contributes meaningfully to the overarching story.

Narrative Context:
{previous_scenes_context}

Upcoming Scene Number: {scene_number}
Narrative Outline for This Scene:
{scene_specific_outline}

Craft a detailed plan for this scene, highlighting:
- The scene's setting and its importance
- Key actions and their impact on the plot
- Emotional beats and their role in character development
- How this scene advances the story or deepens character arcs
- The scene's goal in relation to the narrative's progression

Present your scene plan in a structured format that seamlessly integrates with the screenplay drafting phase, ensuring clarity and depth in the narrative's unfolding:
"""

# Prompt for the Director of Photography to create detailed visual scene descriptions for image generation
DIRECTOR_OF_PHOTOGRAPHY_PROMPT1 = """
As the Director of Photography, your task is to visualize and describe each scene in vivid detail, suitable for creating compelling imagery that aligns with the movie's style guide and narrative outline. For each scene provided, craft a descriptive prompt that encompasses the scene's setting, mood, key actions, and emotional tone. These descriptions will serve as the basis for generating visual representations of each scene.

Scene Planning Input:
{scene_planning_input}

Generate a detailed visual scene description that includes:
- The primary setting and its visual elements
- The mood and atmosphere, including lighting and color palette suggestions
- Key characters and their actions within the scene
- Any significant objects or symbols present in the scene
- Camera angles or shots that could enhance the scene's impact

Your description should provide a comprehensive guide for generating images that capture the essence of each scene, supporting the storytelling with powerful visual imagery:
"""

# prompts.py

# Update the prompt to focus on DALL·E best practices for prompt writing
DIRECTOR_OF_PHOTOGRAPHY_PROMPT = """
Analyze the screenplay provided to identify key visual scenes. For each scene, create a detailed, creative prompt suitable for generating an image with DALL·E. Focus on vividly and comprehensively describing the setting, characters, emotions, and any significant visual elements as if to a person that is blind and has never seen the movie before. Each prompt should be designed to produce a compelling and visually rich image that captures the essence of the scene.

Screenplay Text:
{screenplay}

Format the output as ONLY a JSON list of Dalle prompts, where each prompt is structured to highlight the key elements essential for image generation. Ensure the prompts are detailed and creative, adhering to best practices for Stable Diffusion DALL·E image generation prompt engineering.
"""

