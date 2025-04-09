document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('upload-form');
    const resultSection = document.getElementById('result-section');
    const errorSection = document.getElementById('error-section');
    const summaryText = document.getElementById('summary-text');
    const errorMessage = document.querySelector('.error-message');
    const fileInput = document.getElementById('pdf-file');
    const fileSelected = document.getElementById('file-selected');
    const fileSelectedMessage = document.getElementById('file-selected-message');

    // Show selected file message when a file is chosen
    fileInput.addEventListener('change', function () {
        const file = fileInput.files[0];
        if (file) {
            fileSelectedMessage.textContent = `The PDF "${file.name}" has been uploaded. Press "Process PDF" to continue.`;
            fileSelected.style.display = 'block';
        } else {
            fileSelected.style.display = 'none';
        }
    });

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        // Reset previous results
        resultSection.style.display = 'none';
        errorSection.style.display = 'none';

        const file = fileInput.files[0];

        if (!file) {
            showError('Please select a PDF file');
            return;
        }

        // Show loading spinner
        const loadingContainer = document.getElementById('loading-container');
        loadingContainer.style.display = 'flex';

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/bullet-document-report/upload', {
                method: 'POST',
                body: formData
            });

            // Hide loading spinner
            loadingContainer.style.display = 'none';

            const data = await response.json();

            if (response.ok) {
                showResult(data.summary, data.filename);
            } else {
                showError(data.error || 'An error occurred while processing the PDF');
            }
        } catch (error) {
            // Hide loading spinner in case of error
            loadingContainer.style.display = 'none';
            showError('An error occurred while uploading the file');
        }
    });

    function showResult(summary, filename) {
        const filenameDisplay = document.getElementById('filename-display');
        filenameDisplay.textContent = `File: ${filename || 'Unknown'}`;

        const tableBody = document.getElementById('defects-table-body');
        const noDefectsMessage = document.getElementById('no-defects-message');
        const tableContainer = document.getElementById('table-container');

        // Clear any previous results
        tableBody.innerHTML = '';

        try {
            // Try to parse the JSON if it's a string
            let defects = summary;
            if (typeof summary === 'string') {
                defects = JSON.parse(summary);
            }

            if (Array.isArray(defects) && defects.length > 0) {
                // We have defects to display in the table
                defects.forEach(defect => {
                    const row = document.createElement('tr');

                    const nameCell = document.createElement('td');
                    nameCell.textContent = defect.name || 'Unknown defect';
                    row.appendChild(nameCell);

                    const locationCell = document.createElement('td');
                    locationCell.textContent = defect.location || 'Unknown location';
                    row.appendChild(locationCell);

                    tableBody.appendChild(row);
                });

                // Show the table, hide the no defects message
                tableContainer.style.display = 'block';
                noDefectsMessage.style.display = 'none';
            } else {
                // No defects found
                tableContainer.style.display = 'none';
                noDefectsMessage.style.display = 'block';
            }
        } catch (error) {
            // Handle parsing error
            showError(`Could not parse defects data: ${error.message}. Raw data: ${summary}`);
            return;
        }

        resultSection.style.display = 'block';
        errorSection.style.display = 'none';
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorSection.style.display = 'block';
        resultSection.style.display = 'none';
    }
}); 