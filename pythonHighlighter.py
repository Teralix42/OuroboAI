from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
import re

class PythonHighlighter(QSyntaxHighlighter):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.rules = []

		def fmt(color, bold=False, italic=False):
			f = QTextCharFormat()
			f.setForeground(QColor(color))
			if bold:
				f.setFontWeight(QFont.Bold)
			if italic:
				f.setFontItalic(True)
			return f

		# Define formats
		string_fmt = fmt("#FFA500")         # Orange for strings
		comment_fmt = fmt("#4CAF50", italic=True) # Green for comments
		def_class_kw_fmt = fmt("#1E3A8A", bold=True)  # Dark blue for def/class
		control_kw_fmt = fmt("#8A2BE2")     # Purplish for flow control/import
		bracket_fmt = fmt("#FFD700")        # Yellow for brackets
		class_imported_fmt = fmt("#9CCC65", bold=True)  # Light green for class names & modules
		func_name_fmt = fmt("#FFF176", bold=True) # Yellowish for function names

		# String literals
		self.rules.append((re.compile(r'"[^"\\]*(\\.[^"\\]*)*"'), string_fmt))
		self.rules.append((re.compile(r"'[^'\\]*(\\.[^'\\]*)*'"), string_fmt))

		# Comments
		self.rules.append((re.compile(r"#.*"), comment_fmt))

		# def / class keywords
		for word in ["def", "class"]:
			self.rules.append((re.compile(rf"\b{word}\b"), def_class_kw_fmt))

		# control flow + import
		control_keywords = ["if", "else", "elif", "for", "in", "return", "from", "import", "as"]
		for word in control_keywords:
			self.rules.append((re.compile(rf"\b{word}\b"), control_kw_fmt))

		# Brackets
		for b in ["\(", "\)", "\[", "\]", "\{", "\}"]:
			self.rules.append((re.compile(b), bracket_fmt))

		# Class names
		self.rules.append((re.compile(r"class\s+([A-Za-z_][A-Za-z0-9_]*)"), class_imported_fmt))

		# Function names
		self.rules.append((re.compile(r"def\s+([A-Za-z_][A-Za-z0-9_]*)"), func_name_fmt))

		# Imported modules
		self.rules.append((re.compile(r"import\s+([A-Za-z_][A-Za-z0-9_\.]*)"), class_imported_fmt))
		self.rules.append((re.compile(r"from\s+([A-Za-z_][A-Za-z0-9_\.]*)"), class_imported_fmt))

	def highlightBlock(self, text):
		# Set whole block default format to white first
		plain_format = QTextCharFormat()
		plain_format.setForeground(QColor("white"))
		self.setFormat(0, len(text), plain_format)

		# Then apply all custom formats
		for pattern, fmt in self.rules:
			for match in pattern.finditer(text):
				start, end = match.span(1) if match.lastindex else match.span()
				self.setFormat(start, end - start, fmt)