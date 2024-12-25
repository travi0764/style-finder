import aiohttp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from pathlib import Path
import json
from uuid import uuid4
from typing import List, Dict, Optional
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GoogleShoppingScraper:
    def __init__(self, save_dir: str):
        """Initialize the Google Shopping scraper.

        Args:
            save_dir (str): Directory to save the scraped results.
        """
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)

    def _init_driver(self) -> webdriver.Chrome:
        """Initialize a headless Chrome driver.

        Returns:
            webdriver.Chrome: The Chrome driver instance.
        """
        chrome_options = Options()
        chrome_options.binary_location = "/usr/bin/chromium"  # Point to Chromium binary
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service("/usr/bin/chromedriver")  # Point to ChromiumDriver binary
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    async def _fetch_image(
        self, session: aiohttp.ClientSession, url: str, save_path: Path
    ) -> Optional[str]:
        """Fetch an image from a URL and save it to a file.

        Args:
            session (aiohttp.ClientSession): Session object for making HTTP requests.
            url (str): URL of the image to fetch.
            save_path (Path): Path to save the image file.

        Returns:
            Optional[str]: Path to the saved image file or None if failed.
        """
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(save_path, "wb") as file:
                        file.write(await response.read())
                    logger.info(f"Image saved: {save_path}")
                    return str(save_path)
                else:
                    logger.warning(f"Failed to fetch image: {url}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching image {url}: {e}")
            return None

    def scrape_google_shopping(
        self, search_term: str, max_results: int = 40
    ) -> List[Dict[str, Optional[str]]]:
        """Scrape Google Shopping search results for a given search term.

        Args:
            search_term (str): The search term or query.
            max_results (int, optional): Maximum number of results to scrape. Defaults to 40.

        Returns:
            List[Dict[str, Optional[str]]]: _description_
        """
        driver = self._init_driver()
        try:
            driver.get("https://www.google.com/")

            # Search for the term
            search_box = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.send_keys(search_term)
            search_box.send_keys(Keys.RETURN)

            # Click on the "Shopping" tab
            shopping_tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Shopping"))
            )
            shopping_tab.click()

            # Wait for shopping results to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".sh-dgr__grid-result")
                )
            )

            # Scrape product details
            product_elements = driver.find_elements(
                By.CSS_SELECTOR, ".sh-dgr__grid-result"
            )
            products = []

            for index, product in enumerate(product_elements[:max_results]):
                try:
                    name = product.find_element(By.CSS_SELECTOR, "h3").text
                    price = product.find_element(By.CSS_SELECTOR, ".a8Pemb").text
                    url = product.find_element(By.CSS_SELECTOR, "a").get_attribute(
                        "href"
                    )
                    image_url = product.find_element(
                        By.CSS_SELECTOR, ".ArOc1c img"
                    ).get_attribute("src")
                    rating = (
                        product.find_element(By.CSS_SELECTOR, ".Rsc7Yb").text
                        if product.find_elements(By.CSS_SELECTOR, ".Rsc7Yb")
                        else "No rating available"
                    )

                    products.append(
                        {
                            "name": name,
                            "price": price,
                            "product_url": url,
                            "image_url": image_url,
                            "rating": rating,
                        }
                    )
                except Exception as e:
                    logger.warning(f"Error extracting product {index + 1}: {e}")

            return products
        finally:
            driver.quit()

    async def scrape_and_save(
        self, search_term: str, max_results: int = 40
    ) -> List[Dict[str, Optional[str]]]:
        """Scrape Google Shopping search results for a given search term and save the results

        Args:
            search_term (str): The search term or query.
            max_results (int, optional): Maximum number of results to scrape. Defaults to 40.

        Raises:
            Exception: Timeout while scraping Google Shopping if the scraping process takes too long.
            Exception: WebDriverException if there is an issue with the WebDriver.
            Exception: An unexpected error occurred during scraping.

        Returns:
            List[Dict[str, Optional[str]]]: List of scraped product details with image paths if available or None.
        """
        try:
            products = self.scrape_google_shopping(search_term, max_results)

            async with aiohttp.ClientSession() as session:
                for product in products:
                    if product["image_url"]:
                        save_path = self.save_dir / f"{uuid4()}.jpg"
                        product["local_image_path"] = await self._fetch_image(
                            session, product["image_url"], save_path
                        )

            filename = f"{uuid4()}_google_results.json"
            self._save_results(products, filename)
            return products
        except TimeoutException as e:
            logger.error(f"Timeout while scraping Google Shopping: {e}")
            logger.error(traceback.format_exc())
            raise Exception("Scraping timed out.")
        except WebDriverException as e:
            logger.error(f"WebDriver error: {e}")
            logger.error(traceback.format_exc())
            raise Exception("Scraping failed due to a WebDriver issue.")
        except Exception as e:
            logger.error(f"Unexpected error in scrape_and_save: {e}")
            logger.error(traceback.format_exc())
            raise Exception("An unexpected error occurred during scraping.")

    def _save_results(
        self, results: List[Dict[str, Optional[str]]], filename: str
    ) -> None:
        """Save the scraped results to a JSON file

        Args:
            results (List[Dict[str, Optional[str]]]): List of scraped product details.
            filename (str): Name of the file to save the results to.
        """
        file_path = self.save_dir / filename
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(results, file, indent=4)
            logger.info(f"Results saved to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save results: {e}")
