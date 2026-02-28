import sys, os, io

# --------------------------------------------------
# FIX FOR PYINSTALLER + NORMAL PYTHON PATHS
# --------------------------------------------------

if getattr(sys, 'frozen', False):
    # Running from .exe (PyInstaller)
    BASE_DIR = sys._MEIPASS  
else:
    # Running from source (.py)
    # BASE_DIR must be project root, NOT interface/
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add project root
sys.path.insert(0, BASE_DIR)

# Add interface folder
sys.path.insert(0, os.path.join(BASE_DIR, "interface"))

# Add analyser folder
sys.path.insert(0, os.path.join(BASE_DIR, "analyser"))

# --------------------------------------------------

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from minimap import MinimapWindow
import subprocess

from ide import Ui_mw_main

# Import backend
from analyser.lexer_frog import Lexer, LexicalError
from analyser.syntaxique_frog import Syntaxe, SyntaxiqueError
from analyser.semantique_frog import Semantique, SemanticError

# >>> IMPORT DU HIGHLIGHTER <<<
from syntax_highlighter import FrogHighlighter


def resource_path(relative_path):
    """Get absolute path to resource in dev or PyInstaller EXE."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mw_main()
        self.ui.setupUi(self)
        print([w for w in dir(self.ui) if "error" in w.lower()])

        #  SYNTAX HIGHLIGHTER <<<
        self.highlighter = FrogHighlighter(self.ui.tb_code.document())

        # Connexions des boutons
        self.ui.pb_upload.clicked.connect(self.upload_file)
        self.ui.pb_runLexical.clicked.connect(self.run_lexical)
        self.ui.actionLexical.triggered.connect(self.run_lexical)
        self.ui.pb_runSyntax.clicked.connect(self.run_syntax)
        self.ui.actionSyntax.triggered.connect(self.run_syntax)
        self.ui.pb_runSemantic.clicked.connect(self.run_semantic)
        self.ui.actionSemantic.triggered.connect(self.run_semantic)

        self.ui.pb_generateTree.clicked.connect(self.generate_tree)

        # report
        self.ui.actionReport.triggered.connect(self.open_pdf_report)
        self.ui.actionDocumentation.triggered.connect(self.open_documentation)

        self.ui.pb_openMiniMap.clicked.connect(self.show_minimap)

        self.minimap_window = MinimapWindow(self.ui.tb_code)
        self.minimap_window.hide()
        self.position_minimap()

    # --------------------------------------------------
    # UPLOAD FILE
    # --------------------------------------------------
    def upload_file(self):
        from PyQt5.QtWidgets import QFileDialog
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "",
            "FROG Files (*.txt *.frog *.fg);;All Files (*)"
        )

        if path:
            self.ui.le_path.setText(path)
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()
                self.ui.tb_code.setPlainText(code)
            self.log("File loaded.")

    # --------------------------------------------------
    # RUN LEXICAL
    # --------------------------------------------------
    def run_lexical(self):
        code = self.ui.tb_code.toPlainText()

        if not code.strip():
            self.ui.tb_results.setPlainText(" No code to analyze.")
            return

        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            self.ui.tb_results.clear()
            for t in tokens:
                self.ui.tb_results.append(str(t))

            self.ui.lv_errors.clear()
            self.log("Lexical analysis complete")

        except LexicalError as e:
            self.ui.lv_errors.clear()
            self.ui.lv_errors.addItem(str(e))
            self.ui.tb_results.setPlainText(" Lexical Error!!!")
            self.log(" Lexical error!!!")

    # --------------------------------------------------
    # RUN SYNTAX
    # --------------------------------------------------
    def run_syntax(self):
        code = self.ui.tb_code.toPlainText()

        if not code.strip():
            self.ui.tb_results.setPlainText("No code to analyze.")
            return

        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
        except LexicalError as e:
            self.ui.lv_errors.clear()
            self.ui.lv_errors.addItem("Lexical error: " + str(e))
            self.log("Lexical error!!!")
            return

        try:
            parser = Syntaxe(tokens)
            graph_root, ast_root = parser.program()

            tree_text = self.format_ast(ast_root)
            self.ui.tb_results.setPlainText(
                "Syntax OK\n\n======== AST ========\n" + tree_text +
                "\n\nImage générée : arbre_syntaxique.png"
            )

            self.ui.lv_errors.clear()
            self.log("Syntax analysis complete ")

            if os.path.exists("arbre_syntaxique.png"):
                scene = QtWidgets.QGraphicsScene()
                pixmap = QPixmap("arbre_syntaxique.png")
                scene.addPixmap(pixmap)
                self.ui.gv_tree.setScene(scene)

        except SyntaxiqueError as e:
            self.ui.lv_errors.clear()
            self.ui.lv_errors.addItem("Syntax error: " + str(e))
            self.ui.tb_results.setPlainText("Syntax Error!!!")
            self.log(" Syntax error!!!")

    # --------------------------------------------------
    # FORMAT AST
    # --------------------------------------------------
    def format_ast(self, node, indent=0):
        txt = "  " * indent + node.type
        if node.value is not None:
            txt += f" : {node.value}"
        txt += "\n"
        for ch in node.children:
            txt += self.format_ast(ch, indent + 1)
        return txt

    # --------------------------------------------------
    # LOGGING
    # --------------------------------------------------
    def log(self, msg):
        self.ui.lv_logs.addItem(msg)

    # --------------------------------------------------
    # RUN SEMANTIC
    # --------------------------------------------------
    def run_semantic(self):

        code = self.ui.tb_code.toPlainText()

        if not code.strip():
            self.ui.tb_results.setPlainText("No code to analyze.")
            return

        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
        except LexicalError as e:
            self.ui.lv_errors.clear()
            self.ui.lv_errors.addItem("Lexical error: " + str(e))
            self.ui.tb_results.setPlainText("Lexical Error!!!")
            self.log("Lexical error!!!")
            return

        try:
            parser = Syntaxe(tokens)
            _, ast_root = parser.program()
        except SyntaxiqueError as e:
            self.ui.lv_errors.clear()
            self.ui.lv_errors.addItem("Syntax error: " + str(e))
            self.ui.tb_results.setPlainText("Syntax Error!!!")
            self.log("Syntax error!!!")
            return

        try:
            sem = Semantique(ast_root)

            buffer = io.StringIO()
            old_stdout = sys.stdout
            sys.stdout = buffer

            sem.run()

            sys.stdout = old_stdout
            semantic_output = buffer.getvalue().strip()

            result_text = "Semantic Analysis OK\n\n"

            if semantic_output:
                result_text += "======== Program Output ========\n" + semantic_output + "\n\n"
            else:
                result_text += "No program output.\n\n"

            result_text += "======== Symbol Table========\n"
            for k, v in sem.symboles.items():
                result_text += f"{k} : {v}\n"

            self.ui.tb_results.setPlainText(result_text)

            self.ui.lv_errors.clear()
            self.log("Semantic analysis complete")

        except SemanticError as e:
            sys.stdout = old_stdout
            self.ui.lv_errors.clear()
            self.ui.lv_errors.addItem(str(e))
            self.ui.tb_results.setPlainText("Semantic Error!!!")
            self.log("Semantic error!!!")

    # --------------------------------------------------
    # GENERATE TREE
    # --------------------------------------------------
    def generate_tree(self):
        code = self.ui.tb_code.toPlainText()

        if not code.strip():
            self.ui.tb_results.setPlainText("No code to analyze.")
            return

        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
        except LexicalError as e:
            self.ui.lv_errors.clear()
            self.ui.lv_errors.addItem("Lexical error: " + str(e))
            self.ui.tb_results.setPlainText("Lexical Error!!!")
            self.log("Lexical error!!!")
            return

        try:
            parser = Syntaxe(tokens)
            graph_root, ast_root = parser.program()

            self.ui.tb_results.setPlainText(
                "Syntax Tree Generated\n\n======== AST ========\n\n\nImage générée : arbre_syntaxique.png"
            )

            self.ui.lv_errors.clear()
            self.log("Syntax tree generated.")

            if os.path.exists("arbre_syntaxique.png"):
                scene = QtWidgets.QGraphicsScene()
                pixmap = QPixmap("arbre_syntaxique.png")
                scene.addPixmap(pixmap)

                self.ui.gv_tree.setScene(scene)
                self.ui.gv_tree.fitInView(scene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)

            else:
                self.ui.tb_results.append("\nImage NOT FOUND!")

        except SyntaxiqueError as e:
            self.ui.lv_errors.clear()
            self.ui.lv_errors.addItem("Syntax error: " + str(e))
            self.ui.tb_results.setPlainText("Syntax Error!!!")
            self.log("Syntax error!!!")

    # --------------------------------------------------
    # MINIMAP POSITION
    # --------------------------------------------------
    def position_minimap(self):
        geo = self.geometry()
        x = geo.x() + geo.width() - 300
        y = geo.y() + 600
        self.minimap_window.move(x, y)

    def moveEvent(self, event):
        self.position_minimap()
        super().moveEvent(event)

    def resizeEvent(self, event):
        self.position_minimap()
        super().resizeEvent(event)

    # --------------------------------------------------
    # OPEN PDF REPORT
    # --------------------------------------------------
    def open_pdf_report(self):
        pdf_path = resource_path("interface/Rapport.pdf")

        if not os.path.exists(pdf_path):
            QMessageBox.warning(self, "Error", f"PDF not found:\n{pdf_path}")
            return

        if sys.platform.startswith("win"):
            os.startfile(pdf_path)
        elif sys.platform.startswith("darwin"):
            subprocess.call(["open", pdf_path])
        else:
            subprocess.call(["xdg-open", pdf_path])

    # --------------------------------------------------
    # OPEN MINIMAP
    # --------------------------------------------------
    def show_minimap(self):
        if self.minimap_window.isVisible():
            self.minimap_window.raise_()
            self.minimap_window.activateWindow()
        else:
            self.minimap_window.show()
            self.position_minimap()

    # --------------------------------------------------
    # OPEN DOCUMENTATION
    # --------------------------------------------------
    def open_documentation(self):
        doc_path = resource_path("docs/build/index.html")

        if not os.path.exists(doc_path):
            QMessageBox.warning(self, "Error", f"Documentation not found:\n{doc_path}")
            return

        if sys.platform.startswith("win"):
            os.startfile(doc_path)
        elif sys.platform.startswith("darwin"):
            subprocess.call(["open", doc_path])
        else:
            subprocess.call(["xdg-open", doc_path])


# --------------------------------------------------
# RUN APP
# --------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    icon_path = os.path.join(base_path, "interface", "icons", "compiler.ico")

    app.setWindowIcon(QIcon(icon_path))

    win = MainWindow()
    win.setWindowIcon(QIcon(icon_path))
    win.show()

    sys.exit(app.exec())
