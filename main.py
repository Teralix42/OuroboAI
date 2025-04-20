import ide

ai_code = """
import random

def mutate(code):
	lines = code.split("\n")
	if lines:
		index = random.randint(0, len(lines) - 1)
		lines[index] += "  # mutated"
	return "\n".join(lines)
"""

heading = "Hello World!"
sub_boxes = [
    ("sub1", "hello"),
    ("sub2", "hi")
]

formatted_box = ide.create_box(heading, sub_boxes)
print(formatted_box)