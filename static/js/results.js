class ResultsHandler {
    constructor() {
        this.resultsSection = document.getElementById('resultsSection');
        this.resultsGrid = document.getElementById('resultsGrid');
    }

    displayResults(response) {
        const { data: { description, results } } = response;

        if (!Array.isArray(results)) {
            console.error('Expected results to be an array:', results);
            return;
        }

        this.resultsSection.hidden = false;
        this.resultsGrid.innerHTML = '';



        results.forEach(result => {
            const card = this.createResultCard(result);
            this.resultsGrid.appendChild(card);
        });
    }

    createResultCard(result) {
        const similarityPercentage = (result.cosine_similarity * 100).toFixed(1);
        const name = result.name || 'No name available';
        const price = result.price || 'Price not available';
        const rating = result.rating ? `⭐ ${result.rating}` : '';
    
        const card = document.createElement('div');
        card.className = 'result-card';
    
        card.innerHTML = `
            <div class="result-image-container">
                <img src="${result.image_url}" alt="${name}" class="result-image" loading="lazy">
            </div>
            <div class="result-info">
                <h3 class="product-name">${name}</h3>
                <p class="product-price">${price}</p>
                ${rating ? `<p class="product-rating">${rating}</p>` : ''}
                <p class="similarity-score">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="m6 9 6 6 6-6"/>
                    </svg>
                    ${similarityPercentage}% Match
                </p>
                <a href="${result.product_url}" target="_blank" class="view-product">
                    View Product
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                        <polyline points="15 3 21 3 21 9"/>
                        <line x1="10" y1="14" x2="21" y2="3"/>
                    </svg>
                </a>
            </div>
        `;
    
        return card;
    }

    
    clear() {
        this.resultsSection.hidden = true;
        this.resultsGrid.innerHTML = '';
    }
}