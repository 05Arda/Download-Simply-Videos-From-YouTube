📥 SmartYTDL - Advanced YouTube Downloader

SmartYTDL is a powerful, modular, and user-friendly YouTube downloader built with Python and PyQt6.

Originally based on a simple script, this project has been completely refactored into a professional engineering project featuring a modern Graphical User Interface (GUI) with a queue management system, as well as a robust Command Line Interface (CLI).

✨ Key Features

🖥️ Graphical User Interface (GUI)

Smart Queue System: Add multiple videos to a list and download them sequentially automatically.

Drag & Drop Sorting: Easily reorder your download queue by dragging rows (enabled when idle).

Live Fetching & Caching: Automatically fetches video titles, thumbnails, and available formats. Caches data to prevent redundant network requests.

Advanced Format Selection:

Standard: Video + Audio (1080p, 720p, etc.)

Video Only: Download video stream only (silent).

Audio Only: Extract high-quality MP3.

Visual Feedback: Indeterminate progress bars for fetching and detailed progress bars for downloading.

Safety Locks: Prevents invalid inputs and locks critical UI elements during processing to prevent errors.

💻 Command Line Interface (CLI)

Instant Access: Run ytdownload from anywhere in your terminal.

Headless Operation: Download videos without opening the window.

Utility Tools: Includes a built-in cleaner to wipe the downloads folder.

⚙️ Prerequisites

Python 3.10 or higher.

FFmpeg: Essential for merging video and audio streams.

Windows: Download ffmpeg.exe and place it in the project folder or add it to System PATH.

macOS: brew install ffmpeg

Linux: sudo apt install ffmpeg

📦 Installation

Follow these steps to set up the project in Developer Mode:

Clone the Repository:

git clone [https://github.com/YOUR_USERNAME/SmartYTDL.git](https://github.com/YOUR_USERNAME/SmartYTDL.git)
cd SmartYTDL

Install Dependencies & The App:
This command installs required libraries (PyQt6, yt-dlp) and links the ytdownload command to your system.

pip install -e .

🚀 Usage

You can use SmartYTDL in two modes:

1. GUI Mode (Visual Interface)

Simply type the command in your terminal:

ytdownload

Step 1: Paste a YouTube link.

Step 2: Wait for the auto-fetch to show the title and thumbnail.

Step 3: Select quality and click "Add to Queue".

Step 4: Repeat for other videos, then click "🚀 Start All Downloads".

2. CLI Mode (Terminal)

Download directly from the command line without opening the interface:

Download Best Quality (Video+Audio):

ytdownload [https://www.youtube.com/watch?v=VIDEO_ID](https://www.youtube.com/watch?v=VIDEO_ID)

Download Audio Only (MP3):

ytdownload [https://www.youtube.com/watch?v=VIDEO_ID](https://www.youtube.com/watch?v=VIDEO_ID) -a

Download Specific Quality (e.g., 4K/2160p):

ytdownload [https://www.youtube.com/watch?v=VIDEO_ID](https://www.youtube.com/watch?v=VIDEO_ID) -q 2160

Clear Downloads Folder:

ytdownload --clear

🏗️ Project Architecture

This project follows a modular Object-Oriented architecture, separating concerns for maintainability and scalability:

SmartYTDL/
│
├── core/ # Backend Logic
│ ├── downloader.py # Background worker for downloading (Threading)
│ ├── workers.py # Background worker for fetching metadata
│ ├── cli.py # Logic for Command Line Interface
│ └── cleaner.py # Utility for file management
│
├── ui/ # Frontend Logic
│ └── main_window.py # PyQt6 Layouts, Signals, and Slots
│
├── downloads/ # Default download directory
├── main.py # Application Router (Entry Point)
└── setup.py # Installation script

🤝 Contributing & Credits

This project is a heavily engineered fork based on the original script by Pierre-Henry Soria.

Major improvements in this fork:

Migrated from single-script to Modular Package Architecture.

Implemented PyQt6 GUI with multithreading.

Added Queue Management System.

Integrated Caching and Drag & Drop features.

Feel free to fork and submit Pull Requests!

⚖️ License

Distributed under the MIT License. See LICENSE for more information.

Developed with ❤️ using Python & PyQt6
