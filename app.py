from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from services.image_description import ImageDescriptionGenerator
from services.clip_embeddings import DINOEmbeddingsGenerator
from services.image_comparator import ImageComparator
from scrapper.google_scrapper import GoogleShoppingScraper
from scrapper.amazon_scrapper import AsyncAmazonScraper
from utils.file_handling import FileHandler
from utils.api_responses import APIResponse
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup directories
UPLOAD_DIR = Path("uploads")
FETCHED_IMAGES_DIR = Path("fetched_images")
IMAGE_DIR = Path("images")
UPLOAD_DIR.mkdir(exist_ok=True)
FETCHED_IMAGES_DIR.mkdir(exist_ok=True)
IMAGE_DIR.mkdir(exist_ok=True)

# Initialize services
logger.info(f"OPENAI_KEY: {os.getenv('OPENAI_KEY')}")
description_generator = ImageDescriptionGenerator(api_key=os.getenv("OPENAI_KEY"))
dino_generator = DINOEmbeddingsGenerator()
comparator = ImageComparator()
scraper = GoogleShoppingScraper(save_dir=str(FETCHED_IMAGES_DIR))
amazon_scrapper = AsyncAmazonScraper(save_dir=str(FETCHED_IMAGES_DIR))

# Setup templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Serve the main HTML page.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process/")
async def process_image(
    file: UploadFile = File(...),
    garment_type: str = Form(...),
    garment_layer: str = Form(None),
) -> JSONResponse:
    """
    Process the uploaded image by generating a description and retrieving similar items.
    """
    try:
        # Clean directories before processing
        FileHandler.clean_directory(UPLOAD_DIR)
        FileHandler.clean_directory(FETCHED_IMAGES_DIR)
        FileHandler.clean_directory(IMAGE_DIR)

        # Save the uploaded file
        file_path = await FileHandler.save_uploaded_file(file, UPLOAD_DIR)

        # Generate description using GPT-4 Vision
        description = await description_generator.generate_description(
            file_path=file_path, garment_type=garment_type, garment_layer=garment_layer
        )

        # Generate embeddings for the uploaded image
        clip_embeddings = await dino_generator.generate_embeddings(file_path)

        # Scrape Google Shopping for similar items
        try:
            google_results = await scraper.scrape_and_save(description, max_results=40)
        except Exception as e:
            logger.error(f"Error scraping Google Shopping: {e}")
            raise HTTPException(
                status_code=500,
                detail="There was an issue during search. Please try again.",
            )

        # Scrape Amazon
        try:
            amazon_results = await amazon_scrapper.scrape_and_save(
                description, max_results=20
            )
        except Exception as e:
            logger.error(f"Error scraping Amazon: {e}")
            raise HTTPException(
                status_code=500,
                detail="There was an issue during search. Please try again.",
            )

        try:
            google_results.extend(amazon_results)
        except Exception as e:
            logger.error(f"Error processing combined results: {e}")
            raise HTTPException(status_code=500, detail=str(e))

        # Generate vectors for fetched items
        for item in google_results:
            if item.get("local_image_path"):
                item["vectors"] = await dino_generator.generate_embeddings(
                    item["local_image_path"]
                )

        # Sort results by similarity
        sorted_results = await comparator.sort_dicts_by_similarity(
            clip_embeddings, google_results, cleanup=False
        )

        return APIResponse.success_response(
            {
                "description": description,
                "results": sorted_results,
            }
        )

    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/health/")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok"}
