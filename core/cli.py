import sys
import os
import re
from yt_dlp import YoutubeDL

def cli_progress_hook(d):
    """
    Callback for CLI progress bar.
    Prints progress to the same line in the terminal using carriage return.
    """
    if d['status'] == 'downloading':
        try:
            p = d.get('_percent_str', '0%').replace('%','')
            # Clean ANSI colors
            p = re.sub(r'\x1b\[[0-9;]*m', '', p)
            progress = float(p)
        except:
            progress = 0
        
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        
        # Create visual bar: [======    ]
        bar_length = 30
        filled_length = int(bar_length * progress // 100)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        # \r allows overwriting the current line
        sys.stdout.write(f'\r⏳ Downloading: |{bar}| {progress:.1f}% | Speed: {speed} | ETA: {eta}')
        sys.stdout.flush()

    elif d['status'] == 'finished':
        sys.stdout.write('\n✅ Download complete! Processing...\n')

def run_cli_mode(url, audio_only=False, quality="1080"):
    """
    Main entry point for the CLI functionality.
    """
    print(f"🚀 Starting CLI Downloader")
    print(f"🔗 URL: {url}")
    print(f"🎧 Mode: {'Audio Only (MP3)' if audio_only else 'Video (MP4)'}")
    
    # Save to 'downloads' folder in the current directory
    save_path = os.path.join(os.getcwd(), 'downloads')
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # yt-dlp configuration
    ydl_opts = {
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'progress_hooks': [cli_progress_hook],
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        # Format selection logic
        'format': 'bestaudio/best' if audio_only else f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]/best',
        'http_headers': {'User-Agent': 'Mozilla/5.0'},
    }

    # FFmpeg Post-processing for Audio
    if audio_only:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        # Merge video+audio into mp4
        ydl_opts['merge_output_format'] = 'mp4'

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"🎉 Saved to: {save_path}")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")