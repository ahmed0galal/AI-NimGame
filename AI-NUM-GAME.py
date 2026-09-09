import tkinter as tk
from tkinter import messagebox

class NimGame:
    def init(self, root):
        self.root = root
        self.root.title("AI Nim Game")

        self.sticks = 20
        self.memo = {}
        self.ai_thinking = False

        # UI
        self.label = tk.Label(root, text="", font=("Arial", 35, "bold"))
        self.label.pack(pady=10)

        self.status = tk.Label(root, text="Your turn", fg="blue")
        self.status.pack()

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.buttons = []
        for i in range(1, 4):
            btn = tk.Button(
                btn_frame,
                text=f"Take {i}",
                width=8,
                command=lambda x=i: self.player_move(x)
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.buttons.append(btn)

        tk.Button(root, text="Restart", command=self.reset).pack(pady=10)

        self.update()

    # ---------- Minimax ----------
    def minimax(self, sticks, is_max):
        if sticks == 0:
            return -1 if is_max else 1

        if (sticks, is_max) in self.memo:
            return self.memo[(sticks, is_max)]

        if is_max:
            best = -float("inf")
            for i in range(1, 4):
                if i <= sticks:
                    best = max(best, self.minimax(sticks - i, False))
        else:
            best = float("inf")
            for i in range(1, 4):
                if i <= sticks:
                    best = min(best, self.minimax(sticks - i, True))

        self.memo[(sticks, is_max)] = best
        return best

    # ---------- Player ----------
    def player_move(self, move):
        if self.ai_thinking or move > self.sticks:
            return

        self.sticks = max(0, self.sticks - move)
        self.update()

        if self.sticks == 0:
            return self.end("You Win!")

        self.ai_thinking = True
        self.lock_buttons(True)

        self.status.config(text="AI thinking...")
        self.root.after(400, self.ai_move)

    # ---------- AI ----------
    def ai_move(self):
        best_move = 1
        best_score = -float("inf")

        for i in range(1, 4):
            if i <= self.sticks:
                score = self.minimax(self.sticks - i, False)
                if score > best_score:
                    best_score = score
                    best_move = i

        self.sticks = max(0, self.sticks - best_move)
        self.update()

        if self.sticks == 0:
            return self.end("AI Wins!")

        self.ai_thinking = False
        self.lock_buttons(False)
        self.status.config(text="Your turn")

    # ---------- Safety ----------
    def lock_buttons(self, state):
        for b in self.buttons:
            b.config(state="disabled" if state else "normal")

    # ---------- Utils ----------
    def update(self):
        self.label.config(text=str(self.sticks))

    def end(self, msg):
        self.lock_buttons(True)
        messagebox.showinfo("Game Over", msg)
        self.reset()

    def reset(self):
        self.sticks = 20
        self.memo.clear()
        self.ai_thinking = False
        self.lock_buttons(False)
        self.update()
        self.status.config(text="Your turn")

if name == "main":
    root = tk.Tk()
    root.geometry("320x300")
    NimGame(root)
    root.mainloop()