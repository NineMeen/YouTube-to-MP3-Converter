# YouTube to MP3 Converter

A simple Flask application that converts YouTube videos to MP3 files via a web interface or API. Users can paste a YouTube URL and download the audio as an MP3 file named after the video title.

## Features
- Web UI for easy URL input and MP3 download
- REST API endpoint for programmatic access
- Uses `yt-dlp` for YouTube downloading and `FFmpeg` for audio conversion
- Saves files with the original YouTube video title

## Prerequisites
- Python 3.6 or higher
- Windows (for `winget` usage; see alternatives for other OS below)

## Installation

### 1. Install Python Dependencies
Install the required Python packages using `pip`:

```bash
pip install flask yt_dlp
```
### 2. Install FFmpeg
FFmpeg is required for audio conversion. On Windows, use winget:
```bash
winget install FFmpeg
```
### 3. Verify FFmpeg Installation
Find FFmpeg on your system to ensure it’s installed correctly:
```bash
where FFmpeg
```
and set on `'ffmpeg_location': r'C:\path\to\bin\ffmpeg.exe'`


