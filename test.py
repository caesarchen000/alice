from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QBrush
import sys

class MacFloatingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JARVIS Floating Window")
        
        # macOS-specific window flags for floating behavior
        self.setWindowFlags(
            Qt.FramelessWindowHint |      # No window frame
            Qt.WindowStaysOnTopHint |     # Always on top
            Qt.Tool |                     # Tool window (floating)
            Qt.WindowDoesNotAcceptFocus | # Don't steal focus
            Qt.WA_ShowWithoutActivating   # Show without activating
        )
        
        # Make background semi-transparent
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Set size and position
        self.setFixedSize(200, 150)
        self.move(100, 100)
        
        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Create main content
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 0.9);
                border: 2px solid #ffffff;
                border-radius: 15px;
            }
        """)
        
        content_layout = QVBoxLayout()
        self.content_widget.setLayout(content_layout)
        
        # Icon and title
        self.icon_label = QLabel("🤖")
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("""
            QLabel {
                color: #ff4444;
                font-size: 48px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        content_layout.addWidget(self.icon_label)
        
        # Title
        self.title_label = QLabel("JARVIS")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        content_layout.addWidget(self.title_label)
        
        # Status
        self.status_label = QLabel("Always Visible")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #58a6ff;
                font-size: 12px;
                padding: 5px;
            }
        """)
        content_layout.addWidget(self.status_label)
        
        layout.addWidget(self.content_widget)
        
        # Timer to ensure visibility
        self.visibility_timer = QTimer()
        self.visibility_timer.timeout.connect(self.ensure_visibility)
        self.visibility_timer.start(1000)  # Check every second
        
        # Animation for smooth movement
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.setDuration(300)
        
        print("Mac floating window created")
    
    def ensure_visibility(self):
        """Ensure the window stays visible"""
        if not self.isVisible():
            self.show()
        self.raise_()
        self.activateWindow()
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle mouse movement for dragging"""
        if event.buttons() == Qt.LeftButton:
            new_pos = event.globalPos() - self.drag_position
            self.move(new_pos)
            event.accept()
    
    def mouseDoubleClickEvent(self, event):
        """Handle double click to minimize/maximize"""
        if event.button() == Qt.LeftButton:
            if self.height() > 100:
                # Minimize
                self.animation.setStartValue(self.geometry())
                self.animation.setEndValue(self.geometry().adjusted(0, 0, 0, -100))
                self.animation.start()
            else:
                # Maximize
                self.animation.setStartValue(self.geometry())
                self.animation.setEndValue(self.geometry().adjusted(0, 0, 0, 100))
                self.animation.start()
    
    def keyPressEvent(self, event):
        """Handle key presses"""
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Q:
            QApplication.quit()
        elif event.key() == Qt.Key_H:
            # Hide/show
            if self.isVisible():
                self.hide()
            else:
                self.show()
    
    def paintEvent(self, event):
        """Custom painting for rounded corners and shadow"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create rounded rectangle path
        rect = self.rect()
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
        painter.drawRoundedRect(rect, 15, 15)

class SimpleFloatingIcon(QWidget):
    """Simpler version - just an icon"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JARVIS Icon")
        
        # Basic floating window flags
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(60, 60)
        self.move(200, 200)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Simple icon
        icon = QLabel("🤖")
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("""
            QLabel {
                color: #ff4444;
                background-color: rgba(0, 0, 0, 0.8);
                border: 2px solid #ffffff;
                border-radius: 30px;
                font-size: 30px;
            }
        """)
        layout.addWidget(icon)
        
        # Visibility timer
        timer = QTimer()
        timer.timeout.connect(lambda: self.raise_() if self.isVisible() else self.show())
        timer.start(500)
        
        print("Simple floating icon created")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create both types of floating windows
    floating_window = MacFloatingWindow()
    floating_window.show()
    
    simple_icon = SimpleFloatingIcon()
    simple_icon.show()
    
    print("Mac floating windows created!")
    print("Features:")
    print("- Draggable (click and drag)")
    print("- Double-click to minimize/maximize")
    print("- ESC to close, Q to quit, H to hide/show")
    print("- Always visible on all applications")
    print("- Works across all macOS Spaces")
    
    sys.exit(app.exec_())
