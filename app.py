import os
from dotenv import load_dotenv
 
from flask import Flask, jsonify, request, render_template
import tracker
 

load_dotenv()

app = Flask(__name__)  # Crea una instancia de la aplicación Flask

api_key = os.environ.get("API_KEY")
print(f"API Key: {api_key}")

# Ruta para el aplicativo principal
@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/track', methods=['POST'])
def track():
    if not request.headers.get('x-api-key') == api_key:   
        return jsonify({"status": "error", "message": "Invalid API key"}), 403

    try:
        data = request.get_json()
        tracking_number = data['trackingNumber']
        details = tracker.track_package(tracking_number)
        return jsonify({"status": "success", "details": details})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
