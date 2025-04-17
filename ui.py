import sys

from PyQt5.QtWidgets import (
	QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
	QTextEdit, QSlider, QHBoxLayout, QSpinBox, QCheckBox
)
from PyQt5.QtCore import Qt

from sandbox import Sandbox
import ide



class AIApp(QWidget):
	def __init__(self):
		super().__init__()
        
		self.input_box_text = ["""import random

def mutate(code):
	lines = code.split("\\n")
	if lines:
		index = random.randint(0, len(lines) - 1)
		lines[index] += "" if len(lines[index]) == 0 else "  "
		lines[index] += "# mutation here!"
	return "\\n".join(lines)
"""]
		self.output_box_text = [""]

		self.dark_mode_enabled = True
		ide.apply_dark_mode(self)

		self.initUI()

		self.sandbox = Sandbox()

		self.input_box_selector["slider"].setMaximum(0)
		self.output_box_selector["spinbox"].setMaximum(0)
		
		self.survivors = []


	def initUI(self):
        # Window
		self.setWindowTitle("OuroboroAI")
		self.setGeometry(100, 100, 600, 400)

		# Main Layout
		self.layout = QVBoxLayout()

		# Create toolbox
		self.header_layout = QHBoxLayout()
		self.status_label = QLabel("Welcome to the AI Evolution System", self)
		self.header_layout.addWidget(self.status_label)
		self.header_layout.addStretch()
		self.theme_checkbox = QCheckBox("Dark Mode")
		self.theme_checkbox.setChecked(True)
		self.theme_checkbox.stateChanged.connect(self.toggle_dark_mode)
		self.header_layout.addWidget(self.theme_checkbox)
		self.layout.addLayout(self.header_layout)

		# TODO : Add save and load button, iteration display + selector, settings menu... that kinda stuff.

		# Input box
		self.input_box = ide.AutoIndentTextEdit(self)
		self.input_box.setText(self.input_box_text[0])
		self.input_box.textChanged.connect(self.sync_input_box)
		self.layout.addWidget(self.input_box)

		# Font
		self.input_box.setFont(ide.MonospaceFont())
		font_metrics = self.input_box.fontMetrics()
		tab_width = font_metrics.width(' ') * 4  # Tab width is 4 spaces
		self.input_box.setTabStopDistance(tab_width)

		# Syntax highlighter
		self.highlighter = ide.PythonHighlighter(self.input_box.document(), self.dark_mode_enabled, self)

		# Selector
		self.input_box_selector = self.create_selector("AI index", self.input_changed)
		self.layout.addLayout(self.input_box_selector["layout"])

		# Run Button
		self.run_button = QPushButton('Run Iteration', self)
		self.run_button.clicked.connect(self.run_iteration)
		self.layout.addWidget(self.run_button)

		# Output Box
		self.output_box = QTextEdit(self)
		self.output_box.setReadOnly(True)
		self.layout.addWidget(self.output_box)

		# Font
		self.output_box.setFont(ide.MonospaceFont())
		self.output_box.setTabStopDistance(tab_width)

		# Selector
		self.output_box_selector = self.create_selector("Child Index", self.output_changed)
		self.layout.addLayout(self.output_box_selector["layout"])

		# Main Layout
		self.setLayout(self.layout)


	def create_selector(self, label, callback):
		widgets = {}
		layout = QHBoxLayout()
		layout.addWidget(QLabel(label))

		spinbox = QSpinBox()
		spinbox.setMinimum(0)
		layout.addWidget(spinbox)

		slider = QSlider(Qt.Horizontal)
		slider.setMinimum(0)
		layout.addWidget(slider)

		slider.valueChanged.connect(spinbox.setValue)
		spinbox.valueChanged.connect(slider.setValue)
		spinbox.valueChanged.connect(callback)

		widgets["layout"] = layout
		widgets["slider"] = slider
		widgets["spinbox"] = spinbox
		return widgets


	def run_iteration(self):
		self.survivors[:] = self.input_box_text
		new_generation = self.sandbox.iteration(self.survivors)


        # Setup the lists of texts for output and input boxes
		self.output_box_text.clear()
		for ai, validated, error_message, score in new_generation:
			formatted_ai = ai.replace('\t', '    ')
			longest_line = max(ide.visual_length(line) for line in formatted_ai.splitlines())
			horizontal_line = "─" * (longest_line + 2)
			formatted_ai = "\n".join(f"│ {line}" + " " * (longest_line - ide.visual_length(line) + 1) + "│" for line in formatted_ai.splitlines())
			
			result = f"<b><u>AI</u>:</b><br>"
			result += f"┌{horizontal_line}┐<br>"
			result += f"<span style='font-family: monospace; white-space: pre;'>{formatted_ai}</span><br>"
			result += f"└{horizontal_line}┘<br>"
			if not validated:
				result += f"<b><u>Error</u>:</b> {error_message if error_message else 'None'}<br>"
			result += f"<b><u>Score</u>:</b> {score}"
			self.output_box_text.append(result)
		
		self.input_box_text.clear()
		self.input_box_text[:] = [ai for ai, _, _, _ in new_generation[:int(self.sandbox.population_size / 2)]]
		

		# Set maximum index for the selectors
		for selector, data in [(self.input_box_selector, self.input_box_text), (self.output_box_selector, self.output_box_text)]:
			max_index = max(0, len(data) - 1)
			selector["slider"].setMaximum(max_index)
			selector["spinbox"].setMaximum(max_index)
		

		# Set selectors back to O
		self.input_changed(0)
		self.output_changed(0)

		# Update status label
		self.status_label.setText("Iteration completed!")
	

	def input_changed(self, index):
		if 0 <= index < len(self.input_box_text):
			code = self.input_box_text[index]
			self.input_box.setText(code)


	def output_changed(self, index):
		if 0 <= index < len(self.output_box_text):
			code = self.output_box_text[index]
			self.output_box.setHtml(code)  # Because we format the output with HTML instead of normal (<b> stuff 'n' all)
	

	def sync_input_box(self):
		current_index = self.input_box_selector["spinbox"].value()
		if 0 <= current_index < len(self.input_box_text):
			self.input_box_text[current_index] = self.input_box.toPlainText()
	

	def toggle_dark_mode(self):
		self.dark_mode_enabled = self.theme_checkbox.isChecked()
		if self.dark_mode_enabled:
			ide.apply_dark_mode(self)
		else:
			self.setStyleSheet("")

		self.highlighter.set_dark_mode(self.dark_mode_enabled)



def main():
	app = QApplication(sys.argv)
	ex = AIApp()
	ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()