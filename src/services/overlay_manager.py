"""
Service for managing visual UI overlays (COPIED, REMOVED).
"""
from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QTimer


class OverlayManager:
    """
    Manages transient visual notifications on top of the ViewerWindow.
    """
    def __init__(self, parent_widget: QWidget) -> None:
        self.parent = parent_widget
        
        self.label = QLabel(self.parent)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.label.hide()
        
        # Using a QPropertyAnimation on windowOpacity doesn't always work on child widgets 
        # in some OS/environments. To be safe across platforms for child widgets, 
        # we can use a graphics effect, but PySide6's QGraphicsOpacityEffect is standard.
        from PySide6.QtWidgets import QGraphicsOpacityEffect
        self.opacity_effect = QGraphicsOpacityEffect(self.label)
        self.label.setGraphicsEffect(self.opacity_effect)
        
        self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._start_fade_out)

    def show_overlay(self, text: str, color: str = "#22C55E") -> None:
        """
        Shows a fading overlay with the given text and color.
        """
        self.label.setText(text)
        self.label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 48px;
                font-weight: bold;
                background-color: rgba(0, 0, 0, 150);
                border-radius: 20px;
                padding: 20px 40px;
            }}
        """)
        
        self.label.adjustSize()
        self._center_label()
        
        # Disconnect previous finished connections if any
        try:
            self.fade_anim.finished.disconnect()
        except RuntimeError:
            pass
            
        self.opacity_effect.setOpacity(1.0)
        self.label.show()
        self.label.raise_()
        
        # Stop any existing animation
        self.fade_anim.stop()
        self.timer.stop()
        
        # Keep it fully visible for 400ms before fading out
        self.timer.start(400)

    def _start_fade_out(self) -> None:
        self.fade_anim.setDuration(400)
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        self.fade_anim.finished.connect(self.label.hide)
        self.fade_anim.start()

    def _center_label(self) -> None:
        if not self.parent:
            return
            
        parent_rect = self.parent.rect()
        label_rect = self.label.rect()
        
        x = (parent_rect.width() - label_rect.width()) // 2
        y = (parent_rect.height() - label_rect.height()) // 2
        
        self.label.move(x, y)
