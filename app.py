from flask import Flask, request, render_template, send_file, jsonify
from PIL import Image
import io
import os
import zipfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max file size

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview', methods=['POST'])
def preview():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        img = Image.open(file.stream)
        return jsonify({
            'format': img.format,
            'width': img.width,
            'height': img.height,
            'mode': img.mode
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/convert', methods=['POST'])
def convert():
    if 'files' not in request.files:
        return 'No files provided', 400
    
    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return 'No files selected', 400
    
    # Get conversion options
    output_format = request.form.get('format', 'WEBP')
    quality = int(request.form.get('quality', 70))
    lossless = request.form.get('lossless') == 'on'
    
    # Create a ZIP file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file in files:
            if not allowed_file(file.filename):
                continue
            
            try:
                # Open and convert image
                img = Image.open(file.stream)
                
                # Preserve transparency if present
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    if output_format == 'WEBP':
                        # Convert to RGBA if needed
                        if img.mode != 'RGBA':
                            img = img.convert('RGBA')
                        output = io.BytesIO()
                        img.save(output, format='WEBP', quality=quality, lossless=lossless)
                    elif output_format == 'PNG':
                        output = io.BytesIO()
                        img.save(output, format='PNG', optimize=True)
                    else:  # JPEG doesn't support transparency
                        img = img.convert('RGB')
                        output = io.BytesIO()
                        img.save(output, format=output_format, quality=quality)
                else:
                    # No transparency, convert to RGB if needed
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    output = io.BytesIO()
                    img.save(output, format=output_format, quality=quality)
                
                output.seek(0)
                
                # Generate output filename
                filename = secure_filename(file.filename)
                name, ext = os.path.splitext(filename)
                output_filename = f"{name}.{output_format.lower()}"
                
                # Add to ZIP
                zip_file.writestr(output_filename, output.getvalue())
            
            except Exception as e:
                print(f"Error converting {file.filename}: {str(e)}")
                continue
    
    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='converted_images.zip'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False) 