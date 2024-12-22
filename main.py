import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime

# Función para conectar a la base de datos y crear las tablas si no existen
def conectar_db():
    conn = sqlite3.connect("presupuestos.db")
    cursor = conn.cursor()

    # Crear tabla transacciones si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS transacciones (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tipo TEXT NOT NULL,
                        cantidad REAL NOT NULL,
                        categoria TEXT NOT NULL,
                        descripcion TEXT,
                        fecha TEXT,
                        nombre_usuario TEXT NOT NULL
                    )''')
    conn.commit()
    return conn

# Agregar una transacción (ingreso o gasto)
def agregar_transaccion(conn, tipo, cantidad, categoria, descripcion, nombre_usuario):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Obtener la fecha actual
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transacciones (tipo, cantidad, categoria, descripcion, fecha, nombre_usuario) VALUES (?, ?, ?, ?, ?, ?)",
                   (tipo, cantidad, categoria, descripcion, fecha, nombre_usuario))
    conn.commit()

# Función para obtener el balance
def obtener_balance(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(CASE WHEN tipo = 'ingreso' THEN cantidad ELSE 0 END) FROM transacciones")
    ingresos = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(CASE WHEN tipo = 'gasto' THEN cantidad ELSE 0 END) FROM transacciones")
    gastos = cursor.fetchone()[0] or 0

    return ingresos - gastos

# Mostrar las últimas transacciones
def mostrar_ultimos_movimientos(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT tipo, cantidad, categoria, descripcion, fecha, nombre_usuario FROM transacciones ORDER BY id DESC LIMIT 5")
    return cursor.fetchall()

# Función para actualizar la lista de transacciones en la interfaz
def mostrar_transacciones_gui(conn, listbox):
    transacciones = mostrar_ultimos_movimientos(conn)
    listbox.delete(0, tk.END)  # Limpiar la lista
    for transaccion in transacciones:
        listbox.insert(tk.END, f"{transaccion[0].capitalize()} - ${transaccion[1]:.2f} - Categoría: {transaccion[2]} - {transaccion[3]} - {transaccion[4]} - Usuario: {transaccion[5]}")

# Función para agregar ingresos
def agregar_ingreso(conn, listbox):
    agregar_transaccion_gui(conn, "ingreso", listbox)

# Función para agregar gastos
def agregar_gasto(conn, listbox):
    agregar_transaccion_gui(conn, "gasto", listbox)

# Función para agregar transacciones (ingreso o gasto)
def agregar_transaccion_gui(conn, tipo, listbox):
    ventana_transaccion = tk.Toplevel()
    ventana_transaccion.title(f"Agregar {tipo.capitalize()}")
    ventana_transaccion.geometry("400x450")  # Aumentar altura de la ventana
    ventana_transaccion.config(bg="#f4f4f9")

    # Título
    titulo = tk.Label(ventana_transaccion, text=f"Agregar {tipo.capitalize()}", font=("Arial", 16, "bold"), fg="#4CAF50", bg="#f4f4f9")
    titulo.pack(pady=15)

    # Nombre de quien hace el movimiento
    label_nombre = tk.Label(ventana_transaccion, text="Nombre del Usuario:", font=("Arial", 12), fg="#333", bg="#f4f4f9")
    label_nombre.pack(pady=5)
    entry_nombre = tk.Entry(ventana_transaccion, font=("Arial", 12), width=30)
    entry_nombre.pack(pady=5)

    # Cantidad
    label_cantidad = tk.Label(ventana_transaccion, text="Cantidad:", font=("Arial", 12), fg="#333", bg="#f4f4f9")
    label_cantidad.pack(pady=5)
    entry_cantidad = tk.Entry(ventana_transaccion, font=("Arial", 12), width=30)
    entry_cantidad.pack(pady=5)

    # Categoría
    label_categoria = tk.Label(ventana_transaccion, text="Categoría:", font=("Arial", 12), fg="#333", bg="#f4f4f9")
    label_categoria.pack(pady=5)
    entry_categoria = tk.Entry(ventana_transaccion, font=("Arial", 12), width=30)
    entry_categoria.pack(pady=5)

    # Descripción (opcional)
    label_descripcion = tk.Label(ventana_transaccion, text="Descripción (opcional):", font=("Arial", 12), fg="#333", bg="#f4f4f9")
    label_descripcion.pack(pady=5)
    entry_descripcion = tk.Entry(ventana_transaccion, font=("Arial", 12), width=30)
    entry_descripcion.pack(pady=5)

    # Función para agregar la transacción
    def agregar():
        nombre = entry_nombre.get().strip()
        cantidad = entry_cantidad.get().strip()
        categoria = entry_categoria.get().strip()
        descripcion = entry_descripcion.get().strip()

        if not nombre:
            messagebox.showerror("Error", "El nombre del usuario es obligatorio.")
            return

        if not cantidad.replace(".", "", 1).isdigit() or float(cantidad) <= 0:
            messagebox.showerror("Error", "La cantidad debe ser un número mayor a cero.")
            return

        # Agregar la transacción en la base de datos
        agregar_transaccion(conn, tipo, float(cantidad), categoria, descripcion, nombre)
        messagebox.showinfo("Éxito", f"{tipo.capitalize()} agregado con éxito.")
        ventana_transaccion.destroy()

        # Actualizar la lista de transacciones en tiempo real
        mostrar_transacciones_gui(conn, listbox)

    # Botón de agregar
    button_agregar = tk.Button(ventana_transaccion, text=f"Agregar {tipo.capitalize()}", font=("Arial", 12), fg="white", bg="#4CAF50", command=agregar)
    button_agregar.pack(pady=10)

    # Botón de cancelar
    button_cancelar = tk.Button(ventana_transaccion, text="Cancelar", font=("Arial", 12), fg="white", bg="#FF6347", command=ventana_transaccion.destroy)
    button_cancelar.pack(pady=10)

# Función para ver el balance
def ver_balance(conn, label_balance):
    balance = obtener_balance(conn)
    if balance < 0:
        label_balance.config(text=f"Balance: ${balance:.2f}", fg="red")
    else:
        label_balance.config(text=f"Balance: ${balance:.2f}", fg="#4CAF50")

# Función para actualizar el balance automáticamente
def actualizar_balance_periodicamente(conn, label_balance):
    ver_balance(conn, label_balance)
    label_balance.after(1000, actualizar_balance_periodicamente, conn, label_balance)  # Llama a esta función cada 5 segundos

# Función para mostrar todas las transacciones
def ver_todas_transacciones(conn, listbox):
    cursor = conn.cursor()
    cursor.execute("SELECT tipo, cantidad, categoria, descripcion, fecha, nombre_usuario FROM transacciones")
    transacciones = cursor.fetchall()
    listbox.delete(0, tk.END)
    for transaccion in transacciones:
        listbox.insert(tk.END, f"{transaccion[0].capitalize()} - ${transaccion[1]:.2f} - Categoría: {transaccion[2]} - {transaccion[3]} - {transaccion[4]} - Usuario: {transaccion[5]}")

# Función para filtrar por categoría
def filtrar_por_categoria(conn, listbox):
    categoria = simpledialog.askstring("Filtrar por categoría", "Ingrese la categoría para filtrar:")
    if categoria:
        cursor = conn.cursor()
        cursor.execute("SELECT tipo, cantidad, categoria, descripcion, fecha, nombre_usuario FROM transacciones WHERE categoria=?", (categoria,))
        transacciones = cursor.fetchall()
        listbox.delete(0, tk.END)
        for transaccion in transacciones:
            listbox.insert(tk.END, f"{transaccion[0].capitalize()} - ${transaccion[1]:.2f} - Categoría: {transaccion[2]} - {transaccion[3]} - {transaccion[4]} - Usuario: {transaccion[5]}")

# Configurar ventana principal
def main():
    # Conectar a la base de datos
    conn = conectar_db()

    # Crear la ventana principal
    root = tk.Tk()
    root.title("MONEY CONTROL by NOCTAMBULO")
    root.geometry("600x650")  # Aumentar tamaño de la ventana
    root.config(bg="#f4f4f9")

    # Título de la ventana
    titulo = tk.Label(root, text="Gestor de Presupuestos", font=("Arial", 20, "bold"), fg="#4CAF50", bg="#f4f4f9")
    titulo.pack(pady=20)

    # Crear el listado de transacciones
    listbox = tk.Listbox(root, width=70, height=10, font=("Arial", 12), bg="#ffffff", fg="#333", selectmode=tk.SINGLE)
    listbox.pack(pady=20)

    # Botón de agregar ingreso
    button_ingreso = tk.Button(root, text="Agregar Ingreso", font=("Arial", 12), fg="white", bg="#4CAF50", command=lambda: agregar_ingreso(conn, listbox))
    button_ingreso.pack(pady=10)

    # Botón de agregar gasto
    button_gasto = tk.Button(root, text="Agregar Gasto", font=("Arial", 12), fg="white", bg="#FF6347", command=lambda: agregar_gasto(conn, listbox))
    button_gasto.pack(pady=10)

    # Mostrar balance
    label_balance = tk.Label(root, text="Balance: $0.00", font=("Arial", 14), fg="#4CAF50", bg="#f4f4f9")
    label_balance.pack(pady=10)

    # Actualizar balance automáticamente
    actualizar_balance_periodicamente(conn, label_balance)

    # Botón para ver todas las transacciones
    button_ver_todas = tk.Button(root, text="Ver Todas las Transacciones", font=("Arial", 12), fg="white", bg="#4CAF50", command=lambda: ver_todas_transacciones(conn, listbox))
    button_ver_todas.pack(pady=10)

    # Botón para filtrar por categoría
    button_filtrar = tk.Button(root, text="Filtrar por Categoría", font=("Arial", 12), fg="white", bg="#4CAF50", command=lambda: filtrar_por_categoria(conn, listbox))
    button_filtrar.pack(pady=10)

    # Mostrar las transacciones iniciales
    mostrar_transacciones_gui(conn, listbox)

    # Iniciar la interfaz gráfica
    root.mainloop()

if __name__ == "__main__":
    main()
