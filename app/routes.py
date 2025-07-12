from app import app
from flask import render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image

UPLOAD_FOLDER = 'app/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'tiff', 'bmp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        text = ""
        try:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
                text = pytesseract.image_to_string(Image.open(filepath))
            else:
                text = "OCR for this file type is not supported yet."
        except Exception as e:
            return jsonify({'error': str(e)}), 500

        # AI-powered renaming
        new_filename = get_new_filename(text)

        # Rename the file
        base, extension = os.path.splitext(filename)
        renamed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename + extension)
        os.rename(filepath, renamed_filepath)


        return jsonify({'original_filename': filename, 'new_filename': new_filename + extension, 'ocr_text': text})

    return jsonify({'error': 'File type not allowed'}), 400

from functools import wraps
from flask import request, jsonify

API_KEY = "your-secret-api-key" # Should be in env

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == API_KEY:
            return f(*args, **kwargs)
        else:
            return jsonify({"message": "API key is missing or invalid."}), 401
    return decorated_function

@app.route('/api/rename', methods=['POST'])
@require_api_key
def api_rename():
    return upload_file()

import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_new_filename(text):
    if not openai.api_key or openai.api_key == "YOUR_OPENAI_API_KEY":
        # Fallback if API key is not set
        return f"renamed_{text[:20].replace(' ', '_')}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that renames files based on their content."},
                {"role": "user", "content": f"Based on the following text, suggest a concise and descriptive filename (without extension):\n\n{text}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        # Fallback on API error
        return f"renamed_{text[:20].replace(' ', '_')}"
