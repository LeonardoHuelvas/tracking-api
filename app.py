import os
from flask import Flask, jsonify, request, render_template
import tracker

app = Flask(__name__)

# Ruta para la página principal
@app.route('/')
def index():
    """
    Renderiza la plantilla 'index.html' como la página principal.

    Retorna:
    str: Contenido HTML de la página principal.
    """
    return render_template('index.html')

# Ruta para rastrear el paquete
@app.route('/track', methods=['POST'])
def track():
    """
    Maneja la solicitud de rastreo de paquetes.

    Retorna:
    str: Respuesta JSON que indica el estado del rastreo y los detalles del paquete.
    """
    # Verificar la clave de la API
    api_key = os.environ.get("API_KEY")
    if not request.headers.get('x-api-key') == api_key:   
        return jsonify({"status": "error", "message": "Invalid API key"}), 403

    try:
        # Obtener datos de la solicitud
        data = request.get_json()
        tracking_number = data['trackingNumber']
        
        # Rastrear el paquete usando la función en tracker
        details = tracker.track_package(tracking_number)

        return jsonify({"status": "success", "details": details})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
