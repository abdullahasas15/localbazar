// Initialize Lucide icons
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // Background image rotation functionality
    const backgroundImages = document.querySelectorAll('.background-image');
    const dots = document.querySelectorAll('.dot');
    let currentImageIndex = 0;
    let imageInterval;

    // Function to show specific background image
    function showImage(index) {
        // Remove active class from all images and dots
        backgroundImages.forEach(img => img.classList.remove('active'));
        dots.forEach(dot => dot.classList.remove('active'));
        
        // Add active class to current image and dot
        backgroundImages[index].classList.add('active');
        dots[index].classList.add('active');
        
        currentImageIndex = index;
    }

    // Function to rotate to next image
    function nextImage() {
        const nextIndex = (currentImageIndex + 1) % backgroundImages.length;
        showImage(nextIndex);
    }

    // Start automatic rotation
    function startImageRotation() {
        imageInterval = setInterval(nextImage, 8000);
    }

    // Stop automatic rotation
    function stopImageRotation() {
        if (imageInterval) {
            clearInterval(imageInterval);
        }
    }

    // Add click event listeners to dots
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            stopImageRotation();
            showImage(index);
            // Restart rotation after manual selection
            setTimeout(startImageRotation, 5000);
        });
    });

    // Start the automatic rotation
    startImageRotation();

    // Search functionality
    const searchInput = document.getElementById('village-search');
    const searchBtn = document.getElementById('search-btn');

    function handleSearch() {
        const village = searchInput.value.trim();
        if (village) {
            // In a real app, this would navigate to search results
            alert(`Searching for shops in ${village}`);
            
            // Add some visual feedback
            searchBtn.style.transform = 'scale(0.95)';
            setTimeout(() => {
                searchBtn.style.transform = 'scale(1)';
            }, 150);
        } else {
            // Add shake animation for empty input
            searchInput.style.animation = 'shake 0.5s ease-in-out';
            setTimeout(() => {
                searchInput.style.animation = '';
            }, 500);
        }
    }

    // Search button click
    searchBtn.addEventListener('click', handleSearch);

    // Search input enter key
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });

    // Add shake animation CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
    `;
    document.head.appendChild(style);

    // Smooth scroll for navigation buttons
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const buttonText = button.textContent.toLowerCase();
            
            if (buttonText.includes('login')) {
                alert('Login functionality would be implemented here');
            } else if (buttonText.includes('register')) {
                alert('Registration functionality would be implemented here');
            } else if (buttonText.includes('cart')) {
                alert('Shopping cart would open here');
            }
        });
    });

    // CTA button functionality
    const ctaButtons = document.querySelectorAll('.cta-btn');
    ctaButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const buttonText = button.querySelector('span').textContent;
            
            if (buttonText.includes('Register Your Shop')) {
                alert('Shop registration form would open here');
            } else if (buttonText.includes('Shop Owner Login')) {
                alert('Shop owner login would open here');
            }
        });
    });

    // Footer link functionality
    const footerLinks = document.querySelectorAll('.footer-link');
    footerLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const linkText = link.textContent;
            alert(`${linkText} page would open here`);
        });
    });

    // Add fade-in animation to elements when they come into view
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);

    // Observe elements for fade-in animation
    const fadeElements = document.querySelectorAll('.cta-card, .trust-indicators, .hero-content');
    fadeElements.forEach(el => observer.observe(el));

    // Add hover effects for interactive elements
    const interactiveElements = document.querySelectorAll('.nav-btn, .cta-btn, .search-btn');
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', () => {
            element.style.transform = 'translateY(-2px)';
        });
        
        element.addEventListener('mouseleave', () => {
            element.style.transform = 'translateY(0)';
        });
    });

    // Image error handling
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('error', function() {
            // Create a fallback SVG for broken images
            const svgFallback = `
                <svg width="88" height="88" xmlns="http://www.w3.org/2000/svg" stroke="#000" stroke-linejoin="round" opacity=".3" fill="none" stroke-width="3.7">
                    <rect x="16" y="16" width="56" height="56" rx="6"/>
                    <path d="m16 58 16-18 32 32"/>
                    <circle cx="53" cy="35" r="7"/>
                </svg>
            `;
            
            // Create a data URL from the SVG
            const svgDataUrl = 'data:image/svg+xml;base64,' + btoa(svgFallback);
            this.src = svgDataUrl;
            this.style.opacity = '0.3';
        });
    });

    // Add loading state to search button
    searchBtn.addEventListener('click', function() {
        const originalText = this.innerHTML;
        this.innerHTML = '<i data-lucide="loader-2"></i><span>Searching...</span>';
        this.disabled = true;
        
        // Re-initialize icons for the new loader icon
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
        
        // Simulate search delay
        setTimeout(() => {
            this.innerHTML = originalText;
            this.disabled = false;
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        }, 2000);
    });

    // Add smooth scroll behavior for anchor links
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

    // Add keyboard navigation support
    document.addEventListener('keydown', (e) => {
        // Escape key to close any modals or overlays
        if (e.key === 'Escape') {
            // Close any open modals here
        }
        
        // Enter key on search input
        if (e.key === 'Enter' && document.activeElement === searchInput) {
            handleSearch();
        }
    });

    // Add touch support for mobile devices
    let touchStartX = 0;
    let touchEndX = 0;

    document.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    });

    document.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });

    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;
        
        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                // Swipe left - next image
                stopImageRotation();
                nextImage();
                setTimeout(startImageRotation, 5000);
            } else {
                // Swipe right - previous image
                stopImageRotation();
                const prevIndex = currentImageIndex === 0 ? backgroundImages.length - 1 : currentImageIndex - 1;
                showImage(prevIndex);
                setTimeout(startImageRotation, 5000);
            }
        }
    }

    // Performance optimization: Pause animations when tab is not visible
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            stopImageRotation();
        } else {
            startImageRotation();
        }
    });

    // Add console welcome message
    console.log(`
        🛍️ Welcome to LocalBazaar.com!
        
        This is a vanilla HTML/CSS/JS implementation of the LocalBazaar landing page.
        
        Features:
        - Dynamic background image rotation
        - Interactive search functionality
        - Responsive design
        - Smooth animations
        - Touch/swipe support for mobile
        
        Built with ❤️ for local communities.
    `);
}); 