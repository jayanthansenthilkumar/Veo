// Gen AI Platform - Main JavaScript

// Utility Functions
const utils = {
    // Show notification
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    },
    
    // Format date
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },
    
    // Debounce function
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Copy to clipboard
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            this.showNotification('Copied to clipboard!', 'success');
        } catch (err) {
            this.showNotification('Failed to copy', 'error');
        }
    }
};

// API Handler
const api = {
    async generateImage(data) {
        const response = await fetch('/api/generate-image', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return response.json();
    },
    
    async generateVideo(data) {
        const response = await fetch('/api/generate-video', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return response.json();
    },
    
    async generateMusic(data) {
        const response = await fetch('/api/generate-music', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return response.json();
    },
    
    async getGeneration(id) {
        const response = await fetch(`/api/generations/${id}`);
        return response.json();
    },
    
    async getStats() {
        const response = await fetch('/api/stats');
        return response.json();
    }
};

// Loading Manager
const loadingManager = {
    show(element) {
        if (element) {
            element.classList.remove('hidden');
        }
    },
    
    hide(element) {
        if (element) {
            element.classList.add('hidden');
        }
    },
    
    setProgress(element, percent) {
        if (element) {
            element.style.width = `${percent}%`;
        }
    }
};

// Form Validation
const formValidator = {
    validatePrompt(prompt, minLength = 10) {
        if (!prompt || prompt.trim().length < minLength) {
            return {
                valid: false,
                message: `Prompt must be at least ${minLength} characters long`
            };
        }
        return { valid: true };
    },
    
    validateNumber(value, min, max) {
        const num = parseFloat(value);
        if (isNaN(num) || num < min || num > max) {
            return {
                valid: false,
                message: `Value must be between ${min} and ${max}`
            };
        }
        return { valid: true, value: num };
    }
};

// Image Gallery
class ImageGallery {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.images = [];
    }
    
    add(imagePath, metadata = {}) {
        this.images.push({ path: imagePath, metadata });
        this.render();
    }
    
    clear() {
        this.images = [];
        this.render();
    }
    
    render() {
        if (!this.container) return;
        
        if (this.images.length === 0) {
            this.container.innerHTML = `
                <div class="placeholder">
                    <i class="fas fa-image"></i>
                    <p>Your generated images will appear here</p>
                </div>
            `;
            return;
        }
        
        this.container.innerHTML = this.images.map((img, index) => `
            <div class="image-card" data-index="${index}">
                <img src="/${img.path}" alt="Generated Image ${index + 1}" loading="lazy">
                <div class="image-actions">
                    <button class="btn-icon" onclick="downloadImage('/${img.path}', 'image_${index + 1}.png')">
                        <i class="fas fa-download"></i>
                    </button>
                    <button class="btn-icon" onclick="utils.copyToClipboard('${window.location.origin}/${img.path}')">
                        <i class="fas fa-share"></i>
                    </button>
                </div>
            </div>
        `).join('');
    }
}

// Download Helper
function downloadImage(url, filename) {
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// Smooth Scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Active Navigation Link
window.addEventListener('DOMContentLoaded', () => {
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.background = 'rgba(255, 255, 255, 0.2)';
        }
    });
});

// Handle Errors Globally
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    utils.showNotification('An unexpected error occurred', 'error');
});

// Lazy Loading for Images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// Auto-save to localStorage
const autoSave = {
    save(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.error('LocalStorage error:', e);
        }
    },
    
    load(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.error('LocalStorage error:', e);
            return null;
        }
    },
    
    remove(key) {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.error('LocalStorage error:', e);
        }
    }
};

// Keyboard Shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K to focus search/prompt
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const promptInput = document.querySelector('textarea[name="prompt"]');
        if (promptInput) {
            promptInput.focus();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const modal = document.querySelector('.modal:not(.hidden)');
        if (modal) {
            modal.classList.add('hidden');
        }
    }
});

// Performance Monitoring
const perfMonitor = {
    start(label) {
        if (performance && performance.mark) {
            performance.mark(`${label}-start`);
        }
    },
    
    end(label) {
        if (performance && performance.mark && performance.measure) {
            performance.mark(`${label}-end`);
            performance.measure(label, `${label}-start`, `${label}-end`);
            const measure = performance.getEntriesByName(label)[0];
            console.log(`${label}: ${measure.duration.toFixed(2)}ms`);
        }
    }
};

// Export utilities for use in other scripts
window.GenAI = {
    utils,
    api,
    loadingManager,
    formValidator,
    ImageGallery,
    autoSave,
    perfMonitor
};

console.log('Gen AI Platform initialized');
