import aiohttp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from pathlib import Path
import json
import logging
from typing import List, Dict, Optional
from uuid import uuid4

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AsyncAmazonScraper:
    def __init__(self, save_dir: str):
        """Initialize the Amazon scraper.

        Args:
            save_dir (str): Directory to save the scraped results.
        """
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        self.image_dir = self.save_dir / "images"
        self.image_dir.mkdir(exist_ok=True)

    def _init_driver(self) -> webdriver.Chrome:
        """Initialize a headless Chrome driver.

        Returns:
            webdriver.Chrome: The Chrome driver instance.
        """
        chrome_options = Options()
        chrome_options.binary_location = "/usr/bin/chromium"  # Use Chromium binary
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service("/usr/bin/chromedriver")  # Point to ChromiumDriver binary
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def scrape_amazon(
        self, search_term: str, max_results: int = 20
    ) -> List[Dict[str, Optional[str]]]:
        """Scrape Amazon search results for a given search term.

        Returns:
            List[Dict]: List of dictionaries containing product information.
        """
        driver = self._init_driver()
        try:
            driver.get("https://www.amazon.in/")

            # Search for the term
            search_box = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
            )
            search_box.send_keys(search_term)
            search_box.send_keys(Keys.RETURN)

            # Wait for results to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "[data-component-type='s-search-result']")
                )
            )

            product_elements = driver.find_elements(
                By.CSS_SELECTOR, "[data-component-type='s-search-result']"
            )
            products = []

            for index, product in enumerate(product_elements[:max_results]):
                try:
                    name = (
                        product.find_element(
                            By.CSS_SELECTOR, "h2.a-size-base-plus span"
                        ).text
                        if product.find_elements(
                            By.CSS_SELECTOR, "h2.a-size-base-plus span"
                        )
                        else "No name available"
                    )
                    # Extract price
                    price_symbol = (
                        product.find_element(
                            By.CSS_SELECTOR, "span.a-price-symbol"
                        ).text
                        if product.find_elements(By.CSS_SELECTOR, "span.a-price-symbol")
                        else ""
                    )
                    price_whole = (
                        product.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
                        if product.find_elements(By.CSS_SELECTOR, "span.a-price-whole")
                        else ""
                    )
                    price = (
                        f"{price_symbol}{price_whole}"
                        if price_whole
                        else "No price available"
                    )
                    image_url = (
                        product.find_element(
                            By.CSS_SELECTOR, "img.s-image"
                        ).get_attribute("src")
                        if product.find_elements(By.CSS_SELECTOR, "img.s-image")
                        else None
                    )
                    rating = (
                        product.find_element(
                            By.CSS_SELECTOR, ".a-icon-alt"
                        ).get_attribute("innerHTML")
                        if product.find_elements(By.CSS_SELECTOR, ".a-icon-alt")
                        else "No rating available"
                    )
                    relative_url = (
                        product.find_element(
                            By.CSS_SELECTOR, "a.a-link-normal"
                        ).get_attribute("href")
                        if product.find_elements(By.CSS_SELECTOR, "a.a-link-normal")
                        else None
                    )
                    product_url = (
                        f"https://amazon.in{relative_url}"
                        if relative_url and not relative_url.startswith("http")
                        else relative_url
                    )

                    products.append(
                        {
                            "name": name,
                            "price": price,
                            "image_url": image_url,
                            "rating": rating,
                            "product_url": product_url,
                        }
                    )
                except Exception as e:
                    logger.warning(f"Error extracting product {index + 1}: {e}")

            return products
        finally:
            driver.quit()

    async def _fetch_image(
        self, session: aiohttp.ClientSession, url: str, save_path: Path
    ) -> Optional[str]:
        """Fetch an image from a URL and save it to a local path.

        Args:
            session (aiohttp.ClientSession): Client session for making requests.
            url (str): URL of the image.
            save_path (Path): Path to save the image.

        Returns:
            Optional[str]: Local path of the saved image or None if failed.
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

    async def scrape_and_save(
        self, search_term: str, max_results: int = 20
    ) -> List[Dict[str, Optional[str]]]:
        """Scrape Amazon search results for a given search term and save the results.

        Args:
            search_term (str): The search term or query.
            max_results (int, optional): Maximum number of results to scrape. Defaults to 20.

        Returns:
            List[Dict[str, Optional[str]]]: List of dictionaries containing product information.
        """
        try:
            products = self.scrape_amazon(search_term, max_results)
            async with aiohttp.ClientSession() as session:
                for product in products:
                    if product["image_url"]:
                        save_path = self.image_dir / f"{uuid4()}.jpg"
                        product["local_image_path"] = await self._fetch_image(
                            session, product["image_url"], save_path
                        )

            filename = f"{search_term}_results.json"
            self._save_results(products, filename)
            return products
        except Exception as e:
            logger.error(f"Error in scrape_and_save: {e}")
            return []

    def _save_results(
        self, results: List[Dict[str, Optional[str]]], filename: str
    ) -> None:
        """Save the scraped results to a JSON file

        Args:
            results (List[Dict[str, Optional[str]]]): List of dictionaries containing product information.
            filename (str): Name of the file to save the results.
        """

        file_path = self.save_dir / filename
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(results, file, indent=4)
            logger.info(f"Results saved to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save results: {e}")
