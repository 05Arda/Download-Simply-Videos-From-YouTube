import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QComboBox, QHeaderView, QMessageBox, QAbstractItemView, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QTimer
from PyQt6.QtGui import QPixmap, QIcon
from core.workers import VideoInfoWorker
from core.downloader import DownloadWorker

# --- MAIN WINDOW ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart YouTube Downloader")
        self.setGeometry(100, 100, 950, 650)
        
        self.current_video_data = None 
        self.video_cache = {} # Key: URL, Value: dict
        
        self.active_downloader = None
        
        # Debounce Timer
        self.fetch_timer = QTimer()
        self.fetch_timer.setSingleShot(True)
        self.fetch_timer.setInterval(500) 
        self.fetch_timer.timeout.connect(self.validate_and_fetch)

        self.setup_ui()

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # --- SECTION 1: Input Panel ---
        input_layout = QHBoxLayout()
        INPUT_HEIGHT = 40 

        # 1. URL Input
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste YouTube link here...")
        self.url_input.setFixedHeight(INPUT_HEIGHT)
        self.url_input.setStyleSheet(f"""
            QLineEdit {{
                padding-left: 10px; 
                font-size: 14px; 
                border: 1px solid #ccc; 
                border-radius: 4px;
            }}
        """)
        self.url_input.textChanged.connect(self.on_url_text_changed)
        
        # 2. Quality Selector
        self.quality_combo = QComboBox()
        self.quality_combo.setPlaceholderText("Waiting for URL...")
        self.quality_combo.setEnabled(False)
        self.quality_combo.setFixedWidth(180) # Widen slightly for longer text
        self.quality_combo.setFixedHeight(INPUT_HEIGHT)
        self.quality_combo.setStyleSheet(f"""
            QComboBox {{
                padding-left: 10px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }}
            QComboBox::drop-down {{ border: 0px; }}
        """)
        
        # 3. Add Button
        self.btn_add = QPushButton("Add to Queue")
        self.btn_add.setEnabled(False) 
        self.btn_add.setFixedWidth(120)
        self.btn_add.setFixedHeight(INPUT_HEIGHT)
        self.btn_add.setStyleSheet(f"""
            QPushButton {{
                background-color: #2196F3; color: white; font-weight: bold; border-radius: 4px; font-size: 13px;
            }}
            QPushButton:disabled {{ background-color: #90CAF9; }}
            QPushButton:hover {{ background-color: #1976D2; }}
        """)
        self.btn_add.clicked.connect(self.add_to_queue)

        input_layout.addWidget(self.url_input)
        input_layout.addWidget(self.quality_combo)
        input_layout.addWidget(self.btn_add)

        # --- SECTION 2: Info Label & Progress Bar ---
        info_layout = QVBoxLayout()
        
        self.info_label = QLabel("Ready")
        self.info_label.setStyleSheet("color: gray; font-style: italic;")
        
        self.fetch_progress = QProgressBar()
        self.fetch_progress.setRange(0, 0) # 0-0 aralığı "Sonsuz Döngü" (Marquee) animasyonu yapar
        self.fetch_progress.setFixedHeight(4) # Çok ince, zarif bir çizgi olsun
        self.fetch_progress.setTextVisible(False) # Üzerinde % yazmasın
        self.fetch_progress.hide() # Başlangıçta gizli
        self.fetch_progress.setStyleSheet("""
            QProgressBar {
                border: 0px;
                background-color: #f0f0f0;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
                border-radius: 2px;
            }
        """)

        info_layout.addWidget(self.info_label)
        info_layout.addWidget(self.fetch_progress)


        # --- SECTION 3: Queue Table ---
        self.queue_table = QTableWidget()
        self.queue_table.setColumnCount(4)
        self.queue_table.setHorizontalHeaderLabels(["Video Details", "Quality", "Status", "Progress"])
        self.queue_table.setIconSize(QSize(80, 45))
        self.queue_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        header = self.queue_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.queue_table.setColumnWidth(1, 150) # Widen quality column
        self.queue_table.setColumnWidth(3, 150)

        # --- SECTION 4: Bottom Controls ---
        bottom_layout = QHBoxLayout()
        self.btn_start = QPushButton("🚀 Start All Downloads")
        self.btn_start.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        self.btn_start.clicked.connect(lambda: self.process_queue(from_user=True))
     
        self.btn_delete = QPushButton("🗑️ Remove Selected")
        self.btn_delete.setStyleSheet("background-color: #F44336; color: white; padding: 10px;")
        self.btn_delete.clicked.connect(self.remove_selected)

        bottom_layout.addStretch()
        bottom_layout.addWidget(self.btn_delete)
        bottom_layout.addWidget(self.btn_start)

        self.main_layout.addLayout(input_layout)
        self.main_layout.addLayout(info_layout)
        self.main_layout.addWidget(self.queue_table)
        self.main_layout.addLayout(bottom_layout)

    def on_url_text_changed(self):
        self.fetch_timer.stop()
        if self.url_input.text().strip():
            self.fetch_timer.start()
        else:
            self.reset_input_ui()

    def validate_and_fetch(self):
        url = self.url_input.text().strip()
        
        if "youtube.com" not in url and "youtu.be" not in url:
            self.info_label.setText("⚠️ Invalid YouTube URL format")
            return

        if url in self.video_cache:
            print(f"DEBUG: Cache Hit for {url}")
            self.info_label.setText("⚡ Loaded from cache...")
            self.on_fetch_success(self.video_cache[url])
            return

        # UI Updates for Fetching State
        self.info_label.setText("⏳ Starting...")
        self.quality_combo.clear()
        self.quality_combo.setEnabled(False)
        self.btn_add.setEnabled(False)
        
        self.fetch_progress.show() 

        self.worker = VideoInfoWorker(url)
        self.worker.data_loaded.connect(self.on_fetch_success)
        self.worker.error_occurred.connect(self.on_fetch_error)
        
        self.worker.status_updated.connect(self.info_label.setText)
        
        self.worker.start()

    def on_fetch_success(self, data):
        self.current_video_data = data
        self.video_cache[data['url']] = data # Save to cache
        
        self.quality_combo.clear()
        self.quality_combo.addItems(data['formats'])
        self.quality_combo.setEnabled(True)
        self.btn_add.setEnabled(True)

        self.fetch_progress.hide()
        
        title = data['title']
        self.info_label.setText(f"✅ Found: {title[:60]}...")

    def on_fetch_error(self):
        self.fetch_progress.hide()
    
        self.info_label.setText("❌ Failed to fetch video info")

    def add_to_queue(self):
        # 1. Check if video data exists
        if not self.current_video_data:
            return

        # 2. Get the selected quality
        target_quality = self.quality_combo.currentText()

        # --- VALIDATION FIX ---
        # Eğer kalite seçili değilse veya metin boşsa durdur.
        if not target_quality or not target_quality.strip():
            QMessageBox.warning(self, "Selection Missing", "Please select a quality option from the list!")
            return
        # ----------------------

        target_url = self.current_video_data['url']

        # --- DUPLICATE CHECK ---
        for row in range(self.queue_table.rowCount()):
            item = self.queue_table.item(row, 0)
            existing_url = item.data(Qt.ItemDataRole.UserRole)
            existing_quality = self.queue_table.item(row, 1).text()

            if existing_url == target_url and existing_quality == target_quality:
                QMessageBox.warning(self, "Duplicate Warning", 
                                    "This video with the same quality is already in the queue!")
                return

        row = self.queue_table.rowCount()
        self.queue_table.insertRow(row)

        # --- COLUMN 0: Video Title (EDITABLE) ---
        item_title = QTableWidgetItem(self.current_video_data['title'])
        # Store hidden URL for backend logic
        item_title.setData(Qt.ItemDataRole.UserRole, target_url) 
        
        # Add Thumbnail
        if self.current_video_data['thumbnail_bytes']:
            pixmap = QPixmap()
            pixmap.loadFromData(self.current_video_data['thumbnail_bytes'])
            item_title.setIcon(QIcon(pixmap))
        
        # Flags: Selectable + Enabled + EDITABLE
        item_title.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable)
        self.queue_table.setItem(row, 0, item_title)


        # --- COLUMN 1: Quality (READ-ONLY) ---
        item_quality = QTableWidgetItem(target_quality)
        item_quality.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        self.queue_table.setItem(row, 1, item_quality)


        # --- COLUMN 2: Status (READ-ONLY) ---
        item_status = QTableWidgetItem("Pending")
        item_status.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable)
        self.queue_table.setItem(row, 2, item_status)


        # --- COLUMN 3: Progress (READ-ONLY) ---
        item_progress = QTableWidgetItem("0%")
        item_progress.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        self.queue_table.setItem(row, 3, item_progress)

        # Reset UI Input Area
        self.url_input.clear()
        self.reset_input_ui()

    def reset_input_ui(self):
        self.quality_combo.clear()
        self.quality_combo.setEnabled(False)
        self.quality_combo.setPlaceholderText("Waiting for URL...")
        self.btn_add.setEnabled(False)
        self.info_label.setText("Ready")
        self.current_video_data = None

    def remove_selected(self):
        row = self.queue_table.currentRow()
        if row >= 0:
            self.queue_table.removeRow(row)
    


  # ------------------------------------------------------------------------
    # QUEUE MANAGEMENT LOGIC (CHAIN REACTION SYSTEM)
    # ------------------------------------------------------------------------

    def process_queue(self, from_user=False):
        """
        Manages the download queue.
        Args:
            from_user (bool): True if triggered by the 'Start' button, 
                              False if triggered automatically by the system.
        """
        # 1. Check if already downloading
        if self.active_downloader is not None:
            if from_user:
                QMessageBox.warning(self, "Busy", "A download is already in progress.")
            else:
                print("DEBUG: System tried to start, but worker is busy.")
            return

        # 2. Check if table is completely empty
        if self.queue_table.rowCount() == 0:
            if from_user:
                QMessageBox.warning(self, "Empty Queue", "Please add videos to the list first!")
            return

        # 3. Scan for Pending tasks
        for row in range(self.queue_table.rowCount()):
            status_item = self.queue_table.item(row, 2)
            
            if status_item.text() == "Pending":
                # Extract Data
                url_item = self.queue_table.item(row, 0)
                url = url_item.data(Qt.ItemDataRole.UserRole)
                quality = self.queue_table.item(row, 1).text()
                
                # Directory
                save_path = os.path.join(os.getcwd(), 'downloads')
                if not os.path.exists(save_path):
                    os.makedirs(save_path)

                # Start Worker
                self.start_download_worker(url, quality, save_path, row)
                return # Exit loop, worker started.

        # 4. If we reach here, NO "Pending" items were found.
        
        if from_user:
            # User clicked start, but everything is already finished or error
            QMessageBox.information(self, "Info", "No pending tasks found in the queue.")
        else:
            # System finished the last task (Chain reaction ended)
            # This is the "End of Batch" message.
            QMessageBox.information(self, "Queue Finished", "Queue processing is complete.\nCheck statuses for any errors.")


    def start_download_worker(self, url, quality, path, row_index):
        """Prepares the Worker thread, connects signals, and starts execution."""
        
        # Update UI Status
        self.queue_table.item(row_index, 2).setText("⏳ Downloading...")
        
        # Create the Worker Instance
        self.active_downloader = DownloadWorker(url, quality, path)
        
        # Connect Signals using Lambda to pass 'row_index' context
        self.active_downloader.progress_updated.connect(
            lambda status, prog: self.update_row_progress(row_index, status, prog)
        )
        self.active_downloader.finished.connect(
            lambda: self.on_download_finished(row_index)
        )
        self.active_downloader.error_occurred.connect(
            lambda err: self.on_download_error(row_index, err)
        )
        
        # Start the Thread
        self.active_downloader.start()

    def update_row_progress(self, row, status_text, progress_percent):
        self.queue_table.item(row, 3).setText(f"{progress_percent}%")
        self.queue_table.item(row, 2).setText(status_text)

    def on_download_finished(self, row):
        """Triggered when a download completes successfully."""
        self.queue_table.item(row, 2).setText("Completed ✅")
        self.queue_table.item(row, 3).setText("100%")
        self.active_downloader = None
        
        # RECURSION: Check next item (Not from user)
        self.process_queue(from_user=False)

    def on_download_error(self, row, error_msg):
        """Triggered if the download fails."""
        self.queue_table.item(row, 2).setText("Error ❌")
        
        # İsteğe bağlı: Hata mesajını popup olarak göstermek yerine
        # sadece duruma yazabiliriz, böylece akış kesilmez.
        # Ama şimdilik popup kalsın.
        QMessageBox.critical(self, "Download Error", f"An error occurred at row {row+1}:\n{error_msg}")
        
        self.active_downloader = None
        
        # RECURSION: Check next item even if this one failed
        self.process_queue(from_user=False)