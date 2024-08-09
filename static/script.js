document.addEventListener('DOMContentLoaded', function() {
    const steps = Array.from(document.querySelectorAll('.form-step'));
    const nextBtns = document.querySelectorAll('.next-step');
    const prevBtns = document.querySelectorAll('.prev-step');
    const submitBtn = document.querySelector('.submit-form');
    const progress = document.getElementById('progress');
    const loadingAnimation = document.getElementById('loadingAnimation');
    const successMessage = document.getElementById('successMessage');
    const downloadButton = document.getElementById('downloadButton');
    let currentStep = 0;

    // Function to show the current step
    function showStep(step) {
        steps.forEach((el, index) => {
            el.classList.remove('previous', 'next');
            el.classList.toggle('active', index === step);
        });
        updateProgress();
        if (step === steps.length - 1) {
            populateSummary();
        }
    }

    // Function to update progress bar
    function updateProgress() {
        const totalSteps = steps.length;
        const progressPercentage = ((currentStep + 1) / totalSteps) * 100;
        progress.style.width = `${progressPercentage}%`;
        progress.innerText = `${Math.round(progressPercentage)}%`;
    }

    // Function to populate summary step
    function populateSummary() {
        const summaryDiv = document.getElementById('summary');
        summaryDiv.innerHTML = ''; // Clear existing content
        const formData = new FormData(document.getElementById('reportForm'));

        const summaryData = {
            'Name': formData.get('client_name'),
            'Email': formData.get('client_email'),
            'Business Industry': formData.get('industry'),
            'What are your current data management and utilization challenges?': formData.get('question1'),
            'What are the areas of technology integration and inefficiency?': formData.get('question2'),
            'What are your long-term business goals and AI\'s role in achieving them?': formData.get('question3'),
        };

        for (const [question, answer] of Object.entries(summaryData)) {
            const summaryItem = document.createElement('div');
            summaryItem.className = 'summary-item';
            summaryItem.innerHTML = `<strong>${question}:</strong><br>${answer}`;
            summaryDiv.appendChild(summaryItem);
        }
    }

    // Client-side validation (Basic example)
    function validateStep() {
        const currentFields = steps[currentStep].querySelectorAll('input, textarea');
        for (const field of currentFields) {
            if (!field.checkValidity()) {
                alert('Please complete all required fields before proceeding.');
                return false;
            }
        }
        return true;
    }

    function showLoading() {
        const activeStep = document.querySelector('.form-step.active');
        $(activeStep).fadeOut(400, function() {
            loadingAnimation.classList.remove('d-none');
            loadingAnimation.classList.add('d-block');
        });
    }

    function showSuccess(downloadUrl) {
        $(loadingAnimation).fadeOut(400, function() {
            successMessage.classList.remove('d-none');
            successMessage.classList.add('d-block');
            downloadButton.href = downloadUrl;
        });
    }

    submitBtn.addEventListener('click', () => {
        if (validateStep()) {
            showLoading();

            const formData = new FormData(document.getElementById('reportForm'));
            const data = Object.fromEntries(formData.entries());

            fetch('/generate_report', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(response => {
                if (response.status === 'success') {
                    showSuccess(response.pdf_url);
                } else {
                    alert('An error occurred, please try again.');
                    window.location.reload();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An unexpected error occurred. Please try again.');
                window.location.reload();
            });
        }
    });

    // Event listeners for form navigation
    nextBtns.forEach(button => {
        button.addEventListener('click', () => {
            if (validateStep() && currentStep < steps.length - 1) {
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

    showStep(currentStep);

    // Initialize Bootstrap tooltips
    $(function () {
        $('[data-toggle="tooltip"]').tooltip();
    });
});
