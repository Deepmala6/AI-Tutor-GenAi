document.getElementById('inputForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const grade = parseInt(document.getElementById('grade').value);
    const topic = document.getElementById('topic').value;

    if (!grade || !topic) {
        showError('Please fill in all fields');
        return;
    }

    // Show loading
    document.getElementById('resultsSection').classList.remove('hidden');
    document.getElementById('errorSection').classList.add('hidden');
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('resultsContainer').innerHTML = '';
    document.getElementById('refineButtonContainer').classList.add('hidden');

    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ grade, topic })
        });

        document.getElementById('loading').classList.add('hidden');

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'An error occurred');
        }

        const result = await response.json();
        displayResults(result);
        
        // Store current grade and topic for refinement
        window.currentGrade = grade;
        window.currentTopic = topic;

    } catch (error) {
        document.getElementById('loading').classList.add('hidden');
        showError(error.message);
    }
});

// Refine button event listener
document.addEventListener('DOMContentLoaded', () => {
    const refineButton = document.getElementById('refineButton');
    if (refineButton) {
        refineButton.addEventListener('click', refineContent);
    }
});

async function refineContent() {
    const grade = window.currentGrade;
    const topic = window.currentTopic;

    if (!grade || !topic) {
        showError('Grade and topic information missing');
        return;
    }

    // Show loading
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('refineButtonContainer').classList.add('hidden');

    try {
        const response = await fetch('/api/refine', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ grade, topic })
        });

        document.getElementById('loading').classList.add('hidden');

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'An error occurred');
        }

        const result = await response.json();
        displayAdvancedResults(result);

    } catch (error) {
        document.getElementById('loading').classList.add('hidden');
        showError(error.message);
    }
}

function displayResults(result) {
    const container = document.getElementById('resultsContainer');
    container.innerHTML = '';

    // Pipeline flow visualization
    const pipelineHtml = `
        <div class="pipeline-flow">
            <div class="pipeline-step active">📝 Generate</div>
            <div class="pipeline-arrow">→</div>
            <div class="pipeline-step ${result.review_status === 'pass' ? 'active' : ''}">✓ Review</div>
            ${result.refinement_applied ? `
                <div class="pipeline-arrow">→</div>
                <div class="pipeline-step active">🔄 Refine</div>
            ` : ''}
        </div>
    `;
    container.innerHTML += pipelineHtml;

    // Generated Content
    const generatedHtml = `
        <div class="result-card">
            <h3>📝 Generated Content</h3>
            ${renderContent(result.generated_content)}
        </div>
    `;
    container.innerHTML += generatedHtml;

    // Review Feedback
    const reviewHtml = `
        <div class="result-card ${result.review_status}">
            <h3>✓ Review Status</h3>
            <span class="status-badge ${result.review_status}">
                ${result.review_status.toUpperCase()}
            </span>
            ${result.review_feedback.length > 0 ? `
                <div class="feedback-list">
                    <strong>Feedback:</strong>
                    ${result.review_feedback.map(fb => `
                        <div class="feedback-item">${escapeHtml(fb)}</div>
                    `).join('')}
                </div>
            ` : '<p style="color: #28a745;">No issues found!</p>'}
        </div>
    `;
    container.innerHTML += reviewHtml;

    // Refined Content (if applicable)
    if (result.refinement_applied && result.refined_content) {
        const refinedHtml = `
            <div class="result-card" style="border-left-color: #667eea;">
                <h3>🔄 Refined Content</h3>
                <p style="color: #666; margin-bottom: 15px;">
                    <em>Content has been refined based on reviewer feedback.</em>
                </p>
                ${renderContent(result.refined_content)}
            </div>
        `;
        container.innerHTML += refinedHtml;
    }
    
    // Show refine button ALWAYS (for both PASS and FAIL)
    document.getElementById('refineButtonContainer').classList.remove('hidden');
}

function displayAdvancedResults(result) {
    const container = document.getElementById('resultsContainer');
    
    // Add separator
    const separator = document.createElement('hr');
    separator.style.margin = '30px 0';
    separator.style.borderColor = '#e0e0e0';
    container.appendChild(separator);
    
    // Add advanced content title
    const titleDiv = document.createElement('div');
    titleDiv.innerHTML = '<h2 style="text-align: center; color: #667eea; margin: 20px 0;">🚀 ADVANCED LEVEL CONTENT</h2>';
    container.appendChild(titleDiv);
    
    // Advanced Content
    const advancedHtml = `
        <div class="result-card" style="border-left-color: #ff6b6b; background: linear-gradient(135deg, rgba(255,107,107,0.1) 0%, rgba(102,126,234,0.1) 100%);">
            <h3>📚 Advanced Explanation & Questions</h3>
            <p style="color: #666; margin-bottom: 15px;">
                <em>More detailed and challenging content for deeper understanding.</em>
            </p>
            ${renderContent(result.generated_content)}
        </div>
    `;
    container.innerHTML += advancedHtml;
    
    // Hide refine button when showing advanced
    document.getElementById('refineButtonContainer').classList.add('hidden');
}

function renderContent(content) {
    if (!content) return '<p>No content generated</p>';

    let html = `
        <div class="explanation">
            <strong>Explanation:</strong><br>
            ${escapeHtml(content.explanation)}
        </div>
    `;

    if (content.mcqs && content.mcqs.length > 0) {
        html += '<div class="mcq-section"><strong>Questions:</strong>';
        
        content.mcqs.forEach((mcq, idx) => {
            html += `
                <div class="mcq-item">
                    <div class="mcq-question">Q${idx + 1}: ${escapeHtml(mcq.question)}</div>
                    <div class="mcq-options">
            `;
            
            mcq.options.forEach(option => {
                const isCorrect = option === mcq.answer;
                html += `
                    <div class="mcq-option ${isCorrect ? 'correct' : ''}">
                        ${isCorrect ? '✓ ' : '○ '} ${escapeHtml(option)}
                    </div>
                `;
            });
            
            html += '</div></div>';
        });
        
        html += '</div>';
    }

    return html;
}

function showError(message) {
    document.getElementById('errorSection').classList.remove('hidden');
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('resultsSection').classList.add('hidden');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
