// Landing Page JavaScript

// Theme Toggle Function
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Add rotation animation
    const themeButton = document.getElementById('themeToggle');
    themeButton.style.transform = 'rotate(360deg)';
    setTimeout(() => {
        themeButton.style.transform = 'rotate(0deg)';
    }, 300);
}

// Handle Get Started - redirect to main app
function handleGetStarted() {
    // Redirect to main application
    window.location.href = './index.html';
}

// Initialize theme on landing page
document.addEventListener('DOMContentLoaded', () => {
    const theme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', theme);
});