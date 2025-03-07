import os
import openai

# Assuming OPENAI_API_KEY is set in your environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY  # Set the OpenAI library to use your API key

class DalleImageGenerator:
    def __init__(self):
        self.model = "dall-e-3"  # Model name for DALL·E 3
        print("DalleImageGenerator initialized with model:", self.model)

    def generate_image(self, prompt, size="1024x1024", quality="standard", n=1):
        """
        Generates an image using OpenAI's DALL·E 3 based on the given prompt.

        Args:
            prompt (str): The textual description to generate the image from.
            size (str): The size of the generated image ("1024x1024", "1024x1792", or "1792x1024").
            quality (str): The quality of the generated image ("standard" or "hd").
            n (int): The number of images to generate (currently, DALL·E 3 supports generating 1 image at a time).

        Returns:
            str: The URL of the generated image, or None if the request fails.
        """
        try:
            print("Sending request to OpenAI API...")
            response = openai.generate(
                model=self.model,
                prompt=prompt,
                size=size,
                quality=quality,
                n=n
            )
            print("Response received from OpenAI API.")
            
            
            # Correctly parsing the image URL from the response
            if hasattr(response, 'data') and len(response.data) > 0:
        # Access the first 'Image' object in the 'data' list
                image_object = response.data[0]
                if hasattr(image_object, 'url'):
                    image_url = image_object.url
                    print(f"Generated Image URL: {image_url}")
                    return image_url
                else:
                    print("URL not found in the response object.")
                    return None
            else:
                print("No data found in response.")
                return None
        except Exception as e:
            print(f"Exception occurred while generating image: {e}")
            return None

# Example usage
if __name__ == "__main__":
    generator = DalleImageGenerator()
    prompt = "a white siamese cat"
    image_url = generator.generate_image(prompt, size="1024x1024", quality="standard", n=1)
    if image_url:
        print(f"Image successfully generated. URL: {image_url}")
    else:
        print("Image generation failed.")