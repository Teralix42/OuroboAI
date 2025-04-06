# 🧠 OuroboAI

Welcome to **OuroboAI** — a lightweight Python-based framework for building **self-evolving AIs**.  
This project is a work-in-progress **Recursive Self-Improving system (RSI)** where AIs mutate their own code, get evaluated, and evolve over time.

---

## 🚀 Features

- ✍️ **Self-Modifying AI**  
  Each AI defines its own `mutate` function, allowing it to modify its own source code.

- 🧪 **Sandboxed Execution**  
  AI code is executed in a clean sandbox to prevent malicious or invalid behavior. No globals. No deletes. No funny business.

- 📈 **Evolutionary Algorithm**  
  At each iteration:
  - Each AI generates a new one, ideally a better version of itself.
  - Valid AIs are evaluated and scored.
  - The best are kept and duplicated; the rest are *yeeted*.

- 🖥️ **PyQt5 GUI**  
  Simple interface to input AI code, view mutations, and watch evolution in action.

---

## 🛠 How It Works

1. You give it an initial AI with a `mutate(code: str) -> str` function.
2. The sandbox runs the code, executes `mutate`, and checks that it returns a valid new AI.
3. Each valid mutation is evaluated with a placeholder `evaluate()` function for now.
4. The top scorers become the next generation.

> It's basically natural selection... but with Python code.

---

## 🧪 Evaluation

Evaluation is currently random (`random.uniform(0, 1)`) — **you can and should replace this** with your own scoring logic based on the AI’s behavior or goals.

---

## 🛡 Validation Rules

To keep things safe and sane, AIs that:
- Use `global` or `del`
- Don’t define a valid `mutate()` function
- Crash during execution

...are **rejected**. Dumb AIs may be logged in the future, just for laughs.

---

## 🧠 What's an RSI?

This project is a simple prototype of a **Recursive Self-Improving (RSI)** system.  
RSIs are systems that can:
- Modify their own code
- Improve with each generation
- Choose the "fittest" versions to continue evolving

This framework lays the groundwork for those concepts in a contained and fun environment.

---

## 💻 Requirements

- Python 3.10+
- PyQt5 (`pip install pyqt5`)

---

## 🗂 Project Structure

project-root/ ├── main.py # Launches the GUI ├── sandbox.py # Handles mutation, validation, evaluation, and iteration logic └── README.md # You're reading this!

---

## 🧙‍♂️ Author

Crafted by **NeilAnami22**, possibly a 52 years old fat dude named chuck that lives in his moms garage, but maybe not.  
Helper: ChatGPT (I'm mostly here drinking coffee while it does the real work).

---

## 📝 TODO

- Replace `evaluate()` with actual evaluation logic
- Save invalid ("dumb") AIs for analysis/fun
- Add logging and error tracking
- Expand UI for more control

---

## ⚠️ Disclaimer

This project is for educational and experimental purposes. It is **not intended** to make superintelligent rogue AIs... yet. 😉
