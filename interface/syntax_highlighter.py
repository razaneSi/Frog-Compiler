from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import QRegExp


class FrogHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        # === FORMATS ===
        self.f_keyword = self.make_format("#BA3BA9")       # violet
        self.f_comment = self.make_format("#808080", italic=True)  # gris
        self.f_operator = self.make_format("#FA7A53")      # orange
        self.f_string = self.make_format("#2B5DCA")        # bleu clair
        self.f_brackets = self.make_format("#75B515")      # vert
        self.f_number = self.make_format("#F1D104")        # jaune clair

        # === RÈGLES DE COLORATION ===
        self.rules = []

        # KEYWORDS FROG (violet)
        frog_keywords = [
            r"\bFRG_Begin\b", r"\bFRG_End\b", r"\bFRG_Int\b",
            r"\bFRG_Real\b", r"\bFRG_Strg\b", r"\bFRG_Print\b",
            r"\bIf\b", r"\bElse\b", r"\bBegin\b", r"\bEnd\b",
            r"\bRepeat\b", r"\buntil\b",
        ]
        for kw in frog_keywords:
            self.add_rule(kw, self.f_keyword)

        # COMMENTAIRES (gris)
        self.add_rule(r"##[^\n]*", self.f_comment)

        # STRINGS (bleu clair)
        self.add_rule(r"\"[^\"]*\"", self.f_string)

        # NUMBERS (jaune)
        self.add_rule(r"\b\d+\b", self.f_number)

        # OPERATORS (orange)
        operators = [
            r":=", r"\+", r"-", r"\*", r"/",
            r"==", r"!=", r"<=", r">=", r"<", r">"
        ]
        for op in operators:
            self.add_rule(op, self.f_operator)

        # BRACKETS & COMMA (vert)
        brackets = [r"\[", r"\]", r","]
        for br in brackets:
            self.add_rule(br, self.f_brackets)

    # === UTILITY METHODS ===
    def add_rule(self, pattern, fmt):
        self.rules.append((QRegExp(pattern), fmt))

    def make_format(self, color, bold=False, italic=False):
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        if bold: fmt.setFontWeight(QFont.Bold)
        if italic: fmt.setFontItalic(True)
        return fmt

    # === MAIN COLORING FUNCTION ===
    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            index = pattern.indexIn(text)
            while index >= 0:
                length = pattern.matchedLength()
                self.setFormat(index, length, fmt)
                index = pattern.indexIn(text, index + length)
