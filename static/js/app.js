// Main App
document.addEventListener('DOMContentLoaded', () => {
    const imageUpload = new ImageUpload();
    const apiService = new ApiService();
    const resultsHandler = new ResultsHandler();

    const form = document.getElementById('uploadForm');
    const garmentType = document.getElementById('garmentType');
    const garmentLayer = document.getElementById('garmentLayer');
    const searchButton = document.getElementById('searchButton');
    const loader = document.getElementById('loader');

    function updateSearchButtonState() {
        const isValid = imageUpload.getSelectedFile() && 
                       garmentType.value.trim() && 
                       garmentLayer.value.trim();
        searchButton.disabled = !isValid;
    }

    function showLoader() {
        loader.classList.add('visible');
    }

    function hideLoader() {
        loader.classList.remove('visible');
    }

    garmentType.addEventListener('input', updateSearchButtonState);
    garmentLayer.addEventListener('input', updateSearchButtonState);

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const file = imageUpload.getSelectedFile();
        if (!file || !garmentType.value || !garmentLayer.value) return;

        const formData = new FormData();
        formData.append('file', file);
        formData.append('garment_type', garmentType.value);
        formData.append('garment_layer', garmentLayer.value);

        showLoader();
        resultsHandler.clear();
        searchButton.disabled = true;

        try {
            const response = await apiService.searchSimilarGarments(formData);
            resultsHandler.displayResults(response);
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to process image. Please try again.');
        } finally {
            hideLoader();
            searchButton.disabled = false;
        }
    });
});