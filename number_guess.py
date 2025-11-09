import random
import tkinter as tk
from tkinter import messagebox, ttk

class NumberGuessingGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎯 Number Guessing Game")
        self.geometry("420x380")
        self.configure(bg="#e6f2ff")  # Light blue background
        self.resizable(False, False)

        self.max_value = 100
        self.best_score = None
        self.new_game()

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="Guess the Number",
                               font=("Segoe UI", 18, "bold"),
                               bg="#e6f2ff", fg="#003366")
        title_label.pack(pady=15)

        # Range scale
        scale_frame = tk.Frame(self, bg="#e6f2ff")
        scale_frame.pack(pady=5)
        tk.Label(scale_frame, text="Max number:", bg="#e6f2ff",
                 fg="#003366", font=("Segoe UI", 10, "bold")).pack(side="left")
        self.range_scale = ttk.Scale(scale_frame, from_=10, to=1000,
                                     orient="horizontal", command=self.on_range_change, length=220)
        self.range_scale.set(self.max_value)
        self.range_scale.pack(side="left", padx=10)

        # Attempts info
        info_frame = tk.Frame(self, bg="#e6f2ff")
        info_frame.pack(pady=10)
        self.attempts_label = tk.Label(info_frame, text=f"Attempts: {self.attempts}",
                                       font=("Segoe UI", 10), bg="#e6f2ff", fg="#004080")
        self.attempts_label.pack(side="left", padx=10)
        self.best_label = tk.Label(info_frame, text=f"Best: {self.best_score if self.best_score else '-'}",
                                   font=("Segoe UI", 10), bg="#e6f2ff", fg="#004080")
        self.best_label.pack(side="right", padx=10)

        # Hint text
        self.hint_var = tk.StringVar(value="Enter a number and press Guess")
        hint_label = tk.Label(self, textvariable=self.hint_var,
                              font=("Segoe UI", 11, "italic"), bg="#e6f2ff", fg="#00264d")
        hint_label.pack(pady=10)

        # Guess entry
        entry_frame = tk.Frame(self, bg="#e6f2ff")
        entry_frame.pack(pady=5)
        self.guess_entry = ttk.Entry(entry_frame, width=15, font=("Segoe UI", 12))
        self.guess_entry.pack(side="left", padx=10)
        self.guess_entry.bind("<Return>", lambda e: self.check_guess())
        guess_btn = ttk.Button(entry_frame, text="Guess", command=self.check_guess)
        guess_btn.pack(side="left")

        # Buttons frame
        btn_frame = tk.Frame(self, bg="#e6f2ff")
        btn_frame.pack(pady=15)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton",
                        font=("Segoe UI", 11, "bold"),
                        padding=8,
                        background="#66b3ff",
                        foreground="black")
        style.map("TButton",
                  background=[("active", "#99ccff")])

        new_btn = ttk.Button(btn_frame, text="New Game", command=self.new_game_ui)
        new_btn.pack(side="left", padx=5)
        show_btn = ttk.Button(btn_frame, text="Show Range", command=self.show_range)
        show_btn.pack(side="left", padx=5)
        quit_btn = ttk.Button(btn_frame, text="Quit", command=self.quit)
        quit_btn.pack(side="left", padx=5)

    def on_range_change(self, val):
        self.max_value = int(float(val))

    def new_game(self):
        self.target = random.randint(1, self.max_value)
        self.attempts = 0
        self.game_over = False

    def new_game_ui(self):
        self.new_game()
        self.attempts_label.config(text=f"Attempts: {self.attempts}")
        self.hint_var.set("New game started! Enter a number.")
        self.guess_entry.config(state="normal")
        self.guess_entry.delete(0, tk.END)
        self.best_label.config(text=f"Best: {self.best_score if self.best_score else '-'}")

    def show_range(self):
        messagebox.showinfo("Range", f"Guess a number between 1 and {self.max_value}")

    def check_guess(self):
        if self.game_over:
            self.hint_var.set("Game over — start a new game.")
            return

        guess_text = self.guess_entry.get().strip()
        if not guess_text:
            self.hint_var.set("Please enter a number.")
            return

        try:
            guess = int(guess_text)
        except ValueError:
            self.hint_var.set("Not a valid number.")
            return

        if not 1 <= guess <= self.max_value:
            self.hint_var.set(f"Enter between 1 and {self.max_value}.")
            return

        self.attempts += 1
        self.attempts_label.config(text=f"Attempts: {self.attempts}")

        if guess == self.target:
            self.hint_var.set(f"🎉 Correct! The number was {self.target}.")
            messagebox.showinfo("Winner!", f"You guessed it in {self.attempts} tries!")
            self.game_over = True
            self.guess_entry.config(state="disabled")

            if self.best_score is None or self.attempts < self.best_score:
                self.best_score = self.attempts
                self.best_label.config(text=f"Best: {self.best_score}")
        elif guess < self.target:
            self.hint_var.set("Too low — try higher.")
        else:
            self.hint_var.set("Too high — try lower.")

        self.guess_entry.delete(0, tk.END)

if __name__ == "__main__":
    app = NumberGuessingGame()
    app.mainloop()
