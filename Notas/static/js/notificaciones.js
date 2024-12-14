// static/js/notificaciones.js

function mostrarNotificacion(mensaje, tipo = 'success') {
    const notificationContainer = document.getElementById("notification-container");

    // Crear el elemento de la notificación
    const notification = document.createElement('div');
    notification.classList.add('notification');
    notification.style.backgroundColor = tipo === 'success' ? '#28a745' : tipo === 'warning' ? '#fd7e14' : '#dc3545';
    notification.style.color = '#fff';
    notification.style.padding = '10px 20px';
    notification.style.margin = '10px';
    notification.style.borderRadius = '5px';
    notification.style.fontSize = '16px';
    notification.style.display = 'inline-block';
    notification.style.transition = 'opacity 0.5s';

    // Añadir el mensaje
    notification.innerHTML = mensaje;

    // Agregar la notificación al contenedor
    notificationContainer.appendChild(notification);

    // Desaparecer la notificación después de 5 segundos
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            notificationContainer.removeChild(notification);
        }, 500); // Tiempo para que desaparezca completamente
    }, 5000); // Tiempo antes de que se empiece a desvanecer (en ms)
}

function evaluarPromedio(promedio) {
    let mensaje = '';
    let tipo = ''; // 'success' para aprobado, 'warning' para en peligro, 'error' para desaprobado

    // Lógica para determinar el estado del alumno basado en su promedio
    if (promedio >= 12.5) {
        mensaje = "¡Felicidades! Has aprobado el curso.";
        tipo = 'success';  // Verde
    } else if (promedio >= 11 && promedio < 12.5) {
        mensaje = "Estás en peligro, tu rendimiento es regular. ¡Esfuérzate!";
        tipo = 'warning';  // Naranja
    } else {
        mensaje = "¡Desaprobado! Necesitas mejorar tus notas.";
        tipo = 'error';  // Rojo
    }

    // Mostrar la notificación con el mensaje y tipo correspondiente
    mostrarNotificacion(mensaje, tipo);
}

// Ejemplo de uso:
