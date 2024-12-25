import numpy as np
from pathlib import Path
from typing import List, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageComparator:
    @staticmethod
    def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate the cosine similarity between two vectors.

        Args:
            vec1 (np.ndarray): First vector.
            vec2 (np.ndarray): Second vector.

        Returns:
            float: Cosine similarity value.
        """
        try:
            vec1 = vec1.flatten()
            vec2 = vec2.flatten()

            dot_product = np.dot(vec1, vec2)
            norm_vec1 = np.linalg.norm(vec1)
            norm_vec2 = np.linalg.norm(vec2)

            if norm_vec1 == 0 or norm_vec2 == 0:
                return 0.0

            return dot_product / (norm_vec1 * norm_vec2)
        except Exception as e:
            logger.error(f"Error calculating cosine similarity: {e}")
            raise

    async def sort_dicts_by_similarity(
        self,
        test_vector: np.ndarray,
        dict_list: List[Dict[str, np.ndarray]],
        cleanup: bool = False,
    ) -> List[Dict[str, float]]:
        """
        Sort a list of dictionaries based on cosine similarity to the test vector.

        Args:
            test_vector (np.ndarray): The vector to compare against.
            dict_list (List[Dict[str, np.ndarray]]): List of dictionaries with embeddings.
            cleanup (bool): Whether to delete image files after processing.

        Returns:
            List[Dict[str, float]]: Sorted list of dictionaries with similarity scores.
        """
        try:
            for entry in dict_list:
                entry["cosine_similarity"] = float(
                    self.cosine_similarity(test_vector, entry["vectors"])
                )

            sorted_dict_list = sorted(
                dict_list, key=lambda x: x["cosine_similarity"], reverse=True
            )

            # Log top 10 images for visual confirmation
            for item in sorted_dict_list[:10]:
                logger.info(
                    f"Similarity: {item['cosine_similarity']}, Image: {item['local_image_path']}"
                )

            # Cleanup temporary files if required
            if cleanup:
                await self._cleanup_files([entry["local_path"] for entry in dict_list])

            for item in sorted_dict_list:
                del item["vectors"]
            return sorted_dict_list
        except Exception as e:
            logger.error(f"Error sorting dictionaries by similarity: {e}")
            raise

    async def _cleanup_files(self, file_paths: List[str]) -> None:
        """
        Delete a list of files to clean up temporary storage.

        Args:
            file_paths (List[str]): List of file paths to delete.
        """
        try:
            for file_path in file_paths:
                temp_file = Path(file_path)
                if temp_file.exists():
                    temp_file.unlink()
                    logger.info(f"Temporary file {file_path} deleted.")
        except Exception as e:
            logger.warning(f"Failed to delete temporary file {file_path}: {e}")
