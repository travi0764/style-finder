from openai import AsyncOpenAI
import openai
import base64
import re
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageDescriptionGenerator:
    def __init__(self, api_key: str):
        """Initialize the ImageDescriptionGenerator with the OpenAI API key.

        Args:
            api_key (str): OpenAI API key.
        """

        self.client = AsyncOpenAI(api_key=api_key)

    async def generate_description(
        self, file_path: str, garment_type: str, garment_layer: Optional[str] = None
    ) -> str:
        """
        Generate a detailed description of the image using GPT-4 Vision.

        Args:
            file_path (str): Path to the image file.
            garment_type (str): General type of garment (e.g., "upper").
            garment_layer (Optional[str]): Specific layer or type (e.g., "jacket").

        Returns:
            str: Generated description.
        """
        try:
            prompt = await self._create_prompt(garment_type, garment_layer)

            base64_image = await self._encode_image(file_path)

            logger.info("Generating description with GPT-4 Vision.")
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt,
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
            )

            description = await self._process_response(response)

            logger.info("Description generation successful.")

            return description
        except openai.OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise RuntimeError(f"OpenAI API error: {e}")
        except Exception as e:
            logger.error(f"Error generating description: {e}")
            raise RuntimeError(f"Error generating description: {e}")
        finally:
            # Clean up temporary file
            self._cleanup_file(file_path)

    async def _create_prompt(
        self, garment_type: str, garment_layer: Optional[str]
    ) -> str:
        """Create the prompt for the GPT-4 Vision model.

        Args: garment_type (str): General type of garment (e.g., "upper").
            garment_layer (Optional[str]): Specific layer or type (e.g., "jacket").

        Returns: str: Prompt for the GPT-4 Vision model.
        """
        prompt = f"You are analyzing an image of a {garment_type} garment."
        if garment_layer:
            prompt += f" This garment specifically belongs to the {garment_layer.lower()} layer."

        prompt = """
Please provide an extremely detailed and specific description of the garment, covering the following categories. For each category, ensure the description is concise (1-2 words or short phrases) and avoid generating full sentences or explanations. Exclude the category names and provide only the values in the specified order, separated by commas.

### Categories to Include (in the given order):
1. Garment Type: Specify the specific garment type (e.g., bomber jacket, halter dress, hoodie, puffer coat).
2. Gender: The intended gender for the garment (e.g., man, woman, unisex).
4. Fit: Indicate the fit of the garment (e.g., "relaxed fit", "regular fit", "fitted").
5. Fabric/Material: Specify the primary fabric or material used (e.g., "100% wool", "denim", "silk blend").
6. Texture: Describe the texture of the fabric (e.g., "smooth", "ribbed", "soft").
7. Closure Type: Indicate the closure mechanism (e.g., "zippered", "button-down", "drawstring").
8. Neckline/Collar: Specify the neckline or collar type (e.g., "V-neck", "high collar", "notched collar").
9. Sleeve Type: Specify the type of sleeves (e.g., "long sleeves", "short sleeves", "puffed sleeves").
10. Pockets: Indicate the number and type of pockets, if any (e.g., "two side pockets", "no pockets").
11. Additional Design Features: Highlight any distinctive details (e.g., "ruffled hem", "embroidered logo", "belt loops").
12. Length: Specify the length of the garment (e.g., "waist-length", "knee-length").
13. Lining: Indicate if the garment has lining and describe it briefly (e.g., "fully lined", "no lining").
14. Branding or Logos: Mention visible branding or logos, if applicable (e.g., "small 'Adidas' logo on chest").
15. Occasion/Use: Specify the occasion or use for which the garment is intended (e.g., "casual wear", "formal wear", "activewear").

### Output Format:
Provide the description as a single comma-separated list of values. Do not include category names, explanations, or additional commentary. 

### Example Output:
For a bomber jacket:  
Bomber jacket, Man, Solid black, Relaxed fit, 100% nylon, Smooth, Zippered, Ribbed collar, Long sleeves, Two zippered pockets, Ribbed cuffs and embroidered logo, Waist-length, Fully lined, Small 'Nike' logo, Casual wear

### Guidelines:
1. Focus only on features that are visually identifiable from the garment in the image. Exclude unnecessary details or assumptions.  
2. Avoid including any references to people, backgrounds, or irrelevant details outside the garment itself.  
3. Ensure the description is accurate and concise, strictly following the order provided.  
4. Do not generate category names or additional commentary in the output.
"""

        return prompt

    async def _encode_image(self, file_path: str) -> str:
        """Encode the image file as a base64 string.

        Args:
            file_path (str): Path to the image file.

        Raises:
            RuntimeError: If there is an error encoding the image.

        Returns:
            str: Base64 encoded image string.
        """
        try:
            with open(file_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except Exception as e:
            logger.error(f"Error encoding image: {e}")
            raise RuntimeError(f"Error encoding image: {e}")

    async def _process_response(self, response) -> str:
        """Process the GPT-4 Vision response to extract the generated description.

        Args:
            response (_type_): Response object from GPT-4 Vision.

        Raises:
            RuntimeError: If there is an error processing the response.

        Returns:
            str: Generated description.
        """
        try:
            content = response.choices[0].message.content
            return re.sub(r"\s*\n\s*", ", ", content)
        except Exception as e:
            logger.error(f"Error processing response: {e}")
            raise RuntimeError(f"Error processing response: {e}")

    def _cleanup_file(self, file_path: str) -> None:
        """Delete a file to clean up temporary storage."""
        pass
