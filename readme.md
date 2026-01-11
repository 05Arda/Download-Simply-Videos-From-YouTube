# 📥 SmartYTDL – Advanced YouTube Downloader

**SmartYTDL** is a powerful, modular, and user-friendly **YouTube downloader** built with **Python** and **PyQt6**.

Originally based on a simple script, this project has been **fully refactored into a professional engineering project**, featuring a modern **Graphical User Interface (GUI)**, a robust **Command Line Interface (CLI)**, and a smart **queue-based download system**.

---

## ✨ Key Features

### 🖥️ Graphical User Interface (GUI)

- **Smart Queue System**  
  Add multiple videos to a list and download them **sequentially** automatically.

- **Live Fetching & Caching**  
  Automatically fetches video titles, thumbnails, and available formats.  
  Cached data prevents redundant network requests.

- **Advanced Format Selection**
  - **Standard**: Video + Audio (1080p, 720p, etc.)
  - **Video Only**: Download video stream only (silent)
  - **Audio Only**: Extract high-quality MP3

- **Visual Feedback**
  - Indeterminate progress bars while fetching metadata
  - Detailed progress bars during downloading

- **Safety Locks**
  - Prevents invalid inputs
  - Locks critical UI elements during processing to prevent errors

---

### 💻 Command Line Interface (CLI)

- **Instant Access**  
  Run `ytdownload` from anywhere in your terminal.

- **Headless Operation**  
  Download videos without opening the GUI.

- **Utility Tools**
  - Built-in cleaner to wipe the downloads folder

---

## ⚙️ Prerequisites

- **Python 3.10 or higher**
- **FFmpeg** (required for merging video and audio streams)

### FFmpeg Installation

#### Windows
- Download `ffmpeg.exe`
- Place it in the project folder **or**
- Add it to your **System PATH**

#### macOS
```bash
brew install ffmpeg
```

#### Linux
```bash
sudo apt install ffmpeg
```

---

## 📦 Installation (Developer Mode)

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/SmartYTDL.git
cd SmartYTDL
```

### Install Dependencies & Application

This command installs required libraries (`PyQt6`, `yt-dlp`) and links the  
`ytdownload` command to your system.

```bash
pip install -e .
```

---

## 🚀 Usage

SmartYTDL can be used in **two modes**.

---

### 1️⃣ GUI Mode (Visual Interface)

Launch the GUI by running:

```bash
ytdownload
```

**Steps:**

1. Paste a YouTube link  
2. Wait for auto-fetch to display the title and thumbnail  
3. Select quality and click **Add to Queue**  
4. Repeat for other videos  
5. Click **🚀 Start All Downloads**

---

### 2️⃣ CLI Mode (Terminal)

Download videos directly from the command line without opening the interface.

#### Download Best Quality (Video + Audio)

```bash
ytdownload https://www.youtube.com/watch?v=VIDEO_ID
```

#### Download Audio Only (MP3)

```bash
ytdownload https://www.youtube.com/watch?v=VIDEO_ID -a
```

#### Download Specific Quality (e.g. 4K / 2160p)

```bash
ytdownload https://www.youtube.com/watch?v=VIDEO_ID -q 2160
```

#### Clear Downloads Folder

```bash
ytdownload --clear
```

---

## 🏗️ Project Architecture

SmartYTDL follows a **modular, Object-Oriented architecture**, separating concerns for maintainability and scalability.

```text
SmartYTDL/
│
├── core/                  # Backend Logic
│   ├── downloader.py      # Background worker for downloading (threading)
│   ├── workers.py         # Background workers for metadata fetching
│   ├── cli.py             # Command Line Interface logic
│   └── cleaner.py         # File management utilities
│
├── ui/                    # Frontend Logic
│   └── main_window.py     # PyQt6 layouts, signals, and slots
│
├── downloads/             # Default download directory
├── main.py                # Application router (entry point)
└── setup.py               # Installation and packaging script
```

---

## 🤝 Contributing & Credits

This project is a **heavily engineered fork** based on the original script by  
**Pierre-Henry Soria**.

### Major Improvements in This Fork

- Migrated from single-script to **modular package architecture**
- Implemented **PyQt6 GUI** with multithreading
- Added **Queue Management System**
- Integrated **Caching** feature
- Added full **CLI support**

Contributions are welcome.  
Feel free to fork the repository and submit Pull Requests.

---

## ⚖️ License

Distributed under the **MIT License**.  
See the `LICENSE` file for more information.

---

Developed with ❤️ using **Python & PyQt6**
