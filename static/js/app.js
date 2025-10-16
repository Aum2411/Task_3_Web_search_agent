// ==================== 
// State Management
// ====================

const state = {
    currentQuery: '',
    currentResults: null,
    isSearching: false
};

// ==================== 
// DOM Elements
// ====================

const elements = {
    // Sections
    searchSection: document.getElementById('searchSection'),
    loadingSection: document.getElementById('loadingSection'),
    resultsSection: document.getElementById('resultsSection'),
    errorSection: document.getElementById('errorSection'),
    
    // Search
    searchForm: document.getElementById('searchForm'),
    searchInput: document.getElementById('searchInput'),
    searchButton: document.getElementById('searchButton'),
    
    // Loading
    loadingText: document.getElementById('loadingText'),
    loadingSteps: {
        step1: document.getElementById('step1'),
        step2: document.getElementById('step2'),
        step3: document.getElementById('step3')
    },
    
    // Results
    queryText: document.getElementById('queryText'),
    summaryText: document.getElementById('summaryText'),
    sourcesCount: document.getElementById('sourcesCount'),
    sourcesGrid: document.getElementById('sourcesGrid'),
    backButton: document.getElementById('backButton'),
    
    // Error
    errorMessage: document.getElementById('errorMessage'),
    retryButton: document.getElementById('retryButton'),
    
    // Other
    statusBadge: document.getElementById('statusBadge'),
    toast: document.getElementById('toast'),
    toastMessage: document.getElementById('toastMessage')
};

// ==================== 
// Utility Functions
// ====================

function showSection(sectionName) {
    // Hide all sections
    elements.searchSection.classList.add('hidden');
    elements.loadingSection.classList.add('hidden');
    elements.resultsSection.classList.add('hidden');
    elements.errorSection.classList.add('hidden');
    
    // Show requested section
    switch(sectionName) {
        case 'search':
            elements.searchSection.classList.remove('hidden');
            break;
        case 'loading':
            elements.loadingSection.classList.remove('hidden');
            break;
        case 'results':
            elements.resultsSection.classList.remove('hidden');
            break;
        case 'error':
            elements.errorSection.classList.remove('hidden');
            break;
    }
    
    // Scroll to top smoothly
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showToast(message, duration = 3000) {
    elements.toastMessage.textContent = message;
    elements.toast.classList.remove('hidden');
    
    setTimeout(() => {
        elements.toast.classList.add('hidden');
    }, duration);
}

function updateStatus(status, text) {
    const dot = elements.statusBadge.querySelector('.status-dot');
    const span = elements.statusBadge.querySelector('span');
    
    span.textContent = text;
    
    // Update colors based on status
    if (status === 'searching') {
        dot.style.background = '#ff9800';
        elements.statusBadge.style.background = 'rgba(255, 152, 0, 0.1)';
        elements.statusBadge.style.borderColor = 'rgba(255, 152, 0, 0.3)';
        elements.statusBadge.style.color = '#ff9800';
    } else if (status === 'error') {
        dot.style.background = '#f44336';
        elements.statusBadge.style.background = 'rgba(244, 67, 54, 0.1)';
        elements.statusBadge.style.borderColor = 'rgba(244, 67, 54, 0.3)';
        elements.statusBadge.style.color = '#f44336';
    } else {
        dot.style.background = '#4caf50';
        elements.statusBadge.style.background = 'rgba(76, 175, 80, 0.1)';
        elements.statusBadge.style.borderColor = 'rgba(76, 175, 80, 0.3)';
        elements.statusBadge.style.color = '#4caf50';
    }
}

// ==================== 
// Loading Animation
// ====================

function animateLoadingSteps() {
    const steps = [
        { step: 'step1', text: 'Searching the web...', delay: 0 },
        { step: 'step2', text: 'Filtering relevant results...', delay: 2000 },
        { step: 'step3', text: 'Analyzing with AI...', delay: 4000 }
    ];
    
    steps.forEach(({ step, text, delay }) => {
        setTimeout(() => {
            if (state.isSearching) {
                // Remove active from all steps
                Object.values(elements.loadingSteps).forEach(el => {
                    el.classList.remove('active');
                });
                
                // Add active to current step
                elements.loadingSteps[step].classList.add('active');
                elements.loadingText.textContent = text;
            }
        }, delay);
    });
}

// ==================== 
// Search Functions
// ====================

async function performSearch(query) {
    if (!query.trim()) {
        showToast('Please enter a search query');
        return;
    }
    
    state.currentQuery = query;
    state.isSearching = true;
    
    // Update UI
    showSection('loading');
    updateStatus('searching', 'Searching...');
    animateLoadingSteps();
    
    try {
        // Make API request
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                num_results: 10,
                filter_results: true
            })
        });
        
        const data = await response.json();
        
        state.isSearching = false;
        
        if (data.success) {
            // Display results
            displayResults(data);
            updateStatus('ready', 'Ready');
        } else {
            // Show error
            showError(data.error || 'An error occurred while searching');
        }
        
    } catch (error) {
        state.isSearching = false;
        showError('Network error. Please check your connection and try again.');
        console.error('Search error:', error);
    }
}

// ==================== 
// Display Functions
// ====================

function displayResults(data) {
    // Update query display
    elements.queryText.textContent = data.query;
    
    // Update summary
    elements.summaryText.textContent = data.summary;
    
    // Update sources count
    const sourceCount = data.results.length;
    elements.sourcesCount.textContent = `${sourceCount} source${sourceCount !== 1 ? 's' : ''}`;
    
    // Clear and populate sources grid
    elements.sourcesGrid.innerHTML = '';
    
    data.results.forEach((result, index) => {
        const sourceCard = createSourceCard(result, index + 1);
        elements.sourcesGrid.appendChild(sourceCard);
    });
    
    // Store results in state
    state.currentResults = data;
    
    // Show results section
    showSection('results');
}

function createSourceCard(source, number) {
    const card = document.createElement('a');
    card.className = 'source-card';
    card.href = source.link;
    card.target = '_blank';
    card.rel = 'noopener noreferrer';
    
    card.innerHTML = `
        <div class="source-number">${number}</div>
        <div class="source-title">${escapeHtml(source.title)}</div>
        <div class="source-snippet">${escapeHtml(source.snippet)}</div>
        <div class="source-link">
            <i class="fas fa-external-link-alt"></i>
            <span>${getDomain(source.link)}</span>
        </div>
    `;
    
    return card;
}

function showError(message) {
    elements.errorMessage.textContent = message;
    showSection('error');
    updateStatus('error', 'Error');
}

// ==================== 
// Helper Functions
// ====================

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function getDomain(url) {
    try {
        const urlObj = new URL(url);
        return urlObj.hostname.replace('www.', '');
    } catch (e) {
        return url;
    }
}

// ==================== 
// Event Listeners
// ====================

// Search form submission
elements.searchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const query = elements.searchInput.value.trim();
    performSearch(query);
});

// Example chip clicks
document.querySelectorAll('.example-chip').forEach(chip => {
    chip.addEventListener('click', () => {
        const query = chip.getAttribute('data-query');
        elements.searchInput.value = query;
        performSearch(query);
    });
});

// Back button
elements.backButton.addEventListener('click', () => {
    showSection('search');
    elements.searchInput.value = '';
    elements.searchInput.focus();
});

// Retry button
elements.retryButton.addEventListener('click', () => {
    if (state.currentQuery) {
        performSearch(state.currentQuery);
    } else {
        showSection('search');
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        if (!elements.searchSection.classList.contains('hidden')) {
            elements.searchInput.focus();
        }
    }
    
    // Escape to go back to search
    if (e.key === 'Escape') {
        if (!elements.searchSection.classList.contains('hidden')) {
            elements.searchInput.blur();
        } else if (!elements.resultsSection.classList.contains('hidden')) {
            showSection('search');
        }
    }
});

// ==================== 
// Initialization
// ====================

async function checkHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        if (data.agent_initialized) {
            updateStatus('ready', 'Ready');
        } else {
            updateStatus('error', 'Configuration Error');
            showToast('Please configure your API keys', 5000);
        }
    } catch (error) {
        updateStatus('error', 'Connection Error');
        console.error('Health check failed:', error);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Focus search input
    elements.searchInput.focus();
    
    // Check health
    checkHealth();
    
    // Add smooth scroll behavior
    document.documentElement.style.scrollBehavior = 'smooth';
    
    console.log('🤖 Web Search Agent initialized!');
});

// ==================== 
// Additional Enhancements
// ====================

// Typing effect for search input placeholder
let placeholderIndex = 0;
const placeholders = [
    'What are the latest AI developments?',
    'How does quantum computing work?',
    'Best practices for web development in 2025',
    'What is the current state of climate change?',
    'Explain blockchain technology'
];

function rotatePlaceholder() {
    if (elements.searchSection.classList.contains('hidden') || 
        document.activeElement === elements.searchInput) {
        return;
    }
    
    placeholderIndex = (placeholderIndex + 1) % placeholders.length;
    elements.searchInput.placeholder = placeholders[placeholderIndex];
}

// Rotate placeholder every 3 seconds
setInterval(rotatePlaceholder, 3000);

// Add parallax effect to background orbs
document.addEventListener('mousemove', (e) => {
    const mouseX = e.clientX / window.innerWidth;
    const mouseY = e.clientY / window.innerHeight;
    
    const orbs = document.querySelectorAll('.gradient-orb');
    orbs.forEach((orb, index) => {
        const speed = (index + 1) * 20;
        const x = (mouseX - 0.5) * speed;
        const y = (mouseY - 0.5) * speed;
        
        orb.style.transform = `translate(${x}px, ${y}px)`;
    });
});

// Performance monitoring
if (window.performance && window.performance.getEntriesByType) {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log(`⚡ Page loaded in ${Math.round(perfData.loadEventEnd - perfData.fetchStart)}ms`);
        }, 0);
    });
}

// Add online/offline detection
window.addEventListener('online', () => {
    showToast('Connection restored ✓');
    updateStatus('ready', 'Ready');
});

window.addEventListener('offline', () => {
    showToast('No internet connection', 5000);
    updateStatus('error', 'Offline');
});

// Prevent form resubmission on back button
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}
