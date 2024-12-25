# Style Finder

Style Finder is a powerful AI-driven tool designed to help users find similar garments online by analyzing uploaded images of clothing. Users can upload a picture, specify garment details, and receive recommendations for similar items from online shopping platforms.

## Features

- **Garment Detection and Description**: Utilizes OpenAI's GPT-4 Vision API to generate detailed descriptions of uploaded images.
- **Embeddings Generation**: Leverages DINOv2 to compute embeddings for similarity comparison.
- **Search Capability**: Scrapes Google Shopping for related garments and ranks them based on similarity.
- **Multi-layer Support**: Allows users to specify whether the uploaded garment is an upper layer (e.g., T-shirt, jacket) or lower layer.
- **Modular Design**: Includes separate services for embedding generation, image comparison, and scraping, enabling flexibility and scalability.

## Directory Structure

```plaintext
travi0764-style-finder/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── services/
│   ├── image_description.py
│   ├── image_comparator.py
│   ├── __init__.py
│   └── clip_embeddings.py
├── app.py
├── scrapper/
│   ├── amazon_scrapper.py
│   ├── google_scrapper.py
│   └── __init__.py
├── requirements.txt
├── Prompts_Versions/
│   ├── prompt_v2.py
│   ├── prompts_v3.py
│   └── prompts_v1.py
├── Dockerfile
├── templates/
│   └── index.html
├── utils/
│   ├── api_responses.py
│   ├── file_handling.py
│   └── __init__.py
└── static/
    ├── images/
    ├── css/
    │   └── styles.css
    └── js/
        ├── imageUpload.js
        ├── main.js
        ├── api.js
        ├── results.js
        └── app.js
```

## Installation and Running Locally

### Prerequisites
- Python 3.8+
- Docker (optional, for containerized deployment)

### Steps to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/style-finder.git
   cd style-finder
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   uvicorn app:app --reload
   ```

5. Access the application at `http://127.0.0.1:8000/`.

### Docker Setup
1. Build the Docker image:
   ```bash
   docker build -t style-finder .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 style-finder
   ```

## Usage

1. Upload an image of a garment via the web interface.
2. Specify garment type (e.g., upper, lower) and layer (e.g., T-shirt, jacket).
3. View a detailed description of the garment and browse similar items retrieved from Google Shopping.

## Project Structure

### **Core Components**
- **`app.py`**: Main application file for FastAPI.
- **`services/`**: Contains the core logic for image description, embedding generation, and comparison.
- **`scrapper/`**: Modules for scraping data from Google Shopping and Amazon.
- **`utils/`**: Utility functions for file handling and API responses.
- **`Prompts_Versions/`**: Stores different versions of prompts for GPT-4 Vision.
- **`static/`**: Frontend assets (CSS, JavaScript).
- **`templates/`**: HTML templates for the web application.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Create a pull request.

## Disclaimer

This project includes code for scraping publicly available data from Google and Amazon to demonstrate similarity-based search functionality. Please note:

1. The scraping functionality is intended for **educational and research purposes only**.
2. Users are responsible for ensuring their use of this code complies with the **terms of service** of the platforms being scraped (e.g., Google, Amazon).
3. The authors of this project are not liable for any misuse of this code or for any legal implications arising from its use.

<!-- For production applications, we recommend using official APIs (e.g., [Google Custom Search JSON API](https://developers.google.com/custom-search/v1/introduction) or [Amazon Product Advertising API](https://webservices.amazon.com/)) to ensure compliance with platform policies. -->


## Contact

For questions or feedback, feel free to reach out:
- **Email**: travi0764@gmail.com
- **GitHub**: [travi0764](https://github.com/*travi0764)

---

Thank you for using Style Finder!
