import aiofiles
import requests
from pathlib import Path
from fastapi import UploadFile
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FileHandler:
    @staticmethod
    async def save_uploaded_file(file: UploadFile, upload_dir: Path) -> str:
        """
        Save an uploaded file asynchronously to the specified directory.

        Args:
            file (UploadFile): The uploaded file.
            upload_dir (Path): Directory to save the file.

        Returns:
            str: Path to the saved file.
        """
        try:
            file_path = upload_dir / file.filename
            async with aiofiles.open(file_path, "wb") as buffer:
                content = await file.read()
                await buffer.write(content)
            logger.info(f"File saved successfully: {file_path}")
            return str(file_path)
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            raise RuntimeError(f"Error saving file: {e}")

    @staticmethod
    async def save_image_from_url(
        image_url: str, save_path: str, file_name: str = None
    ) -> str:
        """
        Download and save an image from a URL asynchronously to local storage.

        Args:
            image_url (str): URL of the image to download.
            save_path (str): Directory path to save the image.
            file_name (str, optional): Name of the saved file (default: derived from the URL).

        Returns:
            str: Full path of the saved image.
        """
        try:
            # Create the save directory if it doesn't exist
            os.makedirs(save_path, exist_ok=True)

            # Get the file name from the URL if not provided
            if not file_name:
                file_name = image_url.split("/")[-1]

            full_save_path = os.path.join(save_path, file_name)

            # Download the image synchronously (requests is not async)
            async with aiofiles.open(full_save_path, "wb") as file:
                response = requests.get(image_url, stream=True)
                if response.status_code == 200:
                    for chunk in response.iter_content(1024):
                        await file.write(chunk)
                    logger.info(f"Image saved: {full_save_path}")
                    return full_save_path
                else:
                    logger.error(
                        f"Failed to download image. HTTP status code: {response.status_code}"
                    )
                    raise RuntimeError(
                        f"Failed to download image: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"An error occurred while downloading the image: {e}")
            raise RuntimeError(f"Error downloading image: {e}")

    @staticmethod
    def clean_directory(directory: Path) -> None:
        """
        Clean all files in the specified directory.

        Args:
            directory (Path): Path to the directory to clean.

        Returns:
            None
        """
        try:
            if directory.exists() and directory.is_dir():
                for file in directory.iterdir():
                    if file.is_file():
                        file.unlink()
                        logger.info(f"Deleted file: {file}")
            else:
                logger.warning(
                    f"Directory does not exist or is not a directory: {directory}"
                )
        except Exception as e:
            logger.error(f"Error cleaning directory {directory}: {e}")
            raise RuntimeError(f"Error cleaning directory: {e}")
