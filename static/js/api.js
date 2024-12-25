// API Service
class ApiService {
    constructor(baseUrl = 'http://localhost:8080') {
        this.baseUrl = baseUrl;
    }

    async searchSimilarGarments(formData) {
        const response = await fetch(`${this.baseUrl}/process`, {
            method: 'POST',
            body: formData
        });
    
        if (!response.ok) {
            throw new Error('Failed to process image');
        }
    
        const data = await response.json();
        console.log('Parsed API Response:', data); // Debugging log
        return data; // Return the full response object
    }
    
    
}
