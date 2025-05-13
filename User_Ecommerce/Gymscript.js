const menuIcon = document.querySelector('#menu-icon');
        const navbar = document.querySelector('.navbar');
      
        menuIcon.addEventListener('click', () => {
          navbar.classList.toggle('active');
        });

// Typing animation
const typed = new Typed('.multiple-text', {
    strings: ['Physical Fitness', 'Weight Gain', 'Strength Training', 'Weight Loss', 'Weight Lifting', 'Endurance Trainning'],
    typeSpeed: 60,
    backSpeed: 60,
    backDelay: 1000,
    loop: true
  });