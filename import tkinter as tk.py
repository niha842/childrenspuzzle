import tkinter as tk
from tkinter import messagebox
import random
import time
import math

class MemoryGame:
    def _init_(self, root):
        self.root = root
        self.root.title("Memory Matching Game")
        self.root.config(bg="#090909")  # Background
        self.root.attributes('-fullscreen', True)

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.cards_frame = tk.Frame(self.root, bg="#34495E")
        self.cards_frame.place(relx=0.5, rely=0.55, anchor="center")

        self.emojis = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.cards = self.emojis * 2
        random.shuffle(self.cards)

        self.buttons = []
        self.flipped = []
        self.matched = set()
        self.moves = 0
        self.start_time = None
        self.timer_running = False

        self.match_colors = [
            "#e74c3c", "#f39c12", "#8e44ad", "#27ae60",
            "#2980b9", "#d35400", "#c0392b", "#16a085"
        ]

        emoji_size = max(20, int(self.width / 30))
        self.font_emoji = ("Segoe UI Emoji", emoji_size)
        self.font_label = ("Segoe UI", 18, "bold")

        self.info_frame = tk.Frame(self.root, bg="#1B2631")
        self.info_frame.pack(pady=30)

        self.move_label = tk.Label(self.info_frame, text="Moves: 0", fg="white", bg="#1B2631", font=self.font_label)
        self.move_label.grid(row=0, column=0, padx=40)

        self.timer_label = tk.Label(self.info_frame, text="Time: 0s", fg="white", bg="#1B2631", font=self.font_label)
        self.timer_label.grid(row=0, column=1, padx=40)

        self.restart_btn = tk.Button(self.info_frame, text="Restart", command=self.restart_game, font=self.font_label,
                                     bg="#E67E22", fg="white", activebackground="#D35400", padx=20, pady=8)
        self.restart_btn.grid(row=0, column=2, padx=40)

        self.exit_btn = tk.Button(self.info_frame, text="Exit", command=self.confirm_exit, font=self.font_label,
                                  bg="#C0392B", fg="white", activebackground="#922B21", padx=20, pady=8)
        self.exit_btn.grid(row=0, column=3, padx=40)

        self.root.protocol("WM_DELETE_WINDOW", self.confirm_exit)
        self.root.bind("<Escape>", lambda e: self.confirm_exit())

        self.create_board()
        self.update_timer()

    def create_board(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        self.buttons.clear()

        btn_size = max(80, int(self.width / 20))
        padding = int(btn_size * 0.15)

        for i in range(4):
            for j in range(4):
                idx = i * 4 + j
                btn = tk.Button(self.cards_frame, text="❓", font=self.font_emoji,
                                width=2, height=1,
                                command=lambda idx=idx: self.flip_card(idx),
                                bg="#1ABC9C", fg="white", relief="raised", bd=6)
                btn.grid(row=i, column=j, padx=padding, pady=padding, ipadx=btn_size // 8, ipady=btn_size // 8)
                self.buttons.append(btn)

        self.flipped.clear()
        self.matched.clear()
        self.moves = 0
        self.move_label.config(text=f"Moves: {self.moves}")

        self.start_time = time.time()
        self.timer_running = True
        self.timer_label.config(text="Time: 0s")

    def flip_card(self, idx):
        if idx in self.matched or idx in self.flipped or len(self.flipped) == 2:
            return

        btn = self.buttons[idx]
        btn.config(text=self.cards[idx], bg="#16A085", fg="white", relief="raised")

        self.flipped.append(idx)

        if len(self.flipped) == 2:
            self.root.after(600, self.check_match)

    def check_match(self):
        idx1, idx2 = self.flipped
        if self.cards[idx1] == self.cards[idx2]:
            color_idx = len(self.matched) // 2 % len(self.match_colors)
            color = self.match_colors[color_idx]

            self.matched.add(idx1)
            self.matched.add(idx2)

            self.animate_match(idx1, idx2, color)
        else:
            for idx in self.flipped:
                self.buttons[idx].config(text="❓", bg="#1ABC9C", fg="white", relief="raised")
        self.flipped.clear()
        self.moves += 1
        self.move_label.config(text=f"Moves: {self.moves}")

        if len(self.matched) == 16:
            self.timer_running = False
            self.show_win()

    def animate_match(self, idx1, idx2, color):
        def pulse(count=0):
            if count > 6:
                for i in (idx1, idx2):
                    self.buttons[i].config(bg=color, fg="white", relief="sunken")
                return
            col = "white" if count % 2 == 0 else color
            for i in (idx1, idx2):
                self.buttons[i].config(bg=col, fg="white", relief="raised")
            self.root.after(150, pulse, count + 1)
        pulse()

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed}s")
        self.root.after(1000, self.update_timer)

    def show_win(self):
        elapsed = int(time.time() - self.start_time)
        msg = f"🎉 Congratulations! You won in {self.moves} moves and {elapsed} seconds! 🎉"
        self.confetti_animation()
        self.root.after(1800, lambda: messagebox.showinfo("You Win!", msg))

    def confetti_animation(self):
        canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="#1B2631", highlightthickness=0)
        canvas.place(x=0, y=0)

        colors = ["#E74C3C", "#F1C40F", "#3498DB", "#9B59B6", "#1ABC9C", "#E67E22", "#2ECC71", "#9B59B6"]

        confetti = []
        for _ in range(200):
            x = random.uniform(0, self.width)
            y = random.uniform(-self.height, 0)
            size = random.uniform(7, 15)
            color = random.choice(colors)
            shape = random.choice(['oval', 'rect', 'triangle'])
            speed = random.uniform(2, 6)
            angle = random.uniform(0, 2 * math.pi)
            confetti.append([x, y, size, color, shape, speed, angle])

        def draw_triangle(c, x, y, size, color):
            points = [x, y,
                      x + size / 2, y + size,
                      x - size / 2, y + size]
            c.create_polygon(points, fill=color, outline="")

        def fall():
            canvas.delete("all")
            for i, (x, y, size, color, shape, speed, angle) in enumerate(confetti):
                y += speed
                x += math.sin(angle) * 2
                angle += 0.1
                if y > self.height:
                    y = random.uniform(-50, 0)
                    x = random.uniform(0, self.width)
                    angle = random.uniform(0, 2 * math.pi)
                confetti[i] = [x, y, size, color, shape, speed, angle]

                if shape == 'oval':
                    canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")
                elif shape == 'rect':
                    canvas.create_rectangle(x, y, x + size, y + size, fill=color, outline="")
                else:
                    draw_triangle(canvas, x + size / 2, y, size, color)

                if random.random() < 0.05:
                    spark_x = x + random.uniform(0, size)
                    spark_y = y + random.uniform(0, size)
                    canvas.create_oval(spark_x, spark_y, spark_x + 3, spark_y + 3, fill="white", outline="")

            if not self.timer_running:
                self.root.after(50, fall)
            else:
                canvas.destroy()

        fall()

    def restart_game(self):
        random.shuffle(self.cards)
        self.create_board()
        self.start_time = time.time()
        self.timer_running = True

    def confirm_exit(self):
        if messagebox.askyesno("Exit Game", "Are you sure you want to quit the game?"):
            self.root.destroy()

if _name_ == "_main_":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()