import sys
import argparse
from PyQt6.QtWidgets import QApplication

# Import Modules
from ui.main_window import MainWindow
from core.cli import run_cli_mode
from core.cleaner import clear_downloads_folder

def main():
    """
    Entry point for the application.
    Parses arguments and decides whether to launch GUI, CLI, or Utility tools.
    """
    # --- 1. SETUP ARGUMENT PARSER ---
    parser = argparse.ArgumentParser(description="Smart YouTube Downloader (GUI & CLI)")
    
    # Positional Argument: URL
    parser.add_argument("url", nargs="?", help="The YouTube URL to download")
    
    # Optional Flags
    parser.add_argument("-a", "--audio", action="store_true", help="Download audio only (MP3)")
    parser.add_argument("-q", "--quality", default="1080", help="Max video height (e.g., 1080, 720). Default: 1080")
    
    # NEW ARGUMENT: Clear Downloads
    parser.add_argument("-c", "--clear", action="store_true", help="Delete all files in the downloads folder")
    
    args = parser.parse_args()

    # --- 2. DECISION LOGIC ---

    # Case 1: User wants to clear downloads
    if args.clear:
        clear_downloads_folder()
        sys.exit() # Exit after cleaning, don't open GUI

    # Case 2: CLI Mode (URL provided)
    elif args.url:
        run_cli_mode(args.url, args.audio, args.quality)
        
    # Case 3: GUI Mode (No arguments)
    else:
        # Check if QApplication already exists
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)
            
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()