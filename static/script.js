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

    // Client-side validation (Enhanced)
    function validateStep() {
        const currentFields = steps[currentStep].querySelectorAll('input, textarea, select');
        let isValid = true;

        for (const field of currentFields) {
            if (!field.checkValidity()) {
                field.classList.add('is-invalid');
                isValid = false;
            } else {
                field.classList.remove('is-invalid');
                field.classList.add('is-valid');
            }
        }

        if (!isValid) {
            alert('Please complete all required fields correctly before proceeding.');
        }

        return isValid;
    }

    function showLoading() {
        const activeStep = document.querySelector('.form-step.active');
        activeStep.style.opacity = 1;
        let fadeEffect = setInterval(function () {
            if (!activeStep.style.opacity) {
                activeStep.style.opacity = 1;
            }
            if (activeStep.style.opacity > 0) {
                activeStep.style.opacity -= 0.1;
            } else {
                clearInterval(fadeEffect);
                activeStep.style.display = 'none'; // Ensure the block is not displayed
                loadingAnimation.classList.remove('d-none');
                loadingAnimation.classList.add('d-block');
            }
        }, 50);
    }

    function showSuccess(downloadUrl) {
        loadingAnimation.style.opacity = 1;
        let fadeEffect = setInterval(function () {
            if (loadingAnimation.style.opacity > 0) {
                loadingAnimation.style.opacity -= 0.1;
            } else {
                clearInterval(fadeEffect);
                loadingAnimation.classList.remove('d-block');
                loadingAnimation.classList.add('d-none');

                successMessage.classList.remove('d-none');
                successMessage.classList.add('d-block');
                successMessage.style.opacity = 0;
                let fadeInEffect = setInterval(function () {
                    if (successMessage.style.opacity < 1) {
                        successMessage.style.opacity = parseFloat(successMessage.style.opacity) + 0.1;
                    } else {
                        clearInterval(fadeInEffect);
                    }
                }, 50);

                downloadButton.href = downloadUrl;
            }
        }, 50);
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
