from flask import Flask, render_template, request, send_file, url_for
from PIL import Image
import io
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'temp'

# Ensure temp directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def convert_to_webp(image_data, quality=70):
    """Convert image to WebP format with 30% size reduction"""
    img = Image.open(io.BytesIO(image_data))
    
    # Convert to RGB if image is in RGBA mode
    if img.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background
    
    output = io.BytesIO()
    img.save(output, format='WEBP', quality=quality)
    output.seek(0)
    return output

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400
    
    if file:
        filename = secure_filename(file.filename)
        file_data = file.read()
        
        # Convert to WebP
        webp_data = convert_to_webp(file_data)
        
        # Generate output filename
        output_filename = os.path.splitext(filename)[0] + '.webp'
        
        return send_file(
            webp_data,
            mimetype='image/webp',
            as_attachment=True,
            download_name=output_filename
        )

if __name__ == '__main__':
    # Run on all network interfaces (0.0.0.0) and port 5000
    app.run(host='0.0.0.0', port=5000, debug=False) 