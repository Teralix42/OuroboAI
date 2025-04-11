from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
import re

class PythonHighlighter(QSyntaxHighlighter):
	def __init__(self, document):
		super().__init__(document)

		self.rules = []

		def make_format(color, italic=False, bold=False):
			_format = QTextCharFormat()
			_format.setForeground(QColor(color))
			if italic:
				_format.setFontItalic(True)
			if bold:
				_format.setFontWeight(QFont.Bold)
			return _format

		# --- Rules ---

		# Comments 🟩
		comment_format = make_format("#6A9955", italic=True)
		self.rules.append((re.compile(r"#.*"), comment_format))

		# Strings 🟨
		string_format = make_format("#CE9178")
		self.rules.append((re.compile(r'(\".*?\"|\'.*?\')'), string_format))

		# Keywords / Storage 🟦
		keywords = r"\b(False|class|finally|is|return|None|continue|for|lambda|try|True|def|from|nonlocal|while|and|del|global|not|with|as|elif|if|or|yield|assert|else|import|pass|break|except|in|raise)\b"
		keyword_format = make_format("#569CD6", bold=True)
		self.rules.append((re.compile(keywords), keyword_format))

		# Function names 🟪
		func_format = make_format("#DCDCAA")
		self.rules.append((re.compile(r"\bdef\s+(\w+)"), func_format))

		# Class names 🌈
		class_format = make_format("#4EC9B0")
		self.rules.append((re.compile(r"\bclass\s+(\w+)"), class_format))

		# Operators ⚫
		operator_format = make_format("#569CD6")
		self.rules.append((re.compile(r"[-+*/%&|^~<>!=]=?|==|//|<<|>>|\*\*|\band\b|\bor\b|\bnot\b"), operator_format))

		# Brackets (pale yellow)
		bracket_format = make_format("#DCDCAA")
		self.rules.append((re.compile(r"[\[\]{}()]"), bracket_format))

		# Numbers / constants 🟧
		number_format = make_format("#B5CEA8")
		self.rules.append((re.compile(r"\b[0-9]+(\.[0-9]*)?\b"), number_format))

		# Variables 🔵 (simple: highlight assignment names)
		variable_format = make_format("#9CDCFE")
		self.rules.append((re.compile(r"\b(\w+)\s*="), variable_format))

	def highlightBlock(self, text):
		# Default color (white)
		default_format = QTextCharFormat()
		default_format.setForeground(QColor("white"))
		self.setFormat(0, len(text), default_format)

		# Apply each rule
		for pattern, fmt in self.rules:
			for match in pattern.finditer(text):
				start, end = match.span(1) if match.lastindex else match.span()
				self.setFormat(start, end - start, fmt)


def apply_dark_mode(app):
	dark_stylesheet = """
	QWidget {
		background-color: #121212;
		color: #FFFFFF;
	}
	QTextEdit, QLineEdit {
		background-color: #1E1E1E;
		color: #D4D4D4;
		border: 1px solid #333;
	}
	QPushButton {
		background-color: #333;
		color: #FFFFFF;
		border: 1px solid #444;
		padding: 5px;
	}
	QPushButton:hover {
		background-color: #444;
	}
	QLabel {
		color: #FFFFFF;
	}
	QSlider::groove:horizontal {
		height: 6px;
		background: #444;
	}
	QSlider::handle:horizontal {
		background: #888;
		border: 1px solid #555;
		width: 14px;
		margin: -4px 0;
		border-radius: 7px;
	}
	QSpinBox {
		background-color: #1E1E1E;
		color: #D4D4D4;
		border: 1px solid #333;
	}
	"""
	app.setStyleSheet(dark_stylesheet)