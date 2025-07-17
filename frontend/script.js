// JavaScript for handling navigation and dynamic content
function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => {
        section.style.display = 'none';
    });
    document.getElementById(sectionId).style.display = 'block';
}

// Chat history storage
let chatHistory = [];

// Function to ask question to the chatbot
async function askQuestion(question) {
    try {
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: question,
                chat_history: chatHistory
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Add to chat history
        chatHistory.push({
            question: question,
            answer: data.response
        });
        
        return data.response;
    } catch (error) {
        console.error('Error asking question:', error);
        return 'Sorry, there was an error processing your request. Please try again.';
    }
}

// Calculate fluid requirement
function calculateFluidRequirement(weight) {
    if (weight <= 0) return 'Please enter a valid weight';
    
    let fluidRequirement;
    if (weight <= 10) {
        fluidRequirement = weight * 100;
    } else if (weight <= 20) {
        fluidRequirement = 1000 + (weight - 10) * 50;
    } else {
        fluidRequirement = 1500 + (weight - 20) * 20;
    }
    
    return `Daily fluid requirement: ${fluidRequirement} mL (${(fluidRequirement/24).toFixed(1)} mL/hour)`;
}

// Initialize event listeners when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Guidelines section
    const guidelinesTextarea = document.querySelector('#guidelines textarea');
    const guidelinesButton = document.querySelector('#guidelines button');
    const guidelinesFeedback = document.querySelector('#guidelines .feedback');
    
    guidelinesButton.addEventListener('click', async function() {
        const question = guidelinesTextarea.value.trim();
        if (!question) {
            guidelinesFeedback.textContent = 'Please enter a question.';
            guidelinesFeedback.style.color = '#dc3545';
            return;
        }
        
        guidelinesButton.textContent = 'Processing...';
        guidelinesButton.disabled = true;
        
        const response = await askQuestion(question);
        guidelinesFeedback.textContent = response;
        guidelinesFeedback.style.color = '#28a745';
        
        guidelinesButton.textContent = 'Submit';
        guidelinesButton.disabled = false;
    });
    
    // Calculator section
    const weightInput = document.querySelector('#weight');
    const calculatorButton = document.querySelector('#calculator button');
    const calculatorFeedback = document.querySelector('#calculator .feedback');
    
    calculatorButton.addEventListener('click', function() {
        const weight = parseFloat(weightInput.value);
        if (isNaN(weight) || weight <= 0) {
            calculatorFeedback.textContent = 'Please enter a valid weight.';
            calculatorFeedback.style.color = '#dc3545';
            return;
        }
        
        const result = calculateFluidRequirement(weight);
        calculatorFeedback.textContent = result;
        calculatorFeedback.style.color = '#28a745';
    });
    
    // Quiz section
    const quizInput = document.querySelector('#quizzes input');
    const quizButton = document.querySelector('#quizzes button');
    const quizFeedback = document.querySelector('#quizzes .feedback');
    
    quizButton.addEventListener('click', function() {
        const answer = quizInput.value.trim().toLowerCase();
        if (!answer) {
            quizFeedback.textContent = 'Please enter an answer.';
            quizFeedback.style.color = '#dc3545';
            return;
        }
        
        // Simple quiz logic
        if (answer.includes('120') && answer.includes('80') || 
            answer.includes('systolic') || answer.includes('diastolic')) {
            quizFeedback.textContent = 'Correct! Normal blood pressure is typically around 120/80 mmHg.';
            quizFeedback.style.color = '#28a745';
        } else {
            quizFeedback.textContent = 'Not quite right. Normal blood pressure is typically around 120/80 mmHg (systolic/diastolic).';
            quizFeedback.style.color = '#dc3545';
        }
    });
});
