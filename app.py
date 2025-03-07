from flask import Flask, request, jsonify, send_file, render_template
import yt_dlp
import os
import subprocess
import sys

app = Flask(__name__)

# Configuration
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Check if FFmpeg is installed
def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

if not check_ffmpeg():
    print("ERROR: FFmpeg is not installed or not in PATH. Please install FFmpeg.")
    print("You can download it from: https://ffmpeg.org/download.html")
    print("Or install it using: winget install FFmpeg")
    sys.exit(1)

def download_youtube_to_mp3(url, output_path):
    try:
        # yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'quiet': True,
            'noplaylist': True,
            'ffmpeg_location': r'C:\path\to\bin\ffmpeg.exe',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
            return filename
    except Exception as e:
        raise Exception(f"Error downloading: {str(e)}")

# Web UI - Home Page
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# API Endpoint for Conversion
@app.route('/convert', methods=['POST'])
def convert_to_mp3():
    try:
        youtube_url = request.form.get('youtube_url')
        if not youtube_url:
            return render_template('index.html', error="Please provide a YouTube URL")

        # Download and convert
        file_path = download_youtube_to_mp3(youtube_url, DOWNLOAD_FOLDER)
        
        # Instead of sending file, return success message
        return render_template('index.html', success=f"Successfully downloaded! Check the downloads folder: {DOWNLOAD_FOLDER}")
        
    except Exception as e:
        return render_template('index.html', error=str(e))
        if request.content_type == 'application/json':
            return jsonify({'error': str(e)}), 500
        return render_template('index.html', error=str(e))

# Health Check Endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)