import sys
from PyQt5.QtWidgets import (
	QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
	QTextEdit, QSlider, QHBoxLayout, QSpinBox
)
from PyQt5.QtCore import Qt
from sandbox import Sandbox

class AIApp(QWidget):
	def __init__(self):
		super().__init__()
        
		self.initUI()
		self.sandbox = Sandbox()  # Initialize the sandbox
		self.survivors = []  # List to store survivors' AI code
		self.input_box_text = [""]
		self.output_box_text = [""]
		self.input_box_selector["slider"].setMaximum(0)
		self.output_box_selector["spinbox"].setMaximum(0)


	def initUI(self):
        # Create UI components
		self.setWindowTitle("AI Evolution")
		self.setGeometry(100, 100, 600, 400)

		self.layout = QVBoxLayout()

		self.status_label = QLabel("Welcome to the AI Evolution System", self)
		self.layout.addWidget(self.status_label)

		self.input_box = QTextEdit(self)
		self.input_box.textChanged.connect(self.sync_input_box)
		self.layout.addWidget(self.input_box)

		self.input_box_selector = self.create_selector("AI index", self.on_parent_change)
		self.layout.addLayout(self.input_box_selector["layout"])

		self.run_button = QPushButton('Run Iteration', self)
		self.run_button.clicked.connect(self.run_iteration)
		self.layout.addWidget(self.run_button)

		self.output_box = QTextEdit(self)
		self.output_box.setReadOnly(True)
		self.layout.addWidget(self.output_box)

		self.output_box_selector = self.create_selector("Child Index", self.on_child_change)
		self.layout.addLayout(self.output_box_selector["layout"])

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


        # Settup the lists of texts for output and input boxes
		self.output_box_text.clear()
		for ai, validated, error_message, score in new_generation:
			result = f"AI: {ai}\n"
			result += f"Validated: {validated}\n"
			result += f"Error: {error_message if error_message else 'None'}\n"
			result += f"Score: {score}\n\n"
			self.output_box_text.append(result)
		
		self.input_box_text.clear()
		self.input_box_text[:] = [ai for ai, _, _, _ in new_generation[:int(self.sandbox.population_size / 2)]]
		

		# Set maximum index for the selectors
		for selector, data in [(self.input_box_selector, self.input_box_text), (self.output_box_selector, self.output_box_text)]:
			max_index = max(0, len(data) - 1)
			selector["slider"].setMaximum(max_index)
			selector["spinbox"].setMaximum(max_index)
		

		# Set selectors back to O
		self.on_parent_change(0)
		self.on_child_change(0)


		self.status_label.setText("Iteration completed!")
	

	def on_parent_change(self, index):
		if 0 <= index < len(self.input_box_text):
			code = self.input_box_text[index]
			self.input_box.setText(code)


	def on_child_change(self, index):
		if 0 <= index < len(self.output_box_text):
			code = self.output_box_text[index]
			self.output_box.setText(code)
	

	def sync_input_box(self):
		current_index = self.input_box_selector["spinbox"].value()
		if 0 <= current_index < len(self.input_box_text):
			self.input_box_text[current_index] = self.input_box.toPlainText()


def main():
	app = QApplication(sys.argv)
	ex = AIApp()
	ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()