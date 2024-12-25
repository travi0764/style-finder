// Image Upload Handler
class ImageUpload {
    constructor() {
        this.dropZone = document.getElementById('dropZone');
        this.fileInput = document.getElementById('fileInput');
        this.imagePreview = document.getElementById('imagePreview');
        this.dropZoneContent = document.querySelector('.drop-zone-content');
        this.selectedFile = null;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        this.dropZone.addEventListener('click', () => this.fileInput.click());
        this.dropZone.addEventListener('dragover', this.handleDragOver.bind(this));
        this.dropZone.addEventListener('drop', this.handleDrop.bind(this));
        this.fileInput.addEventListener('change', this.handleFileSelect.bind(this));
    }

    handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        this.dropZone.style.borderColor = 'var(--primary-color)';
    }

    handleDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        this.dropZone.style.borderColor = '';
        
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            this.handleFile(file);
        }
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.handleFile(file);
        }
    }

    handleFile(file) {
        this.selectedFile = file;
        const reader = new FileReader();

        reader.onload = (e) => {
            this.imagePreview.src = e.target.result;
            this.imagePreview.hidden = false;
            this.dropZoneContent.hidden = true;
        };

        reader.readAsDataURL(file);
        return file;
    }

    getSelectedFile() {
        return this.selectedFile;
    }
}