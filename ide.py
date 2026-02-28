from PyQt5 import QtCore, QtGui, QtWidgets
import recources_rc

class Ui_mw_main(object):
    def setupUi(self, mw_main):
        mw_main.setObjectName("mw_main")
        mw_main.resize(1100, 690)

        # ********* CENTRAL WIDGET ********
        self.centralwidget = QtWidgets.QWidget(mw_main)
        self.verticalLayout_root = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_root.setContentsMargins(0, 0, 0, 0)

        # ******* MENUBAR **********
        self.menubar = QtWidgets.QMenuBar()
        self.menuFile = self.menubar.addMenu("File")
        self.menuRun = self.menubar.addMenu("Run")
        self.menuHelp = self.menubar.addMenu("Help")
        mw_main.setMenuBar(self.menubar)

        # Actions
        self.actionToggleTheme = QtWidgets.QAction(QtGui.QIcon(":/icons/icons/sun.png"),"Toggle Theme", mw_main)
        self.actionClose = QtWidgets.QAction(QtGui.QIcon(":/icons/icons/close.png"), "Close")
        self.actionLexical = QtWidgets.QAction(QtGui.QIcon(":/icons/icons/lexical-icon.png"), "Run Lexical")
        self.actionSyntax = QtWidgets.QAction(QtGui.QIcon(":/icons/icons/syntaxe_icon.png"), "Run Syntax")
        self.actionSemantic = QtWidgets.QAction(QtGui.QIcon(":/icons/icons/semantic.png"), "Run Semantic")
        self.actionDocumentation = QtWidgets.QAction(QtGui.QIcon(":/icons/icons/documentation.png"), "documentation")
        self.actionReport = QtWidgets.QAction(QtGui.QIcon(":/icons/icons/help.png"), "report")
        
        self.menuFile.addAction(self.actionToggleTheme)
        self.menuFile.addAction(self.actionClose)
        self.menuRun.addAction(self.actionLexical)
        self.menuRun.addAction(self.actionSyntax)
        self.menuRun.addAction(self.actionSemantic)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addAction(self.actionReport)

        # *********** TOOLBAR ***********
        self.toolbar = QtWidgets.QToolBar()
        mw_main.addToolBar(self.toolbar)

        self.w_tool = QtWidgets.QWidget()
        self.h_tool = QtWidgets.QHBoxLayout(self.w_tool)
        self.h_tool.setContentsMargins(5, 5, 5, 5)

        self.pb_upload = QtWidgets.QPushButton()
        self.pb_upload.setIcon(QtGui.QIcon(":/icons/icons/upload_file_green.png"))
        self.pb_upload.setText("Upload File")

        self.le_path = QtWidgets.QLineEdit()
        self.le_path.setPlaceholderText("No file selected...")
        self.le_path.setReadOnly(True)

        self.h_tool.addWidget(self.pb_upload)
        self.h_tool.addWidget(self.le_path)
        self.toolbar.addWidget(self.w_tool)

        #********** MAIN SPLITTER **********
        self.splitterV = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.verticalLayout_root.addWidget(self.splitterV)

        # **********PANELS SPLITTER il y left center right ********
        self.splitterH = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.splitterV.addWidget(self.splitterH)

        # LEFT PANEL
        self.leftPanel = QtWidgets.QFrame()
        self.leftPanel.setObjectName("leftPanel")
        v_left = QtWidgets.QVBoxLayout(self.leftPanel)

        self.l_explorer = QtWidgets.QLabel("<img src=':/icons/icons/explorer.png' width='20' height='20'>  Explorer")
        v_left.addWidget(self.l_explorer)

        self.pb_runLexical = QtWidgets.QPushButton("Run Lexical")
        self.pb_runLexical.setIcon(QtGui.QIcon(":/icons/icons/lexical-icon.png"))
        v_left.addWidget(self.pb_runLexical)

        self.pb_runSyntax = QtWidgets.QPushButton("Run Syntax")
        self.pb_runSyntax.setIcon(QtGui.QIcon(":/icons/icons/syntaxe_icon.png"))
        v_left.addWidget(self.pb_runSyntax)

        self.pb_generateTree = QtWidgets.QPushButton("Generate Tree")
        self.pb_generateTree.setIcon(QtGui.QIcon(":/icons/icons/tree-structure.png"))
        v_left.addWidget(self.pb_generateTree)
        

        self.pb_runSemantic = QtWidgets.QPushButton("Run Semantic")
        self.pb_runSemantic.setIcon(QtGui.QIcon(":/icons/icons/semantic.png"))
        v_left.addWidget(self.pb_runSemantic)

        self.pb_openMiniMap = QtWidgets.QPushButton("Show Mini Map")
        self.pb_openMiniMap.setIcon(QtGui.QIcon(":/icons/icons/map.png"))
        v_left.addWidget(self.pb_openMiniMap)
        

        v_left.addStretch()
        self.splitterH.addWidget(self.leftPanel)

        # MAIN PANEL
        self.mainPanel = QtWidgets.QFrame()
        self.mainPanel.setObjectName("mainPanel")
        v_main = QtWidgets.QVBoxLayout(self.mainPanel)

        self.l_file = QtWidgets.QLabel("File... <img src=':/icons/icons/nofile_white.png' width='30' height='30'>")
        v_main.addWidget(self.l_file)

        self.tb_code = QtWidgets.QTextEdit()
        
        self.tb_code.setPlaceholderText("Write code or upload a file...")
        self.tb_code.setReadOnly(False)
        v_main.addWidget(self.tb_code)

        self.splitterH.addWidget(self.mainPanel)

        # RESULTS PANEL
        self.resultsPanel = QtWidgets.QFrame()
        self.resultsPanel.setObjectName("resultsPanel")
        v_results = QtWidgets.QVBoxLayout(self.resultsPanel)

        self.tabs = QtWidgets.QTabWidget()

        # Results
        w_res = QtWidgets.QWidget()
        l_res = QtWidgets.QVBoxLayout(w_res)
        self.tb_results = QtWidgets.QTextEdit()
        self.tb_results.setReadOnly(True)
        self.tb_results.setPlaceholderText("Results appear here...")
        l_res.addWidget(self.tb_results)
        self.tabs.addTab(w_res, "Results")

        # Errors
        w_err = QtWidgets.QWidget()
        l_err = QtWidgets.QVBoxLayout(w_err)
        self.lv_errors = QtWidgets.QListWidget()
        l_err.addWidget(self.lv_errors)
        self.tabs.addTab(w_err, "Errors")

        # Tree 
        w_tree = QtWidgets.QWidget()
        l_tree = QtWidgets.QVBoxLayout(w_tree)
        l_tree.setContentsMargins(5, 5, 5, 5)
        l_tree.setSpacing(5)
        
        # Create zoom control toolbar
        self.tree_toolbar = QtWidgets.QWidget()
        self.tree_toolbar_layout = QtWidgets.QHBoxLayout(self.tree_toolbar)
        self.tree_toolbar_layout.setContentsMargins(5, 2, 5, 2)
        
        # Zoom buttons
        self.btn_zoom_out = QtWidgets.QPushButton()
        self.btn_zoom_out.setIcon(QtGui.QIcon(":/icons/icons/zoom_out.png"))
        self.btn_zoom_out.setToolTip("Zoom Out")
        self.btn_zoom_out.setFixedSize(32, 32)
        
        self.btn_zoom_in = QtWidgets.QPushButton()
        self.btn_zoom_in.setIcon(QtGui.QIcon(":/icons/icons/zoom_in.png"))
        self.btn_zoom_in.setToolTip("Zoom In")
        self.btn_zoom_in.setFixedSize(32, 32)
        
        
        self.btn_reset_view = QtWidgets.QPushButton()
        self.btn_reset_view.setIcon(QtGui.QIcon(":/icons/icons/reset.png"))
        self.btn_reset_view.setToolTip("Reset View")
        self.btn_reset_view.setFixedSize(32, 32)
        
        # Status label
        self.lbl_zoom_status = QtWidgets.QLabel("Zoom: 100%")
        self.lbl_zoom_status.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        self.tree_toolbar_layout.addWidget(self.btn_zoom_out)
        self.tree_toolbar_layout.addWidget(self.btn_zoom_in)
        self.tree_toolbar_layout.addWidget(self.btn_reset_view)
        self.tree_toolbar_layout.addStretch()
        self.tree_toolbar_layout.addWidget(self.lbl_zoom_status)
        
        # Graphics View for tree
        self.gv_tree = QtWidgets.QGraphicsView()
        self.gv_tree.setRenderHint(QtGui.QPainter.Antialiasing)
        self.gv_tree.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        self.gv_tree.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.gv_tree.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.gv_tree.setResizeAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        
        # Initialize scene
        self.tree_scene = QtWidgets.QGraphicsScene()
        self.gv_tree.setScene(self.tree_scene)
        
        # Add widgets to tree tab
        l_tree.addWidget(self.tree_toolbar)
        l_tree.addWidget(self.gv_tree)
        self.tabs.addTab(w_tree, "Syntaxique Tree")

        v_results.addWidget(self.tabs)
        self.splitterH.addWidget(self.resultsPanel)

        # LOG PANEL
        self.logPanel = QtWidgets.QFrame()
        self.logPanel.setObjectName("logPanel")
        v_logs = QtWidgets.QVBoxLayout(self.logPanel)
        self.lv_logs = QtWidgets.QListWidget()
        v_logs.addWidget(self.lv_logs)
        self.splitterV.addWidget(self.logPanel)

        mw_main.setCentralWidget(self.centralwidget)

        # CURSOR POINTER
        pointer = QtGui.QCursor(QtCore.Qt.PointingHandCursor)
        for btn in mw_main.findChildren(QtWidgets.QPushButton):
            btn.setCursor(pointer)
        for tabbar in mw_main.findChildren(QtWidgets.QTabBar):
            tabbar.setCursor(pointer)
        self.menubar.setCursor(pointer)

        # Initialize zoom variables
        self.tree_zoom_factor = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 10.0
        
        # Connect zoom signals
        self.btn_zoom_in.clicked.connect(self.zoom_in_tree)
        self.btn_zoom_out.clicked.connect(self.zoom_out_tree)
        self.btn_reset_view.clicked.connect(self.reset_tree_view)
        # Connect tab change to auto-fit when tree tab is selected
        self.tabs.currentChanged.connect(self.on_tab_changed)
        #close program
        self.actionClose.triggered.connect(lambda: QtWidgets.QApplication.quit())
        
       
    
        # --- Gestion des themes ---
        self.current_theme = "dark"
        self.actionToggleTheme.triggered.connect(lambda: self.toggle_theme(mw_main))
        self.apply_dark_theme(mw_main)

        mw_main.setWindowTitle("Compilateur FROG")
        mw_main.setWindowIcon(QtGui.QIcon(":/icons/icons/compiler.ico"))
        
        # Override wheel event for zoom
        self.gv_tree.wheelEvent = self.tree_wheel_event

    # --- Tree Zoom and Navigation Functions ---
    def zoom_in_tree(self):
        """Zoom in on the tree"""
        if self.tree_zoom_factor < self.max_zoom:
            self.tree_zoom_factor *= 1.2
            self.gv_tree.scale(1.2, 1.2)
            self.update_zoom_status()
            
    def zoom_out_tree(self):
        """Zoom out on the tree"""
        if self.tree_zoom_factor > self.min_zoom:
            self.tree_zoom_factor *= 0.8
            self.gv_tree.scale(0.8, 0.8)
            self.update_zoom_status()
            
    def fit_tree_to_view(self):
         """Fit the entire tree to the view"""
         if not self.tree_scene:
             return
         
         # Get the bounding rect of all items in the scene
         items_rect = self.tree_scene.itemsBoundingRect()
         
         # If no items or invalid rect, return
         if items_rect.isEmpty() or items_rect.isNull():
             return
         
         # Add a small margin around the items
         margin = 20
         items_rect.adjust(-margin, -margin, margin, margin)
         
         # Set the scene rect to include all items
         self.tree_scene.setSceneRect(items_rect)
         
         # Fit the view to show the entire scene
         self.gv_tree.fitInView(items_rect, QtCore.Qt.KeepAspectRatio)
         
         # Force update
         self.gv_tree.update()
         
         # Calculate the new zoom factor
         self._calculate_current_zoom()
         
         # Update status
         self.update_zoom_status()
    def reset_tree_view(self):
        """Reset the tree view to original scale"""
        self.gv_tree.resetTransform()
        self.tree_zoom_factor = 1.0
        self.update_zoom_status()
        
    def update_zoom_status(self):
        """Update the zoom status label"""
        zoom_percent = int(self.tree_zoom_factor * 100)
        self.lbl_zoom_status.setText(f"Zoom: {zoom_percent}%")
        
    def tree_wheel_event(self, event):
        """Handle mouse wheel zoom for tree view"""
        if event.modifiers() & QtCore.Qt.ControlModifier:
            # Zoom with Ctrl + Wheel
            zoom_in_factor = 1.15
            zoom_out_factor = 1 / zoom_in_factor
            
            old_pos = self.gv_tree.mapToScene(event.pos())
            
            if event.angleDelta().y() > 0:
                if self.tree_zoom_factor < self.max_zoom:
                    self.tree_zoom_factor *= zoom_in_factor
                    self.gv_tree.scale(zoom_in_factor, zoom_in_factor)
            else:
                if self.tree_zoom_factor > self.min_zoom:
                    self.tree_zoom_factor *= zoom_out_factor
                    self.gv_tree.scale(zoom_out_factor, zoom_out_factor)
            
            new_pos = self.gv_tree.mapToScene(event.pos())
            delta = new_pos - old_pos
            self.gv_tree.translate(delta.x(), delta.y())
            
            self.update_zoom_status()
            event.accept()
        else:
            # Default wheel behavior (scroll)
            QtWidgets.QGraphicsView.wheelEvent(self.gv_tree, event)
            
    def on_tab_changed(self, index):
        """Auto-fit tree when tree tab is selected"""
        if self.tabs.tabText(index) == "Syntaxique Tree":
            QtCore.QTimer.singleShot(100, self.fit_tree_to_view)
            
    
    # --- Fonctions thèmes ---
    def apply_dark_theme(self, mw_main):
        mw_main.setStyleSheet("""
            /* GENERAL */
            QWidget {
                background-color: #1a1a1a;
                color: #e8e8e8;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                selection-background-color: #2e7d32;
            }
            
            QMenuBar {
                background-color: #0d0d0d;
                color: #e8e8e8;
                border-bottom: 1px solid #333333;
                padding: 6px;
                font-size: 14px; 
            }
            
            QMenuBar::item {
                background-color: transparent;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 14px;             
            }
          
            QMenuBar::item:selected {
                background-color: #2e7d32;
                color: #ffffff;
            }
            
            QToolBar {
                background-color: #141414;
                border-bottom: 1px solid #333333;
                spacing: 10px;
                padding: 8px;
            }

            /* BOUTONS PRINCIPAUX */
            QPushButton {
                background-color: #333333;
                color: #e8e8e8;
                padding: 10px 20px;
                border-radius: 6px;
                border: 1px solid #404040;
                font-weight: 500;
                min-height: 24px;
            }
            
            QPushButton:hover {
                background-color: #2e7d32;
                color: #ffffff;
                border: 1px solid #2e7d32;
            }
            
            QPushButton:pressed {
                background-color: #1b5e20;
                color: #ffffff;
            }

            /* BOUTON UPLOAD SPÉCIAL */
            #w_tool QPushButton {
                background-color: #2e7d32;
                color: white;
                font-weight: 600;
                padding: 12px 24px;
                border-radius: 8px;
                border: none;
            }
            
            #w_tool QPushButton:hover {
                background-color: #388e3c;
            }

            /* CHAMP DE TEXTE */
            QLineEdit {
                background-color: #262626;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 10px;
                color: #e8e8e8;
                font-size: 14px;
                selection-background-color: #2e7d32;
            }
            
            QLineEdit:focus {
                border-color: #2e7d32;
                background-color: #2a2a2a;
            }

            /* LEFT PANEL - SIDEBAR */
            #leftPanel {
                background-color: #0d0d0d;
                border-right: 1px solid #333333;
            }
            
            #leftPanel QLabel {
                color: #4caf50;
                font-weight: 600;
                font-size: 16px;
                padding: 12px;
                background-color: #141414;
                border-radius: 6px;
                margin: 8px;
                border-left: 4px solid #4caf50;
            }
            
            #leftPanel QPushButton {
                background-color: #1a1a1a;
                color: #cccccc;
                text-align: left;
                padding: 12px 16px;
                margin: 6px 10px;
                border-radius: 6px;
                font-weight: normal;
                border: 1px solid transparent;
            }
            
            #leftPanel QPushButton:hover {
                background-color: #2e7d32;
                color: #ffffff;
                border: 1px solid #4caf50;
            }
            
            #leftPanel QPushButton:pressed {
                background-color: #1b5e20;
                color: #ffffff;
            }

            /* MAIN PANEL - ÉDITEUR */
            #mainPanel {
                background-color: #1a1a1a;
                border: none;
            }
            
            #mainPanel QLabel {
                color: #4caf50;
                font-weight: 600;
                padding: 12px;
                background-color: #141414;
                border-radius: 6px;
                margin: 8px;
                border-left: 4px solid #4caf50;
            }
            
            QTextEdit {
                background-color: #262626;
                border: 1px solid #404040;
                border-radius: 6px;
                color: #e8e8e8;
                font-family: 'Cascadia Code', 'Consolas', monospace;
                font-size: 15px;
                padding: 15px;
                selection-background-color: #2e7d32;
                selection-color: #ffffff;
                line-height: 1.5;
            }
            
            QTextEdit:focus {
                border-color: #2e7d32;
            }

            /* RESULTS PANEL */
            #resultsPanel {
                background-color: #141414;
                border-left: 1px solid #333333;
            }
            
            QTabWidget::pane {
                border: none;
                background-color: #141414;
            }
            
            QTabBar::tab {
                background-color: #262626;
                color: #999999;
                padding: 6px 12px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: 500;
                font-size: 14px;
                border-bottom: 3px solid transparent;
                 min-width: 100px; 
            }
            
            QTabBar::tab:selected {
                background-color: #1a1a1a;
                color: #4caf50;
                border-bottom: 3px solid #4caf50;
            }
            
            QTabBar::tab:hover:!selected {
                background-color: #333333;
                color: #e8e8e8;
            }

            /* LISTES ET VUES */
            QListWidget {
                background-color: #262626;
                border: 1px solid #404040;
                border-radius: 6px;
                color: #e8e8e8;
                outline: none;
                font-family: monospace;
                font-size: 13px;
            }
            
            QListWidget::item {
                padding: 10px 12px;
                border-bottom: 1px solid #363636;
            }
            
            QListWidget::item:selected {
                background-color: #2e7d32;
                color: #ffffff;
            }
            
            QListWidget::item:hover {
                background-color: #333333;
            }
            
            QGraphicsView {
                background-color: #262626;
                border: 1px solid #404040;
                border-radius: 6px;
                color: #e8e8e8;
            }

            /* LOG PANEL */
            #logPanel {
                background-color: #0d0d0d;
                border-top: 1px solid #333333;
            }
            
            #logPanel QListWidget {
                background-color: #141414;
                border: none;
                border-radius: 0px;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
            
            #logPanel QListWidget::item {
                border-bottom: 1px solid #262626;
                padding: 8px 12px;
            }
            
            #logPanel QListWidget::item:hover {
                background-color: #1a1a1a;
            }

            /* SPLITTER */
            QSplitter::handle {
                background-color: #333333;
                border: 1px solid #404040;
            }
            
            QSplitter::handle:hover {
                background-color: #4caf50;
            }

            /* SCROLLBARS */
            QScrollBar:vertical {
                background-color: #262626;
                width: 14px;
                border-radius: 0px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #404040;
                border-radius: 0px;
                min-height: 25px;
                margin: 2px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #4caf50;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }

            /* MENUS ET ACTIONS */
            QMenu {
                background-color: #1a1a1a;
                border: 1px solid #404040;
                border-radius: 6px;
                padding: 6px;
            }
            
            QMenu::item {
                padding: 8px 16px;
                border-radius: 4px;
                margin-right: 20px;
                min-width: 120px;
            }
            
            QMenu::item:selected {
                background-color: #2e7d32;
                color: #ffffff;
            }

            /* PLACEHOLDER TEXT */
            QTextEdit[placeholderText]:empty {
                color: #66bb6a;
                font-style: italic;
            }
            
            QLineEdit[placeholderText]:empty {
                color: #66bb6a;
                font-style: italic;
            }

            /* STATUT ET INDICATEURS */
            QLabel[objectName^="l_"] {
                color: #4caf50;
                font-weight: 600;
            }
            
            /* TREE ZOOM BUTTONS */
            QPushButton[icon] {
                background-color: #333333;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 5px;
            }
            
            QPushButton[icon]:hover {
                background-color: #2e7d32;
                border-color: #4caf50;
            }
            
            QPushButton[icon]:pressed {
                background-color: #1b5e20;
            }
        """)
        self.current_theme = "dark"

    def apply_light_theme(self, mw_main):
        mw_main.setStyleSheet("""
            /* GENERAL */ 
              QWidget {
                  background-color: #f5f5f5;
                  color: #1a1a1a;
                  font-family: 'Segoe UI', Arial, sans-serif;
                  font-size: 14px;
                  selection-background-color: #81c784; /* vert clair pour sélection */
              }
              
              QMenuBar {
                  background-color: #e0e0e0;
                  color: #1a1a1a;
                  border-bottom: 1px solid #ccc;
                  padding: 3px;
                  font-size: 14px; 
              }
              
              QMenuBar::item {
                  background-color: transparent;
                  padding: 6px 12px;
                  border-radius: 4px;
                  font-size: 14px;      
              }
              
              QMenuBar::item:selected {
                  background-color: #81c784;
                  color: #ffffff;
              }
              
              QToolBar {
                  background-color: #dcdcdc;
                  border-bottom: 1px solid #ccc;
                  spacing: 10px;
                  padding: 4px;
              }
              
              /* BOUTONS PRINCIPAUX */
              QPushButton {
                  background-color: #e0e0e0;
                  color: #1a1a1a;
                  padding: 10px 20px;
                  border-radius: 6px;
                  border: 1px solid #ccc;
                  font-weight: 500;
                  min-height: 24px;
              }
              
              QPushButton:hover {
                  background-color: #23D138;
                  color: #ffffff;
                  border: 1px solid #00F545;
              }
              
              QPushButton:pressed {
                  background-color: #66bb6a;
                  color: #ffffff;
              }
              
              /* BOUTON UPLOAD SPÉCIAL */
              #w_tool QPushButton {
                  background-color: #4caf50;
                  color: white;
                  font-weight: 600;
                  padding: 12px 24px;
                  border-radius: 8px;
                  border: none;
              }
              
              #w_tool QPushButton:hover {
                  background-color: #66bb6a;
              }
              
              /* CHAMP DE TEXTE */
              QLineEdit {
                  background-color: #ffffff;
                  border: 1px solid #ccc;
                  border-radius: 4px;
                  padding: 10px;
                  color: #1a1a1a;
                  font-size: 14px;
                  selection-background-color: #81c784;
              }
              
              QLineEdit:focus {
                  border-color: #4caf50;
                  background-color: #f0f0f0;
              }
              
              /* LEFT PANEL - SIDEBAR */
              #leftPanel {
                  background-color: #e0e0e0;
                  border-right: 1px solid #ccc;
              }
              
              #leftPanel QLabel {
                  color: #388e3c;
                  font-weight: 600;
                  font-size: 16px;
                  padding: 12px;
                  background-color: #dcdcdc;
                  border-radius: 6px;
                  margin: 8px;
                  border-left: 4px solid #4caf50;
              }
              
              #leftPanel QPushButton {
                  background-color: #f5f5f5;
                  color: #1a1a1a;
                  text-align: left;
                  padding: 12px 16px;
                  margin: 6px 10px;
                  border-radius: 6px;
                  font-weight: normal;
                  border: 1px solid transparent;
              }
              
              #leftPanel QPushButton:hover {
                  background-color: #3BBA4C;
                  color: #ffffff;
                  border: 1px solid #00F545;
              }
              
              #leftPanel QPushButton:pressed {
                  background-color: #66bb6a;
                  color: #ffffff;
              }
              
              /* MAIN PANEL - ÉDITEUR */
              #mainPanel {
                  background-color: #f5f5f5;
                  border: none;
              }
              
              #mainPanel QLabel {
                  color: #388e3c;
                  font-weight: 600;
                  padding: 12px;
                  background-color: #dcdcdc;
                  border-radius: 6px;
                  margin: 8px;
                  border-left: 4px solid #4caf50;
              }
              
              QTextEdit {
                  background-color: #ffffff;
                  border: 1px solid #ccc;
                  border-radius: 6px;
                  color: #1a1a1a;
                  font-family: 'Cascadia Code', 'Consolas', monospace;
                  font-size: 15px;
                  padding: 15px;
                  selection-background-color: #81c784;
                  selection-color: #ffffff;
                  line-height: 1.5;
              }
              
              QTextEdit:focus {
                  border-color: #4caf50;
              }
              
              /* RESULTS PANEL */
              #resultsPanel {
                  background-color: #dcdcdc;
                  border-left: 1px solid #ccc;
              }
              
              QTabWidget::pane {
                  border: none;
                  background-color: #dcdcdc;
              }
              
              QTabBar::tab {
                  background-color: #f5f5f5;
                  color: #333333;
                 padding: 6px 12px;
                  margin-right: 2px;
                  border-top-left-radius: 8px;
                  border-top-right-radius: 8px;
                  font-weight: 500;
                  font-size: 14px;
                  border-bottom: 3px solid transparent;
                  min-width: 100px; 

              }
              
              QTabBar::tab:selected {
                  background-color: #ffffff;
                  color: #4caf50;
                  border-bottom: 3px solid #4caf50;
              }
              
              QTabBar::tab:hover:!selected {
                  background-color: #e0e0e0;
                  color: #1a1a1a;
              }
              
              /* LISTES ET VUES */
              QListWidget {
                  background-color: #ffffff;
                  border: 1px solid #ccc;
                  border-radius: 6px;
                  color: #1a1a1a;
                  outline: none;
                  font-family: monospace;
                  font-size: 13px;
              }
              
              QListWidget::item {
                  padding: 10px 12px;
                  border-bottom: 1px solid #ccc;
              }
              
              QListWidget::item:selected {
                  background-color: #81c784;
                  color: #ffffff;
              }
              
              QListWidget::item:hover {
                  background-color: #e0e0e0;
              }
              
              QGraphicsView {
                  background-color: #ffffff;
                  border: 1px solid #ccc;
                  border-radius: 6px;
                  color: #1a1a1a;
              }
              
              /* LOG PANEL */
              #logPanel {
                  background-color: #e0e0e0;
                  border-top: 1px solid #ccc;
              }
              
              #logPanel QListWidget {
                  background-color: #f5f5f5;
                  border: none;
                  border-radius: 0px;
                  font-family: 'Consolas', monospace;
                  font-size: 12px;
              }
              
              #logPanel QListWidget::item {
                  border-bottom: 1px solid #ddd;
                  padding: 8px 12px;
              }
              
              #logPanel QListWidget::item:hover {
                  background-color: #e0e0e0;
              }
              
              /* SPLITTER */
              QSplitter::handle {
                  background-color: #ccc;
                  border: 1px solid #bbb;
              }
              
              QSplitter::handle:hover {
                  background-color: #81c784;
              }
              
              /* SCROLLBARS */
              QScrollBar:vertical {
                  background-color: #f5f5f5;
                  width: 14px;
                  border-radius: 0px;
              }
              
              QScrollBar::handle:vertical {
                  background-color: #ccc;
                  border-radius: 0px;
                  min-height: 25px;
                  margin: 2px;
              }
              
              QScrollBar::handle:vertical:hover {
                  background-color: #81c784;
              }
              
              QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                  border: none;
                  background: none;
              }
              
              /* MENUS ET ACTIONS */
              QMenu {
                  background-color: #ffffff;
                  border: 1px solid #ccc;
                  border-radius: 6px;
                  padding: 6px;
              }
              
              QMenu::item {
                  padding: 8px 16px;
                  border-radius: 4px;
                  margin-right: 20px;
                  min-width: 120px;
              }
              
              QMenu::item:selected {
                  background-color: #81c784;
                  color: #ffffff;
              }
              
              /* PLACEHOLDER TEXT */
              QTextEdit[placeholderText]:empty {
                  color: #4caf50;
                  font-style: italic;
              }
              
              QLineEdit[placeholderText]:empty {
                  color: #4caf50;
                  font-style: italic;
              }
              
              /* STATUT ET INDICATEURS */
              QLabel[objectName^="l_"] {
                  color: #388e3c;
                  font-weight: 600;
              }
              
              /* TREE ZOOM BUTTONS */
              QPushButton[icon] {
                  background-color: #e0e0e0;
                  border: 1px solid #ccc;
                  border-radius: 4px;
                  padding: 5px;
              }
              
              QPushButton[icon]:hover {
                  background-color: #3BBA4C;
                  border-color: #00F545;
                  color: white;
              }
              
              QPushButton[icon]:pressed {
                  background-color: #66bb6a;
              }
              
        """)
        self.current_theme = "light"

    def toggle_theme(self, mw_main):
        if self.current_theme == "dark":
            self.apply_light_theme(mw_main)
        else:
            self.apply_dark_theme(mw_main)
   
