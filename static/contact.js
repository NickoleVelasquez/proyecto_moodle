document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('contact-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Evita que se recargue la página

        // Muestra el mensaje de éxito
        document.getElementById('success-message').style.display = 'block';
        
        // Opcional: Limpiar los campos del formulario
        document.getElementById('contact-form').reset();
    });
});

