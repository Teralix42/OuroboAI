import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from sandbox import Sandbox as sandbox

class AIApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.sandbox = sandbox()  # Initialize the sandbox


    def initUI(self):
        # Create UI components
        self.setWindowTitle("AI Evolution")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.status_label = QLabel("Welcome to the AI Evolution System", self)
        self.layout.addWidget(self.status_label)

        self.code_input = QTextEdit(self)
        self.layout.addWidget(self.code_input)

        self.run_button = QPushButton('Run Iteration', self)
        self.run_button.clicked.connect(self.run_iteration)
        self.layout.addWidget(self.run_button)

        self.result_output = QTextEdit(self)
        self.result_output.setReadOnly(True)
        self.layout.addWidget(self.result_output)

        self.setLayout(self.layout)


    def run_iteration(self):
	    # Get code from input area
        ai_code = self.code_input.toPlainText()

        # Run the AI through the sandbox
        mutated_code, validation, error_message = self.sandbox.run_ai(ai_code)

        if validation and mutated_code:
		    # If valid, display it in both result and overwrite input box for next iter
            self.result_output.setText(mutated_code)
            self.code_input.setText(mutated_code)
            self.status_label.setText("Mutation successful!")
        else:
		    # If invalid, show the error message and keep original input
            self.result_output.setText(error_message)
            self.status_label.setText("Error during mutation!")


def main():
    app = QApplication(sys.argv)
    ex = AIApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()