import sys
import json
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextOption
from PyQt5.QtWidgets import (
	QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
	QTextEdit, QSlider, QHBoxLayout, QSpinBox, QCheckBox, QInputDialog
)

from sandbox import Sandbox
import ide



class AIApp(QWidget):
	def __init__(self, original):
		super().__init__()
		
		os.makedirs("sessions", exist_ok=True)
        
		self.iteration = 1
		self.input_box_text = [original]
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
		self.setGeometry(100, 100, 750, 500)

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

		self.save_button = QPushButton("📝 Save")
		self.save_button.clicked.connect(self.save_session)
		self.header_layout.addWidget(self.save_button)

		self.load_button = QPushButton("📄 Load")
		self.load_button.clicked.connect(self.load_session)
		self.header_layout.addWidget(self.load_button)

		self.layout.addLayout(self.header_layout)

		# TODO : Add settings menu and other tools

		# Input box
		self.input_box = ide.AutoIndentTextEdit(self)
		self.input_box.setText(self.input_box_text[0])
		self.input_box.textChanged.connect(self.sync_input_box)
		self.input_box.setWordWrapMode(QTextOption.NoWrap)  # Disable text wrapping
		self.layout.addWidget(self.input_box)

		# Font
		self.input_box.setFont(ide.set_font(ide.font))
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
		self.output_box.setWordWrapMode(QTextOption.NoWrap)  # Disable text wrapping
		self.layout.addWidget(self.output_box)

		# Font
		self.output_box.setFont(ide.set_font(ide.font))
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
		for i, (ai, validated, error_message, score) in enumerate(new_generation, start=1):
			formatted_ai = ai.replace('\t', '    ')
			
			heading = f"ITERATION-{self.iteration}-{i}"
			sub_boxes = [
				("Output", formatted_ai),
				("Evaluation", f"""<u>Validation</u>:       {"Success" if validated else "Failed"}
<u>Score</u>:            {score}
<u>Error</u>:            {error_message if not validated else "None"}"""),
			]

			result = ide.create_box(heading, sub_boxes)
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
		self.status_label.setText(f"Iteration {self.iteration} completed!")
		self.iteration += 1
	

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
	

	def save_session(self):
		dialog = CustomInputDialog(self, "Save session", "Enter session name:", ok_text="Save", cancel_text="Cancel")
		name, ok = dialog.exec_()
		if not ok or not name:
			self.status_label.setText(f"Save cancelled")
			return

		data = {
			"iteration": self.iteration,
			"input_box_text": self.input_box_text,
			"survivors": self.survivors
		}

		with open(f"sessions/{name}.json", "w") as f:
			json.dump(data, f, indent=4)

		self.status_label.setText(f"Session '{name}' saved.")


	def load_session(self):
		files = [f[:-5] for f in os.listdir("sessions") if f.endswith(".json")]
		if not files:
			self.status_label.setText("No saved sessions.")
			return

		dialog = CustomInputDialog(
			self,
			title="Load Session",
			label="Select session:",
			ok_text="Load",
			cancel_text="Cancel",
			items=files
		)

		value, accepted = dialog.exec_()
		if not accepted:
			self.status_label.setText(f"Loading cancelled.")
			return
		name = value
		path = f"sessions/{name}.json"

		if not os.path.exists(path):
			self.status_label.setText(f"Session '{name}' not found.")
			return

		with open(path, "r") as f:
			data = json.load(f)

		self.iteration = data.get("iteration", 1)
		self.input_box_text = data.get("input_box_text", [""])
		self.survivors = data.get("survivors", [])

		# Update selectors
		for selector, data_list in [(self.input_box_selector, self.input_box_text)]:
			max_index = max(0, len(data_list) - 1)
			selector["slider"].setMaximum(max_index)
			selector["spinbox"].setMaximum(max_index)

		self.input_changed(0)
		self.status_label.setText(f"Session '{name}' loaded (Iteration {self.iteration}).")


class CustomInputDialog(QInputDialog):
    def __init__(self, parent=None, title="", label="", ok_text="OK", cancel_text="Cancel", items=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setLabelText(label)

        if items is not None:
            self.setComboBoxItems(items)

        # Correctly set input mode
        self.setInputMode(QInputDialog.TextInput)  # Or QInputDialog.ComboBox if needed

        # Customize button texts
        self.setOkButtonText(ok_text)
        self.setCancelButtonText(cancel_text)

    def exec_(self):
        result = super().exec_()
        if self.inputMode() == QInputDialog.TextInput:
            return self.textValue(), result == QInputDialog.Accepted
        else:
            return self.currentText(), result == QInputDialog.Accepted


def main(original="""import random

def mutate(code):
	lines = code.split("\\n")
	if lines:
		index = random.randint(0, len(lines) - 1)
		lines[index] += "" if len(lines[index]) == 0 else "  "
		lines[index] += "# mutation here!"
	return "\\n".join(lines)
"""):
	QApplication.setStyle("Fusion")
	app = QApplication(sys.argv)
	ex = AIApp(original)
	ex.show()
	sys.exit(app.exec_())