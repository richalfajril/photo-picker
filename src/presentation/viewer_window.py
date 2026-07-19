"""
Viewer Window UI Component.
"""


from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
)
from PySide6.QtGui import (
    QPixmap, QImage, QPainter, QWheelEvent, QMouseEvent, QKeyEvent, QResizeEvent
)
from PySide6.QtCore import Qt, Signal


class PhotoGraphicsView(QGraphicsView):
    """
    Custom QGraphicsView to handle zooming and panning of the photo.
    """
    def __init__(self) -> None:
        super().__init__()
        # Must pass self to QGraphicsScene so it doesn't get garbage collected
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self.photo_item = QGraphicsPixmapItem()
        self._scene.addItem(self.photo_item)

        # Setup view properties
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setStyleSheet("background-color: #111111; border: none;")

        self._has_photo = False
        self._zoom_level = 1.0

    def set_image(self, image: QImage) -> None:
        pixmap = QPixmap.fromImage(image)
        self.photo_item.setPixmap(pixmap)
        self._has_photo = True
        self._scene.setSceneRect(self.photo_item.boundingRect())
        self.reset_zoom()

    def reset_zoom(self) -> None:
        if not self._has_photo:
            return
        self.fitInView(self.photo_item.boundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self._zoom_level = 1.0

    def wheelEvent(self, event: QWheelEvent) -> None:
        if not self._has_photo:
            return
        
        # Zoom logic
        zoom_factor = 1.15
        if event.angleDelta().y() > 0:
            self.scale(zoom_factor, zoom_factor)
            self._zoom_level *= zoom_factor
        else:
            self.scale(1 / zoom_factor, 1 / zoom_factor)
            self._zoom_level /= zoom_factor

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.reset_zoom()
        super().mouseDoubleClickEvent(event)


class ViewerWindow(QWidget):
    """
    The main viewer interface for displaying photos and information.
    """
    
    # Navigation Signals
    next_requested = Signal()
    prev_requested = Signal()
    first_requested = Signal()
    last_requested = Signal()
    copy_requested = Signal()
    undo_requested = Signal()
    exit_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Photo Picker - Viewer")
        self.setStyleSheet("background-color: #111111; color: #FFFFFF;")
        self._is_fullscreen = False
        self._setup_ui()

    def _setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Photo Area
        self.photo_view = PhotoGraphicsView()
        main_layout.addWidget(self.photo_view, stretch=1)
        
        # Selected Badge Overlay
        self.lbl_badge = QLabel("✓ SELECTED", self.photo_view)
        self.lbl_badge.setStyleSheet("""
            QLabel {
                background-color: #22C55E;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 16px;
                border-bottom-left-radius: 10px;
            }
        """)
        self.lbl_badge.hide()

        # Bottom Information Bar
        info_bar = QWidget()
        info_bar.setFixedHeight(60)
        info_bar.setStyleSheet("background-color: #222222;")
        info_layout = QHBoxLayout(info_bar)
        info_layout.setContentsMargins(20, 0, 20, 0)

        self.lbl_filename = QLabel("Filename")
        self.lbl_filename.setStyleSheet("font-size: 14px; font-weight: bold;")
        info_layout.addWidget(self.lbl_filename)

        info_layout.addStretch()

        self.lbl_progress = QLabel("0 / 0")
        self.lbl_progress.setStyleSheet("font-size: 14px;")
        info_layout.addWidget(self.lbl_progress)

        info_layout.addStretch()

        self.lbl_selected = QLabel("Selected: 0")
        self.lbl_selected.setStyleSheet("font-size: 14px; font-weight: bold; color: #22C55E;")
        info_layout.addWidget(self.lbl_selected)

        main_layout.addWidget(info_bar)
        
        self.setMinimumSize(800, 600)

    def set_image(self, image: QImage, filename: str, current: int, total: int, selected: int, is_selected: bool) -> None:
        """Updates the viewer with a new image and metadata."""
        self.photo_view.set_image(image)
        self.lbl_filename.setText(filename)
        self.lbl_progress.setText(f"{current} / {total}")
        self.lbl_selected.setText(f"Selected: {selected}")
        
        if is_selected:
            self.lbl_badge.show()
        else:
            self.lbl_badge.hide()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        key = event.key()
        if key == Qt.Key.Key_Right:
            self.next_requested.emit()
        elif key == Qt.Key.Key_Left:
            self.prev_requested.emit()
        elif key == Qt.Key.Key_Home:
            self.first_requested.emit()
        elif key == Qt.Key.Key_End:
            self.last_requested.emit()
        elif key == Qt.Key.Key_Space:
            self.copy_requested.emit()
        elif key == Qt.Key.Key_Backspace:
            self.undo_requested.emit()
        elif key == Qt.Key.Key_F:
            self.toggle_fullscreen()
        elif key == Qt.Key.Key_Escape:
            if self.isFullScreen():
                self.toggle_fullscreen()
            else:
                self.exit_requested.emit()
        else:
            super().keyPressEvent(event)

    def toggle_fullscreen(self) -> None:
        if self._is_fullscreen:
            self.showNormal()
        else:
            self.showFullScreen()
        self._is_fullscreen = not self._is_fullscreen

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        # Position badge at top right corner of photo_view
        badge_w = self.lbl_badge.sizeHint().width()
        self.lbl_badge.move(self.photo_view.width() - badge_w, 0)
