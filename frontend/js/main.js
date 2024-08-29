// Smooth Scrolling
document.addEventListener('DOMContentLoaded', () => {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);

            window.scrollTo({
                top: targetElement.offsetTop,
                behavior: 'smooth'
            });
        });
    });
});


// Add Glowing Effect on Focus
document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('.input-field');

    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.classList.add('glow');
        });
        input.addEventListener('blur', () => {
            input.classList.remove('glow');
        });
    });
});



// Simple Form Validation
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');

    form.addEventListener('submit', (event) => {
        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const message = document.getElementById('message').value.trim();

        if (name === '' || email === '' || message === '') {
            alert('Please fill out all fields.');
            event.preventDefault(); // Prevent form submission
        }
    });
});

// Toggle Light/Dark Mode
document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.querySelector('.sign');
    const body = document.body;

    // Check localStorage for saved mode
    if (localStorage.getItem('theme') === 'light') {
        body.classList.add('light-mode');
    }

    toggleButton.addEventListener('click', () => {
        body.classList.toggle('light-mode');
        // Save the current mode to localStorage
        if (body.classList.contains('light-mode')) {
            localStorage.setItem('theme', 'light');
        } else {
            localStorage.setItem('theme', 'dark');
        }
    });
});
