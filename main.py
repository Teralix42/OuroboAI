from sandbox import Sandbox as sandbox

ai_code = """
import random

def mutate(code):
	lines = code.split("\n")
	if lines:
		index = random.randint(0, len(lines) - 1)
		lines[index] += "  # mutated"
	return "\n".join(lines)
"""

result = sandbox.run_ai(ai_code)
print("Code not runnable" if result == None else result)