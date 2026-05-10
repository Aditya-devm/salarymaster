document.addEventListener('DOMContentLoaded', () => {
    const experienceSlider = document.getElementById('experience-slider');
    const experienceVal = document.getElementById('experience-val');
    const gaugeFill = document.getElementById('gauge-fill');
    const dropZone = document.getElementById('drop-zone');
    const cvUpload = document.getElementById('cv-upload');
    const fileInfo = document.getElementById('file-info');
    const filenameLabel = document.getElementById('filename');
    const predictBtn = document.getElementById('predict-btn');
    const resultContainer = document.getElementById('prediction-result');
    const salaryDisplay = document.getElementById('salary-value');
    const roleDisplay = document.getElementById('target-role-display');
    const loader = document.getElementById('loader');

    // UI elements
    const roleSelect = document.getElementById('role-select');
    const eduSelect = document.getElementById('edu-select');

    const GAUGE_MAX = 502; // stroke-dasharray

    // Update Gauge
    function updateGauge(years) {
        experienceVal.textContent = years;
        const progress = Math.min(years / 30, 1);
        const offset = GAUGE_MAX * (1 - progress);
        gaugeFill.style.strokeDashoffset = offset;
    }

    experienceSlider.addEventListener('input', (e) => {
        updateGauge(e.target.value);
    });

    // File Upload Handling
    dropZone.addEventListener('click', () => cvUpload.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--accent)';
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.style.borderColor = 'var(--input-border)';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        if (file && file.type === 'application/pdf') {
            handleFileUpload(file);
        }
    });

    cvUpload.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) handleFileUpload(file);
    });

    async function handleFileUpload(file) {
        filenameLabel.textContent = file.name;
        fileInfo.classList.remove('hidden');
        
        const formData = new FormData();
        formData.append('file', file);

        loader.classList.remove('hidden');
        try {
            const response = await fetch('/parse_cv', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            
            if (data.success) {
                // Update form with extracted data
                if (data.features.Role) {
                    roleSelect.value = data.features.Role;
                }
                if (data.features.Education) {
                    eduSelect.value = data.features.Education;
                }
                if (data.features.Experience !== undefined) {
                    experienceSlider.value = data.features.Experience;
                    updateGauge(data.features.Experience);
                }
            }
        } catch (error) {
            console.error('Error parsing CV:', error);
        } finally {
            loader.classList.add('hidden');
        }
    }

    // Prediction Logic
    predictBtn.addEventListener('click', async () => {
        const payload = {
            role: roleSelect.value,
            education: eduSelect.value,
            experience: parseInt(experienceSlider.value)
        };

        loader.classList.remove('hidden');
        resultContainer.classList.add('hidden');

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await response.json();

            if (data.success) {
                salaryDisplay.textContent = data.salary_display;
                roleDisplay.textContent = payload.role;
                resultContainer.classList.remove('hidden');
                
                // Scroll to result
                resultContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        } catch (error) {
            console.error('Prediction failed:', error);
        } finally {
            loader.classList.add('hidden');
        }
    });

    // Initialize gauge
    updateGauge(0);
});
