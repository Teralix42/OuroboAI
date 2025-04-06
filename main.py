from sandbox import Sandbox as sandbox

ai_code = """
def mutate(ai_code: str):
    new_code = ai_code + "\n# A new line!"
    return new_code
"""

result = sandbox.run_ai(ai_code)
print("Code not runnable" if result == None else result)