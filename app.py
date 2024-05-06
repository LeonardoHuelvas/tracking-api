from flask import Flask, jsonify, request, render_template
import tracker

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/track', methods=['POST'])
def track():
    try:
        data = request.get_json()
        tracking_number = data['trackingNumber']
        details = tracker.track_package(tracking_number)
        return jsonify({"status": "success", "details": details})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
