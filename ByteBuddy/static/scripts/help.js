document.addEventListener('DOMContentLoaded', function () {
    // Smooth scroll to top when clicking Contact Support
    const contactBtn = document.querySelector('.btn-light');
    if (contactBtn) {
        contactBtn.addEventListener('click', () => {
            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: 'smooth'
            });
            alert("Contact support functionality coming soon!");
        });
    }

    // Hover effect on footer links
    const footerLinks = document.querySelectorAll('footer li');
    footerLinks.forEach(link => {
        link.addEventListener('mouseover', () => {
            link.style.color = '#00bcd4';
        });
        link.addEventListener('mouseout', () => {
            link.style.color = '#999';
        });
    });

    // Optional: feather icon replacement if not already called inline
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
});
