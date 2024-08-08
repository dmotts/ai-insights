document.addEventListener('DOMContentLoaded', function() {
    const steps = Array.from(document.querySelectorAll('.form-step'));
    const nextBtns = document.querySelectorAll('.next-step');
    const prevBtns = document.querySelectorAll('.prev-step');
    const submitBtn = document.querySelector('.submit-form');
    const progress = document.getElementById('progress');
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

    // Save form state to localStorage
    function saveFormState() {
        const formData = new FormData(document.getElementById('reportForm'));
        const data = Object.fromEntries(formData.entries());
        localStorage.setItem('formState', JSON.stringify(data));
        localStorage.setItem('currentStep', currentStep);
    }

    // Restore form state from localStorage
    function restoreFormState() {
        const savedState = JSON.parse(localStorage.getItem('formState'));
        const savedStep = localStorage.getItem('currentStep');

        if (savedState) {
            for (const [key, value] of Object.entries(savedState)) {
                const input = document.querySelector(`[name="${key}"]`);
                if (input) {
                    if (input.type === 'radio') {
                        document.querySelector(`input[name="${key}"][value="${value}"]`).checked = true;
                    } else {
                        input.value = value;
                    }
                }
            }
        }

        if (savedStep !== null) {
            currentStep = parseInt(savedStep, 10);
            showStep(currentStep);
        }
    }

    // Clear form state from localStorage
    function clearFormState() {
        localStorage.removeItem('formState');
        localStorage.removeItem('currentStep');
    }

    // Event listeners for form navigation
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

    // Event listener for form submission
    submitBtn.addEventListener('click', () => {
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
                alert('Report generated successfully!');
                window.open(response.pdf_url, '_blank');
                window.location.href = `/view_report/${response.report_id}`;
                clearFormState();
            } else {
                alert('Error: ' + response.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Save form state on input change
    document.querySelectorAll('.form-control').forEach(input => {
        input.addEventListener('input', function() {
            saveFormState();
        });
    });

    document.querySelectorAll('input[type="radio"]').forEach(input => {
        input.addEventListener('change', function() {
            saveFormState();
        });
    });

    // Restore form state on page load
    restoreFormState();

    showStep(currentStep);

    // Initialize Bootstrap tooltips
    $(function () {
        $('[data-toggle="tooltip"]').tooltip();
    });
});
