import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from sandbox import Sandbox as sandbox

class AIApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.sandbox = sandbox()  # Initialize the sandbox
        self.survivors = []  # List to store survivors' AI code

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
        # Get the code from the input area
        ai_code = self.code_input.toPlainText()

        # Add the current AI code as a survivor (for the first iteration, it's the starting point)
        if not self.survivors:
            self.survivors.append(ai_code)

        # Run the iteration with the current survivors
        new_generation = self.sandbox.iteration(self.survivors)

        # Clear the result output area
        self.result_output.clear()

        # Display the results: AI code, validation status, error message, and score
        for ai, validated, error_message, score in new_generation:
            result = f"AI: {ai}\n"
            result += f"Validated: {validated}\n"
            result += f"Error: {error_message if error_message else 'None'}\n"
            result += f"Score: {score}\n\n"
            self.result_output.append(result)

        # Update the survivors with the top AI codes for the next iteration
        # The survivors list will hold the top performers from the new generation
        self.survivors = [ai for ai, _, _, _ in new_generation[:len(self.survivors)]]

        # Overwrite the code input with the mutated code of the top performer
        top_performer_code = new_generation[0][0]  # Get the AI code of the top performer
        self.code_input.setText(top_performer_code)

        self.status_label.setText("Iteration completed!")

def main():
    app = QApplication(sys.argv)
    ex = AIApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()