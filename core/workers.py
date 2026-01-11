import requests
from PyQt6.QtCore import QThread, pyqtSignal
from yt_dlp import YoutubeDL

class VideoInfoWorker(QThread):
    data_loaded = pyqtSignal(dict) 
    error_occurred = pyqtSignal(str)
    status_updated = pyqtSignal(str) # <--- NEW SIGNAL for live feedback

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            self.status_updated.emit("Connecting to YouTube API...") # <--- Feedback 1

            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,
                'extract_flat': False,
                'socket_timeout': 10,
                'geolocation_bypass': True,
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                # Info extraction
                info = ydl.extract_info(self.url, download=False)
                
                self.status_updated.emit("Parsing video formats...") # <--- Feedback 2
                
                unique_heights = set()
                if 'formats' in info:
                    for f in info['formats']:
                        if f.get('vcodec') != 'none' and f.get('height'):
                            unique_heights.add(f['height'])
                
                sorted_heights = sorted(list(unique_heights), reverse=True)

                display_formats = []
                if not sorted_heights:
                    display_formats.append("Best Quality")
                else:
                    for h in sorted_heights:
                        display_formats.append(f"{h}p")
                        display_formats.append(f"{h}p (Video Only)")

                display_formats.append("Audio Only (MP3)")

                # --- Thumbnail ---
                thumb_url = info.get('thumbnail')
                if info.get('thumbnails'):
                    thumb_url = info['thumbnails'][-1].get('url', thumb_url)

                thumb_data = None
                if thumb_url:
                    self.status_updated.emit("Downloading thumbnail...") # <--- Feedback 3
                    try:
                        headers = {'User-Agent': 'Mozilla/5.0'}
                        response = requests.get(thumb_url, headers=headers, timeout=3, stream=True)
                        if response.status_code == 200:
                            thumb_data = response.content
                    except Exception:
                        pass 

                self.status_updated.emit("Finalizing data...") # <--- Feedback 4

                result = {
                    'title': info.get('title', 'Unknown Title'),
                    'formats': display_formats,
                    'thumbnail_bytes': thumb_data,
                    'url': self.url
                }
                self.data_loaded.emit(result)

        except Exception as e:
            print(f"DEBUG ERROR: {str(e)}") 
            self.error_occurred.emit(str(e))