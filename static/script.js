document.addEventListener('DOMContentLoaded', function() {
    const steps = Array.from(document.querySelectorAll('.form-step'));
    const nextBtns = document.querySelectorAll('.next-step');
    const prevBtns = document.querySelectorAll('.prev-step');
    const submitBtn = document.querySelector('.submit-form');
    const progress = document.getElementById('progress');
    let currentStep = 0;

    function showStep(step) {
        steps.forEach((el, index) => {
            el.classList.toggle('active', index === step);
        });
        progress.style.width = `${(step / (steps.length - 1)) * 100}%`;
    }

    nextBtns.forEach(button => {
        button.addEventListener('click', () => {
            if (currentStep < steps.length - 1) {
                currentStep++;
                showStep(currentStep);
            }
        });
    });

    prevBtns.forEach(button => {
        button.addEventListener('click', () => {
            if (currentStep > 0) {
                currentStep--;
                showStep(currentStep);
            }
        });
    });

    submitBtn.addEventListener('click', () => {
        const formData = new FormData(document.getElementById('reportForm'));
        const data = Object.fromEntries(formData.entries());
        data.includeIntroduction = formData.get('includeIntroduction') !== null;
        data.includeIndustryTrends = formData.get('includeIndustryTrends') !== null;
        data.includeAISolutions = formData.get('includeAISolutions') !== null;
        data.includeAnalysis = formData.get('includeAnalysis') !== null;
        data.includeConclusion = formData.get('includeConclusion') !== null;

        fetch('/generate_report', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(response => {
            if (response.status === 'success') {
                alert('Report generated successfully!');
                // Redirect or open the PDF and HTML report
                window.open(response.pdf_url, '_blank'); // Opens PDF in a new tab
                // Optionally redirect to the HTML version
                window.location.href = `/view_report/${response.report_id}`;
            } else {
                alert('Error: ' + response.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Initialize the form by showing the first step
    showStep(currentStep);
});
