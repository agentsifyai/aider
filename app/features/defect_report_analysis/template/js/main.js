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
            fileSelectedMessage.textContent = `The file "${file.name}" has been uploaded. Press "Process PDF" to continue.`;
            fileSelected.style.display = 'block';
        } else {
            fileSelected.style.display = 'none';
        }
    });

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        // Reset previous results
        toggleVisibility(resultSection, false);
        toggleVisibility(errorSection, false);

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
            const response = await fetch('/defect-report-analysis/upload', {
                method: 'POST',
                body: formData
            });

            // Hide loading spinner
            toggleVisibility(loadingContainer, false);

            const data = await response.json();

            if (response.ok) {
                showResult(data.defect_list, data.filename, data.defect_amount);
            } else {
                showError(data.error || 'An error occurred while processing the PDF');
            }
        } catch (error) {
            // Hide loading spinner in case of error
            toggleVisibility(loadingContainer, false);
            showError('An error occurred while uploading the file');
        }
    });

    function showResult(defectList, filename, amount) {
        const filenameDisplay = document.getElementById('filename-display');
        filenameDisplay.textContent = `File: ${filename || 'Unknown'}`;

        const amountDisplay = document.getElementById('defect-amount-display');
        amountDisplay.textContent = `Total defects amount: ${amount || 'Unknown'}`;

        const tableBody = document.getElementById('defects-table-body');
        const noDefectsMessage = document.getElementById('no-defects-message');
        const tableContainer = document.getElementById('table-container');

        // Clear any previous results
        tableBody.innerHTML = '';

        try {
            let defects = defectList;

            if (Array.isArray(defects) && defects.length > 0) {
                populateDefectsTable(defects, tableBody);

                // Show the table, hide the no defects message
                toggleVisibility(tableContainer, true);
                toggleVisibility(noDefectsMessage, false);
            } else {
                // No defects found
                toggleVisibility(tableContainer, false);
                toggleVisibility(noDefectsMessage, true);
            }
        } catch (error) {
            // Handle parsing error
            showError(`Could not parse defects data: ${error.message}. Raw data: ${defectList}`);
            return;
        }

        toggleVisibility(resultSection, true);
        toggleVisibility(errorSection, false);
    }

    function populateDefectsTable(defects, tableBody) {
        defects.forEach(defect => {
            const row = document.createElement('tr');
    
            const confidenceCell = createTableCell(defect.confidence || 'Unknown confidence');
            const nameCell = createTableCell(defect.name || 'Unknown defect');
            const locationCell = createTableCell(defect.location || 'Unknown location');
    
            // Create dropdown button cell
            const dropdownCell = document.createElement('td');
            const dropdownButton = document.createElement('button');
            dropdownButton.textContent = 'Details';
            dropdownButton.classList.add('dropdown-button');
            dropdownCell.appendChild(dropdownButton);
    
            row.appendChild(confidenceCell);
            row.appendChild(nameCell);
            row.appendChild(locationCell);
            row.appendChild(dropdownCell);
    
            tableBody.appendChild(row);
    
            // Create additional info row (hidden by default)
            const additionalInfoRow = document.createElement('tr');
            additionalInfoRow.classList.add('additional-info-row');
            additionalInfoRow.style.display = 'none';
    
            const additionalInfoCell = document.createElement('td');
            additionalInfoCell.colSpan = 4; // Span across all columns
            additionalInfoCell.innerHTML = renderAdditionalInfo(defect) || '<p>No additional information available</p>';
            additionalInfoRow.appendChild(additionalInfoCell);
    
            tableBody.appendChild(additionalInfoRow);
    
            // Add event listener to toggle visibility of additional info
            dropdownButton.addEventListener('click', () => {
                const isVisible = additionalInfoRow.style.display === 'table-row';
                additionalInfoRow.style.display = isVisible ? 'none' : 'table-row';
            });
        });
    }

    function renderAdditionalInfo(defect) {
        if (!defect) {
            return '<p>No additional information available</p>';
        }
    
        const infoEntries = [
            { label: 'Confidence Reason', value: defect.confidence_reason ?? 'Unknown' },
            { label: 'Evidence', value: defect.evidence ? "<i>" + defect.evidence + "</i>" : 'Unknown' },
            { label: 'Severity', value: defect.severity ?? 'Unknown' }, // Example of an additional field
            { label: 'Reported By', value: defect.reported_by ?? 'Unknown' } // Example of another additional field
        ];
    
        return infoEntries
            .map(entry => `<p><b>${entry.label}:</b> ${entry.value}</p>`)
            .join('');
    }

    function createTableCell(content) {
        const cell = document.createElement('td');
        cell.textContent = content;
        return cell;
    }

    function toggleVisibility(element, isVisible) {
        element.style.display = isVisible ? 'block' : 'none';
    }

    function showError(message) {
        errorMessage.textContent = message;
        toggleVisibility(errorSection, true);
        toggleVisibility(resultSection, false);
    }
});