import gc

class Sandbox:
    def __init__(self):
        self.sandbox = {}


    def run_ai(self, ai_code: str) -> tuple[str | None, bool, str | None]:
        self.sandbox = {}
        gc.collect()

        exec(ai_code, self.sandbox)
        try:
            mutated_code = self.sandbox["mutate"](ai_code)

            validation, error_message = self.validate(mutated_code)
            return mutated_code, validation, error_message
        
        except Exception as e:
            return None, False, f"Error during mutation execution: {e}"


    def validate(self, ai_code: str) -> tuple[bool, str]:
        if "global" in ai_code or "del" in ai_code:
            return False, "Error: uses global or delete"
        try:
            exec(ai_code, self.sandbox)

            if "mutate" in self.sandbox and callable(self.sandbox["mutate"]):
                return True, None
            else:
                return False, "Error: No 'mutate' function found in AI code."
        except Exception as e:
            return False, f"Error during execution: {e}"
