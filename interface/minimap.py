from PyQt5 import QtWidgets, QtCore, QtGui

class MinimapWindow(QtWidgets.QWidget):
    def __init__(self, editor, parent=None):
        super().__init__(parent)

        self.editor = editor
        self._syncing = False     # prevents feedback loops
        self._drag_pos = None

        # ===== WINDOW SETTINGS =====
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFixedSize(230, 380)
        

        # ===== BACKGROUND FRAME =====
        bg = QtWidgets.QFrame(self)
        bg.setStyleSheet("""
            QFrame {
                background: #1e1e1e;
                border-radius: 10px;
            }
        """)
        bg.setGeometry(0, 0, 230, 380)

        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 4)
        shadow.setColor(QtGui.QColor(0, 0, 0, 160))
        bg.setGraphicsEffect(shadow)

        main = QtWidgets.QVBoxLayout(bg)
        main.setContentsMargins(8, 8, 8, 8)

        # ===== TITLE BAR =====
        title_layout = QtWidgets.QHBoxLayout()
        lbl = QtWidgets.QLabel("Minimap")
        lbl.setStyleSheet("color: #ddd; font-size: 12px;")

        btn_hide = QtWidgets.QPushButton("–")
        btn_hide.setFixedSize(22, 22)
        btn_hide.setStyleSheet("background:#444;color:white;border-radius:3px;")

        btn_close = QtWidgets.QPushButton("×")
        btn_close.setFixedSize(22, 22)
        btn_close.setStyleSheet("background:#b02525;color:white;border-radius:3px;")

        title_layout.addWidget(lbl)
        title_layout.addStretch()
        title_layout.addWidget(btn_hide)
        title_layout.addWidget(btn_close)
        main.addLayout(title_layout)

        # ===== MINIMAP EDITOR =====
        self.minimap = QtWidgets.QPlainTextEdit()
        self.minimap.setReadOnly(False)  # so we can click + scroll
        self.minimap.setStyleSheet("""
            QPlainTextEdit {
                background: #262626;
                color: #aaaaaa;
                font-size: 7px;
                border-radius: 6px;
            }
        """)
        

        main.addWidget(self.minimap)
        # ===== SIGNALS =====
        btn_close.clicked.connect(self.close)
        btn_hide.clicked.connect(self.hide)

        self.editor.textChanged.connect(self.update_minimap_from_editor)
        self.editor.verticalScrollBar().valueChanged.connect(self.sync_scroll_from_editor)

        self.minimap.verticalScrollBar().valueChanged.connect(self.sync_scroll_from_minimap)
        self.minimap.cursorPositionChanged.connect(self.jump_to_editor)

        # initial sync
        self.update_minimap_from_editor()
        self.minimap.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

    # ==========================================
    # UPDATE MINIMAP WHEN MAIN EDITOR CHANGES
    # ==========================================
    def update_minimap_from_editor(self):
        if self._syncing:
            return

        self._syncing = True
        self.minimap.setPlainText(self.editor.toPlainText())
        self._syncing = False

    # ==========================================
    # SCROLL -> EDITOR -> MINIMAP
    # ==========================================
    def sync_scroll_from_editor(self):
        if self._syncing:
            return

        self._syncing = True
        e = self.editor.verticalScrollBar()
        m = self.minimap.verticalScrollBar()

        ratio = e.value() / max(1, e.maximum())
        m.setValue(int(ratio * m.maximum()))

        self._syncing = False

    # ==========================================
    # SCROLL -> MINIMAP -> EDITOR
    # ==========================================
    def sync_scroll_from_minimap(self):
        if self._syncing:
            return

        self._syncing = True
        e = self.editor.verticalScrollBar()
        m = self.minimap.verticalScrollBar()

        ratio = m.value() / max(1, m.maximum())
        e.setValue(int(ratio * e.maximum()))

        self._syncing = False

    # ==========================================
    # CLICK IN MINIMAP -> JUMP TO THAT LINE
    # ==========================================
    def jump_to_editor(self):
        if self._syncing:
            return

        cursor = self.minimap.textCursor()
        line = cursor.blockNumber()

        self._syncing = True
        main_cursor = self.editor.textCursor()
        main_cursor.movePosition(QtGui.QTextCursor.Start)
        main_cursor.movePosition(QtGui.QTextCursor.Down, n=line)
        self.editor.setTextCursor(main_cursor)
        self._syncing = False

    # ==========================================
    # WINDOW DRAGGING
    # ==========================================
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton and self._drag_pos:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None


    def paintEvent(self, event):
        super().paintEvent(event)
    
        painter = QtGui.QPainter(self.minimap.viewport())
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
    
        # Main editor scroll
        e_sb = self.editor.verticalScrollBar()
        m_sb = self.minimap.verticalScrollBar()
    
        if e_sb.maximum() == 0 or m_sb.maximum() == 0:
            return
    
        # Ratio between editor scroll and minimap scroll space
        ratio_top = e_sb.value() / e_sb.maximum()
    
        # How tall the visible part is in the minimap
        visible_ratio = (self.editor.viewport().height() /
                         self.editor.document().size().height())
    
        minimap_height = self.minimap.viewport().height()
    
        top = ratio_top * minimap_height
        height = visible_ratio * minimap_height
    
        rect = QtCore.QRectF(0, top, self.minimap.viewport().width(), height)
    
        painter.setBrush(QtGui.QColor(80, 150, 255, 60))      # translucent fill
        painter.setPen(QtGui.QColor(80, 150, 255, 120))       # outline
        painter.drawRoundedRect(rect, 4, 4)
    
