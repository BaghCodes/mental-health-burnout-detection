// Main form submission handler
document.getElementById('burnoutForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Get form data
    const formData = {
        sleep: parseFloat(document.getElementById('sleep').value),
        work: parseFloat(document.getElementById('work').value),
        screen: parseFloat(document.getElementById('screen').value),
        heartRate: document.getElementById('heartRate').value ? 
                  parseInt(document.getElementById('heartRate').value) : 72,
        steps: document.getElementById('steps').value ? 
              parseInt(document.getElementById('steps').value) : 5000
    };

    // Validate input
    if (formData.sleep < 0 || formData.work < 0 || formData.screen < 0) {
        showError('Please enter valid positive numbers for all required fields.');
        return;
    }

    // Show loading state
    showLoading();
    hideError();
    hideResults();

    try {
        // Call backend for risk prediction
        const riskResponse = await fetch('http://localhost:3000/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (!riskResponse.ok) {
            throw new Error(`Backend error: ${riskResponse.status}`);
        }

        const riskData = await riskResponse.json();
        
        // Call AI service for wellness tips
        const tipsResponse = await fetch('http://localhost:5001/tips', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ...riskData,
                ...formData
            })
        });

        if (!tipsResponse.ok) {
            throw new Error(`AI service error: ${tipsResponse.status}`);
        }

        const tipsData = await tipsResponse.json();

        // Display results
        displayResults(riskData, tipsData);

    } catch (error) {
        console.error('Error:', error);
        showError(`Failed to analyze your data: ${error.message}. Please ensure both backend services are running.`);
    } finally {
        hideLoading();
    }
});

function displayResults(riskData, tipsData) {
    // Display risk score
    const scoreElement = document.getElementById('riskScore');
    const categoryElement = document.getElementById('riskCategory');
    const descriptionElement = document.getElementById('riskDescription');

    scoreElement.textContent = riskData.score;
    categoryElement.textContent = riskData.category;

    // Set risk level styling
    scoreElement.className = `risk-score risk-${riskData.category.toLowerCase()}`;

    // Set description based on risk level
    const descriptions = {
        'Low': 'Great job! Your current lifestyle shows low burnout risk. Keep maintaining these healthy habits.',
        'Moderate': 'You\'re showing some signs of stress. Consider implementing the recommendations below.',
        'High': 'Your burnout risk is elevated. Please prioritize self-care and consider the urgent recommendations below.'
    };
    descriptionElement.textContent = descriptions[riskData.category] || 'Assessment complete.';

    // Display AI tips
    const tipsList = document.getElementById('tipsList');
    tipsList.innerHTML = '';
    
    if (tipsData.tips && tipsData.tips.length > 0) {
        tipsData.tips.forEach(tip => {
            const li = document.createElement('li');
            li.textContent = tip;
            tipsList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.textContent = 'No specific recommendations at this time. Continue monitoring your wellness.';
        tipsList.appendChild(li);
    }

    // Show results section
    showResults();
}

function showLoading() {
    document.getElementById('loadingSection').style.display = 'block';
    document.getElementById('submitBtn').disabled = true;
    document.getElementById('submitBtn').textContent = '🔄 Analyzing...';
}

function hideLoading() {
    document.getElementById('loadingSection').style.display = 'none';
    document.getElementById('submitBtn').disabled = false;
    document.getElementById('submitBtn').textContent = '🔍 Analyze My Burnout Risk';
}

function showError(message) {
    const errorSection = document.getElementById('errorSection');
    errorSection.textContent = message;
    errorSection.style.display = 'block';
}

function hideError() {
    document.getElementById('errorSection').style.display = 'none';
}

function showResults() {
    document.getElementById('resultsSection').style.display = 'block';
}

function hideResults() {
    document.getElementById('resultsSection').style.display = 'none';
}

// Add some helpful placeholder text updates
document.addEventListener('DOMContentLoaded', function() {
    // Auto-focus on first input
    document.getElementById('sleep').focus();
    
    // Add helpful tooltips via title attributes
    document.getElementById('sleep').title = 'Enter your total sleep hours from last night';
    document.getElementById('work').title = 'Enter your total work hours from yesterday';
    document.getElementById('screen').title = 'Enter your total screen time (work + personal)';
    document.getElementById('heartRate').title = 'Optional: Your average heart rate (if available)';
    document.getElementById('steps').title = 'Optional: Your total steps taken yesterday';
});
