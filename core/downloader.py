import re
import os
from PyQt6.QtCore import QThread, pyqtSignal
from yt_dlp import YoutubeDL

class DownloadWorker(QThread):
    """
    Handles the actual downloading process in a background thread.
    Communicates with the GUI via signals.
    """
    # Signals
    progress_updated = pyqtSignal(str, int) # status_text, progress_percentage
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, url, quality_option, output_path):
        super().__init__()
        self.url = url
        self.quality = quality_option  # e.g., "1080p", "720p (Video Only)", "Audio Only (MP3)"
        self.output_path = output_path
        self.is_running = True

    def run(self):
        try:
            # 1. Determine Format String based on user selection
            format_str = self._get_format_string()
            
            # 2. Configure yt-dlp options
            ydl_opts = {
                'format': format_str,
                'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self._progress_hook],
                'noplaylist': True,
                'ignoreerrors': False, # Stop on error so we can catch it
                'no_warnings': True,
                'quiet': True,
                # Safe headers to prevent HTTP 403
                'http_headers': {'User-Agent': 'Mozilla/5.0'},
            }

            # 3. Audio Conversion (if MP3 selected)
            if "Audio Only" in self.quality:
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]

            # 4. Start Download
            with YoutubeDL(ydl_opts) as ydl:
                if self.is_running:
                    ydl.download([self.url])
            
            self.finished.emit()

        except Exception as e:
            # Clean up error message
            error_msg = str(e).replace('\033[0;31mERROR:\033[0m ', '')
            self.error_occurred.emit(error_msg)

    def stop(self):
        """Request the thread to stop."""
        self.is_running = False

    def _get_format_string(self):
        """Parses the quality selection string into yt-dlp format codes."""
        
        # Case 1: Audio Only
        if "Audio Only" in self.quality:
            return 'bestaudio/best'
        
        # Extract the resolution number (e.g., "1080" from "1080p")
        try:
            height = ''.join(filter(str.isdigit, self.quality))
            if not height: 
                return 'best' # Fallback
        except:
            return 'best'

        # Case 2: Video Only (Silent)
        if "Video Only" in self.quality:
            # Download best video matching height, no audio
            return f'bestvideo[height<={height}]'
        
        # Case 3: Normal Video (Video + Audio)
        # Download best video matching height + best audio, and merge them
        return f'bestvideo[height<={height}]+bestaudio/best[height<={height}]'



    def _progress_hook(self, d):
        """Callback function called by yt-dlp during download."""
        if not self.is_running:
            raise Exception("Download cancelled by user")

        if d['status'] == 'downloading':
            # --- METHOD 1: Mathematical Calculation (Most Reliable) ---
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes', 0)
            
            progress = 0
            if total_bytes:
                progress = int((downloaded_bytes / total_bytes) * 100)
            else:
                # --- METHOD 2: String Parsing with ANSI Cleanup ---
                try:
                    p = d.get('_percent_str', '0%')
                    
                    # Remove ANSI escape codes (e.g. \x1b[0;94m) using Regex
                    p = re.sub(r'\x1b\[[0-9;]*m', '', p)
                    
                    # Remove percent sign and whitespace
                    p = p.replace('%', '').strip()
                    
                    # Convert to integer
                    progress = float(p)
                except Exception as e:
                    print(f"Progress Parse Error: {e}") 
                    progress = 0
            
            # Clean up Speed and ETA strings as well
            speed = d.get('_speed_str', 'N/A')
            if isinstance(speed, str):
                speed = re.sub(r'\x1b\[[0-9;]*m', '', speed).strip()

            eta = d.get('_eta_str', 'N/A')
            if isinstance(eta, str):
                eta = re.sub(r'\x1b\[[0-9;]*m', '', eta).strip()
            
            status_msg = f"{speed} | ETA: {eta}"
            
            self.progress_updated.emit(status_msg, progress)

        elif d['status'] == 'finished':
            self.progress_updated.emit("Processing...", 100)