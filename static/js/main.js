import { imageUploadHandler } from './imageUpload.js';
import { apiService } from './api.js';
import { resultsHandler } from './results.js';

class App {
    constructor() {
        this.form = document.getElementById('uploadForm');
        this.loader = document.getElementById('loader');
        this.garmentType = document.getElementById('garmentType');
        this.garmentLayer = document.getElementById('garmentLayer');

        this.loader.classList.add('hidden'); // Ensure loader is hidden initially
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        this.garmentType.addEventListener('input', () => this.updateSearchButtonState());
        this.garmentLayer.addEventListener('input', () => this.updateSearchButtonState());
    }

    updateSearchButtonState() {
        imageUploadHandler.updateSearchButtonState();
    }
    
    async handleSubmit(e) {
        e.preventDefault();
    
        const file = imageUploadHandler.getSelectedFile();
        const type = this.garmentType.value;
        const layer = this.garmentLayer.value;
    
        if (!file || !type || !layer) {
            alert('Please fill in all the fields and upload an image.');
            return;
        }
    
        console.log('Showing loader...');
        this.loader.classList.add('active'); // Add "active" to show loader
        resultsHandler.clear(); // Clear any previous results
    
        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('garment_type', type);
            formData.append('garment_layer', layer);
    
            const response = await apiService.searchSimilarGarments(formData);
    
            resultsHandler.displayResults(response);
        } catch (error) {
            console.error('Error during API call:', error);
            alert('Failed to process image. Please try again.');
        } finally {
            console.log('Hiding loader...');
            this.loader.classList.remove('active'); // Remove "active" to hide loader
        }
    }
    
    
}


// Initialize the application
new App();