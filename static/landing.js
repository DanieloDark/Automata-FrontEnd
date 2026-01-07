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

// Show auth modal
function showAuthModal(type) {
    const modal = document.getElementById('authModal');
    modal.classList.add('show');
    switchAuthForm(type);
}

// Hide auth modal
function hideAuthModal() {
    const modal = document.getElementById('authModal');
    modal.classList.remove('show');
}

// Switch between login and signup forms
function switchAuthForm(type) {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    
    if (type === 'login') {
        loginForm.style.display = 'block';
        signupForm.style.display = 'none';
    } else {
        loginForm.style.display = 'none';
        signupForm.style.display = 'block';
    }
}

// Handle login
async function handleLogin(event) {
    event.preventDefault();
    
    const form = event.target;
    const email = form.querySelector('input[type="email"]').value;
    const password = form.querySelector('input[type="password"]').value;
    
    try {
        const response = await fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        if (!response.ok) {
            throw new Error('Login failed');
        }
        
        const data = await response.json();
        
        // Store session/token if needed
        if (data.token) {
            localStorage.setItem('authToken', data.token);
        }
        
        // Redirect to main app
        window.location.href = '/';
        
    } catch (error) {
        console.error('Login error:', error);
        alert('Login failed. Please check your credentials.');
    }
}

// Handle signup
async function handleSignup(event) {
    event.preventDefault();
    
    const form = event.target;
    const name = form.querySelector('input[type="text"]').value;
    const email = form.querySelector('input[type="email"]').value;
    const password = form.querySelectorAll('input[type="password"]')[0].value;
    const confirmPassword = form.querySelectorAll('input[type="password"]')[1].value;
    
    // Validate passwords match
    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return;
    }
    
    try {
        const response = await fetch('http://127.0.0.1:5000/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, email, password })
        });
        
        if (!response.ok) {
            throw new Error('Signup failed');
        }
        
        const data = await response.json();
        
        // Store session/token if needed
        if (data.token) {
            localStorage.setItem('authToken', data.token);
        }
        
        // Redirect to main app
        window.location.href = '/';
        
    } catch (error) {
        console.error('Signup error:', error);
        alert('Signup failed. Please try again.');
    }
}

// Close modal when clicking outside
document.addEventListener('click', (e) => {
    const modal = document.getElementById('authModal');
    if (e.target === modal) {
        hideAuthModal();
    }
});

// Initialize theme on landing page
document.addEventListener('DOMContentLoaded', () => {
    const theme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', theme);
});