from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Inicializar la base de datos SQLite para VaultApp
def init_db():
    conn = sqlite3.connect('vault.db')
    cursor = conn.cursor()
    # Guardamos únicamente el título y el ciphertext (texto cifrado)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vaults (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            ciphertext TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/api/guardar', methods=['POST'])
def guardar_vault():
    data = request.json
    titulo = data.get('titulo', 'Sin título')
    ciphertext = data.get('ciphertext', '')

    if not ciphertext:
        return jsonify({"error": "No se recibió contenido cifrado"}), 400

    conn = sqlite3.connect('vault.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO vaults (titulo, ciphertext) VALUES (?, ?)", (titulo, ciphertext))
    conn.commit()
    conn.close()

    return jsonify({"mensaje": "¡Dato cifrado guardado en el servidor de forma segura (Cero Conocimiento)!"}), 200

@app.route('/api/obtener', methods=['GET'])
def obtener_vaults():
    conn = sqlite3.connect('vault.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, ciphertext FROM vaults")
    rows = cursor.fetchall()
    conn.close()

    vaults = []
    for row in rows:
        vaults.append({
            "id": row[0],
            "titulo": row[1],
            "ciphertext": row[2]
        })

    return jsonify(vaults), 200

if __name__ == '__main__':
    # Usaremos el puerto 5003 para esta nueva app
    app.run(port=5003, debug=True)