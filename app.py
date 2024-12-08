from flask import Flask, render_template, request, redirect, url_for
import os
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# A simple in-memory store for messages (in a real-world app, you'd use a database)
messages = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@app.route('/submit_message', methods=['POST'])
def submit_message():
    message = request.form['message']
    if message:
        messages.append(message)
    return redirect(url_for('index'))

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        messages.append(f"New image uploaded: {filename}")
    return redirect(url_for('index'))

@app.route('/get_latest_message', methods=['GET'])
def get_latest_message():
    latest_message = messages[-1] if messages else "No messages yet"
    return latest_message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
