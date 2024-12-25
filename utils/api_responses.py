from fastapi.responses import JSONResponse
import logging
from typing import Any, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIResponse:
    @staticmethod
    def success_response(data: Dict[str, Any], status_code: int = 200) -> JSONResponse:
        """
        Return a standardized success JSON response.

        Args:
            data (Dict[str, Any]): Data to include in the response.
            status_code (int): HTTP status code for the response (default: 200).

        Returns:
            JSONResponse: The JSON response object.
        """
        try:
            logger.info(f"Generating success response with status {status_code}.")
            return JSONResponse(
                content={"success": True, "data": data}, status_code=status_code
            )
        except Exception as e:
            logger.error(f"Error generating success response: {e}")
            raise RuntimeError(f"Error generating success response: {e}")

    @staticmethod
    def error_response(message: str, status_code: int = 500) -> JSONResponse:
        """
        Return a standardized error JSON response.

        Args:
            message (str): Error message to include in the response.
            status_code (int): HTTP status code for the response (default: 500).

        Returns:
            JSONResponse: The JSON response object.
        """
        try:
            logger.info(
                f"Generating error response with status {status_code}: {message}"
            )
            return JSONResponse(
                content={"success": False, "error": message}, status_code=status_code
            )
        except Exception as e:
            logger.error(f"Error generating error response: {e}")
            raise RuntimeError(f"Error generating error response: {e}")
