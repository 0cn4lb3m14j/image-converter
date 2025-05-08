# Image to WebP Converter

A free web-based tool that converts images to WebP format while reducing file size by approximately 30%.

## Features

- Converts various image formats (PNG, JPEG, etc.) to WebP
- Reduces file size by ~30%
- Simple and intuitive web interface
- Free to use
- Accessible from any network
- No file size limits (up to 32MB per file)

## Setup

### Local Setup
1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```

### Free Hosting Setup (Recommended)
1. Create a free account on [Render.com](https://render.com)
2. Fork this repository to your GitHub account
3. In Render.com:
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository
   - Select the repository
   - Use these settings:
     - Name: image-converter (or your preferred name)
     - Environment: Python
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
   - Click "Create Web Service"

Your app will be available at `https://your-app-name.onrender.com`

## Accessing the Converter

### Local Access
- Open your browser and go to `http://localhost:5000`

### External Access (Other Networks)
1. Find your computer's IP address:
   - Windows: Open CMD and type `ipconfig`
   - Linux/Mac: Open terminal and type `ifconfig` or `ip addr`
2. Share the URL with others using your IP address:
   - Example: `http://192.168.1.100:5000`
   - Replace with your actual IP address

Note: Make sure your firewall allows incoming connections on port 5000

## Usage

1. Click "Choose Image" to select an image file
2. Click "Convert to WebP" to start the conversion
3. The converted file will be automatically downloaded

## Technical Details

- Built with Flask and Pillow
- Uses WebP format for optimal compression
- Handles transparent PNGs by converting to white background
- Maximum file size: 32MB
- CORS enabled for cross-origin requests
- Deployed with Gunicorn for production use

## License

This project is open source and free to use. 
