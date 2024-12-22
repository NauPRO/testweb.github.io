// Función para autenticar usuario desde el servidor
async function authenticate(username, password) {
    try {
        const response = await fetch("/usuarios"); // Asume que tu servidor expone la lista de usuarios en esta ruta
        if (!response.ok) throw new Error("No se pudo obtener la lista de usuarios");
        
        const users = await response.json();
        return users.some(user => user.username === username && user.password === password);
    } catch (error) {
        console.error("Error al autenticar el usuario:", error);
        return false;
    }
}

// Función para registrar un nuevo usuario en el servidor
async function registerUser(username, password) {
    try {
        const response = await fetch("/usuarios", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
        });
        if (!response.ok) throw new Error("Error al registrar usuario");
        
        return response.json(); // Retorna la respuesta del servidor
    } catch (error) {
        console.error("Error al registrar el usuario:", error);
    }
}

// Manejar el evento de envío del formulario
document.getElementById("loginForm").addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevenir el comportamiento por defecto de recargar la página

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Verificar si el usuario existe y la contraseña es correcta
    if (await authenticate(username, password)) {
        // Mensaje de éxito
        document.getElementById("error-message").style.color = "green";
        document.getElementById("error-message").textContent = "Inicio de sesión exitoso. Redirigiendo...";

        // Redirigir a la página principal después de 2 segundos
        setTimeout(() => {
            window.location.href = "home.html"; // Redirige a la página principal de la app
        }, 2000);
    } else {
        // Mostrar mensaje de error
        document.getElementById("error-message").textContent = "Usuario o contraseña incorrectos.";
    }
});

// Redirigir al usuario a la página de compra de usuario
function redirigirARegistro() {
    window.location.href = "comprar.html"; // Cambiar por la página de compra de usuarios
}
