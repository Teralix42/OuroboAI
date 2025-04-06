import gc
import random

class Sandbox:
    def __init__(self):
        self.sandbox = {}
    
    
    #returns the AI's score
    #TODO : replace the placeholder with a real evaluation function
    def evaluate(self, ai_code: str) -> float:
        return random.uniform(0, 1)


    #returns a list of tuples representing the AI survivors, containing the code, if it's validated or not, the error message if not, and its score
    #TODO : also save the dumb AI's, somewhere else.
    def iteration(self, survivors: list[str], population_size: int = 10) -> list[tuple[str, float]]:
        new_generation = [(ai, True, None, 0) for ai in survivors]
        
        # Duplicate survivors to reach desired population
        while len(new_generation) < population_size:
            parent_code = random.choice(survivors)
            new_generation.append((parent_code, True, None, 0))
        
        for ai in range(len(new_generation)):
            child, validated, error_message = self.run_ai(new_generation[ai][0])
            new_generation[ai] = (child, validated, error_message, self.evaluate(child) if validated else 0)
        # Sort by score, highest first
        new_generation.sort(key=lambda x: x[3], reverse=True)
        
        # Return top performers (can tweak how many)
        return new_generation[:len(survivors)]


    #returns a tuple representing the mutated ai, containing the code, if it's validated or not, and the error message if not
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


    #returns a tuple representing the AI's validation, containing if it's validated or not and the error message if not
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