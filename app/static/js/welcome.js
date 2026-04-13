// Elementos del DOM
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const tabLogin = document.getElementById('tab-login');
const tabRegister = document.getElementById('tab-register');
const tabIndicator = document.querySelector('.tab-indicator');

// Función para cambiar a Login
function showLogin() {
    loginForm.classList.add('active');
    registerForm.classList.remove('active');
    tabLogin.classList.add('active');
    tabRegister.classList.remove('active');
    tabIndicator.classList.remove('move-right');
}

// Función para cambiar a Register
function showRegister() {
    registerForm.classList.add('active');
    loginForm.classList.remove('active');
    tabRegister.classList.add('active');
    tabLogin.classList.remove('active');
    tabIndicator.classList.add('move-right');
}

// Event listeners de tabs
tabLogin.addEventListener('click', showLogin);
tabRegister.addEventListener('click', showRegister);

// Indicador de fortaleza de contraseña
const registerPassword = document.getElementById('register-password');
const strengthBar = document.querySelector('.strength-bar');

if (registerPassword) {
    registerPassword.addEventListener('input', (e) => {
        const password = e.target.value;
        const length = password.length;
        
        // Limpiar clases
        strengthBar.classList.remove('weak', 'medium', 'strong');
        
        if (length === 0) {
            strengthBar.style.width = '0%';
        } else if (length < 6) {
            strengthBar.classList.add('weak');
        } else if (length < 10) {
            strengthBar.classList.add('medium');
        } else {
            strengthBar.classList.add('strong');
        }
    });
}

// Validación visual de inputs
const allInputs = document.querySelectorAll('input');

allInputs.forEach(input => {
    input.addEventListener('blur', (e) => {
        if (e.target.value.length > 0 && !e.target.checkValidity()) {
            e.target.style.borderColor = '#ef4444';
        }
    });
    
    input.addEventListener('input', (e) => {
        if (e.target.checkValidity()) {
            e.target.style.borderColor = '';
        }
    });
});

// Animación suave al hacer scroll (si la página crece)
document.addEventListener('DOMContentLoaded', () => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });
    
    // Observar elementos con animación
    const animatedElements = document.querySelectorAll('.feature-item, .auth-container');
    animatedElements.forEach(el => observer.observe(el));
});