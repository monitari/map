from flask import Flask, send_from_directory, jsonify, redirect, url_for
import subprocess
import os

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        result = subprocess.run(['python', 'generate_svg.py'], check=True, capture_output=True, text=True)
        return redirect(url_for('serve_map'))
    except subprocess.CalledProcessError as e:
        return e.stderr, 500

@app.route('/map')
def serve_map():
    return send_from_directory(os.getcwd(), 'vector_map.html')

@app.route('/data/<path:filename>')
def serve_static(filename):
    return send_from_directory('data', filename)

if __name__ == '__main__':
    app.run(debug=True)