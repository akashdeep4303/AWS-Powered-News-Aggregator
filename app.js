// Replace with your API Gateway URL
const API_BASE_URL = 'YOUR_API_GATEWAY_URL';

// DOM Elements
const newsContainer = document.getElementById('news-container');
const template = document.getElementById('news-card-template');
const navLinks = document.querySelectorAll('.nav-link');

// Fetch news articles
async function fetchNews(category = 'all') {
    try {
        const url = category === 'all' 
            ? `${API_BASE_URL}/news`
            : `${API_BASE_URL}/news/${category}`;
            
        const response = await fetch(url);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch news');
        }
        
        return data;
    } catch (error) {
        console.error('Error fetching news:', error);
        return [];
    }
}

// Create news card
function createNewsCard(article) {
    const clone = template.content.cloneNode(true);
    
    clone.querySelector('.card-title').textContent = article.title;
    clone.querySelector('.description').textContent = article.description;
    clone.querySelector('.source').textContent = `Source: ${article.source}`;
    clone.querySelector('.read-more').href = article.url;
    
    return clone;
}

// Display news articles
async function displayNews(category = 'all') {
    // Clear existing content
    newsContainer.innerHTML = '';
    
    // Show loading state
    newsContainer.innerHTML = '<div class="col-12 text-center">Loading...</div>';
    
    // Fetch and display news
    const articles = await fetchNews(category);
    newsContainer.innerHTML = '';
    
    if (articles.length === 0) {
        newsContainer.innerHTML = '<div class="col-12 text-center">No news articles found.</div>';
        return;
    }
    
    articles.forEach(article => {
        newsContainer.appendChild(createNewsCard(article));
    });
}

// Handle navigation
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        
        // Update active state
        navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        
        // Display news for selected category
        const category = link.dataset.category;
        displayNews(category);
    });
});

// Initial load
displayNews(); 