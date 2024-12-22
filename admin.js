// Función para agregar un usuario al servidor
async function addUser(username, password) {
    const response = await fetch('/usuarios', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    });

    // Si el usuario fue creado exitosamente
    if (response.ok) {
        alert('Usuario creado exitosamente');
        loadUsers();  // Recargar la lista de usuarios
    } else {
        alert('Error al crear el usuario: ' + (await response.json()).message);
    }
}

// Función para cargar la lista de usuarios
async function loadUsers() {
    const response = await fetch('/usuarios');
    const users = await response.json();

    const tbody = document.querySelector('#userList tbody');
    tbody.innerHTML = '';  // Limpiar la lista actual

    // Agregar cada usuario a la tabla
    users.forEach(user => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${user.username}</td>
            <td><button onclick="deleteUser('${user.username}')">Eliminar</button></td>
        `;
        tbody.appendChild(tr);
    });
}

// Función para eliminar un usuario
async function deleteUser(username) {
    const response = await fetch(`/usuarios/${username}`, {
        method: 'DELETE',
    });

    if (response.ok) {
        alert('Usuario eliminado');
        loadUsers();  // Recargar la lista de usuarios
    } else {
        alert('Error al eliminar el usuario');
    }
}

// Manejar el evento de enviar el formulario para agregar un usuario
document.getElementById('userForm').addEventListener('submit', function (event) {
    event.preventDefault();  // Evitar que se recargue la página

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Agregar el nuevo usuario
    addUser(username, password);
});

// Cargar la lista de usuarios al cargar la página
loadUsers();
