const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();

// Middleware para manejar JSON
app.use(express.json());

// Servir archivos estáticos desde la carpeta 'page'
app.use(express.static(path.join(__dirname, 'page')));

// Ruta para obtener todos los usuarios
app.get('/usuarios', (req, res) => {
  const users = JSON.parse(fs.readFileSync(path.join(__dirname, 'usuarios.json')));
  res.json(users);
});

// Ruta para agregar un nuevo usuario
app.post('/usuarios', (req, res) => {
  const { username, password } = req.body;
  const users = JSON.parse(fs.readFileSync(path.join(__dirname, 'usuarios.json')));

  // Verificar si el usuario ya existe
  if (users.some(user => user.username === username)) {
    return res.status(400).json({ message: 'El usuario ya existe' });
  }

  // Agregar el nuevo usuario
  users.push({ username, password });
  fs.writeFileSync(path.join(__dirname, 'usuarios.json'), JSON.stringify(users, null, 2));
  res.status(201).json({ message: 'Usuario creado exitosamente' });
});

// Ruta para eliminar un usuario
app.delete('/usuarios/:username', (req, res) => {
  const { username } = req.params;
  let users = JSON.parse(fs.readFileSync(path.join(__dirname, 'usuarios.json')));

  // Filtrar el usuario a eliminar
  users = users.filter(user => user.username !== username);

  // Si el usuario fue encontrado y eliminado
  fs.writeFileSync(path.join(__dirname, 'usuarios.json'), JSON.stringify(users, null, 2));
  res.status(200).json({ message: 'Usuario eliminado' });
});

// Ruta para la página de administración
app.get('/admin', (req, res) => {
  res.sendFile(path.join(__dirname, 'page', 'admin.html')); // Asegúrate de que la ruta sea correcta
});

// Iniciar el servidor
const port = 3000;
app.listen(port, () => {
  console.log(`Servidor corriendo en http://localhost:${port}`);
});
