// Example: Simple page transition
document.addEventListener('DOMContentLoaded', function() {
    // Highlight current navigation link
    let links = document.querySelectorAll('nav a');
    links.forEach(link => {
        if (window.location.pathname.endsWith(link.getAttribute('href'))) {
            link.style.textDecoration = 'underline';
        }
    });
});