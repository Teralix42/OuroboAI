from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor, QFont, QFontDatabase
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import Qt

import re

font = "Consolas"

class PythonHighlighter(QSyntaxHighlighter):
	def __init__(self, document, dark_mode, app):
		super().__init__(document)

		self.rules = []
		self.app = app
		self.dark_mode_enabled = dark_mode

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
		# Default color
		default_format = QTextCharFormat()
		default_format.setForeground(QColor("white" if self.app.dark_mode_enabled else "black"))
		self.setFormat(0, len(text), default_format)

		# Apply each rule
		for pattern, fmt in self.rules:
			for match in pattern.finditer(text):
				start, end = match.span(1) if match.lastindex else match.span()
				self.setFormat(start, end - start, fmt)
	
	def set_dark_mode(self, enabled):
		self.dark_mode_enabled = enabled
		self.rehighlight()



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


# Cascadia Code; Cascadia Mono; 
def set_font(font):
	monospace_font = QFont(font if font in QFontDatabase().families() else "Consolas")
	monospace_font.setStyleHint(QFont.Monospace)
	monospace_font.setFixedPitch(True)
	monospace_font.setPointSize(10)
	return monospace_font

class AutoIndentTextEdit(QTextEdit):
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
			cursor = self.textCursor()
			cursor.insertText("\n" + self.get_previous_indent())
			return  # Skip default behavior

		if event.key() == Qt.Key_Space:
			cursor = self.textCursor()
			cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 3)  # look at last 3 before current

			if cursor.selectedText() == "   ":
				cursor.removeSelectedText()  # delete last 3
				cursor.insertText("\t")  # insert tab instead
				return

		super().keyPressEvent(event)
	
	def insertFromMimeData(self, source): # Pasting
		text = source.text()
		# Replace leading groups of four spaces with tabs for each line
		converted_text = re.sub(r'^( {4})+', lambda m: '\t' * (len(m.group(0)) // 4), text, flags=re.MULTILINE)
		cursor = self.textCursor()
		cursor.insertText(converted_text)

	def get_previous_indent(self):
		cursor = self.textCursor()
		cursor.movePosition(QTextCursor.StartOfBlock)
		prev_line = cursor.block().text()
		indent = re.match(r'^\t*', prev_line).group()

		if prev_line.strip().endswith(":"):
			indent += "\t"

		if not prev_line:
			return ""
		return indent


# takes main heading as str, and sub_boxes as a list of tuples(Each tuple contains a heading and the box's content).
def create_box(heading, sub_boxes):

	def strip_html_tags(text):
			"""Removes HTML tags from a string."""
			return re.sub(r"<[^>]*>", "", text)

	# Determine the width of the boxes based on the longest line in the content
	contents = []
	headings = [heading]
	for sub_heading, content in sub_boxes:
		contents.extend(content.splitlines()) # Extend, because it takes not 1 but multiple values
		headings.append(sub_heading + "    ")
	longest_line = max(len(line) for line in contents) if contents else 1
	longest_heading = max(len(heading) for heading in headings) if headings else 1
	main_box_width = max(longest_line + 6, longest_heading + 2)
	sub_box_width = main_box_width - 4

	# Create the top of the box
	result = f"╔{'═' * main_box_width}╗<br>"
	result += f"║{' ' * ((main_box_width - len(heading)) // 2)}<b><u>{heading}</b></u>{' ' * ((main_box_width - len(heading) + 1) // 2)}║<br>"
	result += f"╠{'═' * main_box_width}╣<br>"

	# Add each sub-box
	for sub_heading, content in sub_boxes:
		# Sub-box heading
		result += f"║ ┌─╴<b>{sub_heading}</b>╶{'─' * (sub_box_width - len(sub_heading) - 3)}┐ ║<br>"
		# Sub-box content
		for line in content.splitlines():
			stripped_line = strip_html_tags(line)
			result += f"║ │ {line}{' ' * (sub_box_width - len(stripped_line) - 1)}│ ║<br>"
		result += f"║ └{'─' * (sub_box_width)}┘ ║<br>"

	# Create the bottom of the box
	result += f"╚{'═' * main_box_width}╝"

	# Replace spaces with non-breaking spaces for HTML formatting
	result = result.replace(" ", "&nbsp;")

	return result