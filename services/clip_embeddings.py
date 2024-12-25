import asyncio
from typing import Any
import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DINOEmbeddingsGenerator:
    def __init__(self):
        """Initialize the DINO embeddings generator with pre-trained model and processor."""
        self.image_processor = AutoImageProcessor.from_pretrained(
            "facebook/dinov2-base"
        )
        self.model = AutoModel.from_pretrained("facebook/dinov2-base")

    async def generate_embeddings(self, file_path: str) -> Any:
        """
        Generate embeddings for the given image file asynchronously.

        Args:
            file_path (str): Path to the image file.

        Returns:
            Any: The embeddings generated for the image.
        """
        try:
            logger.info(f"Generating embeddings for image: {file_path}")
            image = await self._load_image(file_path)
            inputs = self.image_processor(image, return_tensors="pt")

            with torch.no_grad():
                outputs = self.model(**inputs)

            embedding = outputs.last_hidden_state[:, 0, :].squeeze(1)
            logger.info("Embeddings generation successful.")
            return embedding.numpy()
        except Exception as e:
            logger.error(f"Error generating embeddings for {file_path}: {e}")
            raise RuntimeError(f"Error generating embeddings: {e}")

    async def _load_image(self, file_path: str) -> Image.Image:
        """
        Load an image file asynchronously.

        Args:
            file_path (str): Path to the image file.

        Returns:
            Image.Image: The loaded image object.
        """
        try:
            loop = asyncio.get_event_loop()
            image = await loop.run_in_executor(
                None, lambda: Image.open(file_path).convert("RGB")
            )
            logger.info(f"Image loaded successfully: {file_path}")
            return image
        except Exception as e:
            logger.error(f"Error loading image {file_path}: {e}")
            raise RuntimeError(f"Error loading image: {e}")
