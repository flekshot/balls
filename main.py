from tkinter import *
import time
import random
import threading

class Ball:
    def __init__(self, canvas, platform, score_label):
        self.canvas = canvas
        self.platform = platform
        self.score_label = score_label
        self.oval = canvas.create_oval(200, 200, 215, 215, fill='red')
        self.dir = [-3, -2, -1, 1, 2, 3]
        self.x = random.choice(self.dir)
        self.y = -3
        self.touch_bottom = False
        self.score = 0

    def touch_platform(self, ball_pos):
        platform_pos = self.canvas.coords(self.platform.rect)
        if (ball_pos[2] >= platform_pos[0] and ball_pos[0] <= platform_pos[2]) and \
           (ball_pos[3] >= platform_pos[1] and ball_pos[3] <= platform_pos[3] + 5):
            return True
        return False

    def draw(self):
        self.canvas.move(self.oval, self.x, self.y)
        pos = self.canvas.coords(self.oval)

        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= 400:
            self.touch_bottom = True
        if self.touch_platform(pos):
            self.y = -3
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")

        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= 500:
            self.x = -3

class Platform:
    def __init__(self, canvas):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(230, 300, 330, 310, fill='green')
        self.x = 0
        self.canvas.bind_all('<KeyPress-Left>', self.left)
        self.canvas.bind_all('<KeyPress-Right>', self.right)

    def left(self, event):
        self.x = -4

    def right(self, event):
        self.x = 4

    def draw(self):
        self.canvas.move(self.rect, self.x, 0)
        pos = self.canvas.coords(self.rect)
        if pos[0] <= 0 or pos[2] >= 500:
            self.x = 0

def countdown(label, game_time=30):
    for t in range(game_time, -1, -1):
        label.config(text=f"Time: {t}s")
        time.sleep(1)
    global running
    running = False


window = Tk()
window.title("Аркада")
window.resizable(0, 0)
window.wm_attributes("-topmost", 1)
window.config(bg="white")
canvas = Canvas(window, width=500, height=400)
canvas.pack()


score_label = Label(window, text="Score: 0", font=("Arial", 12))
score_label.pack()

time_label = Label(window, text="Time: 30s", font=("Arial", 12))
time_label.pack()

platform = Platform(canvas)
ball = Ball(canvas, platform, score_label)

running = True
timer_thread = threading.Thread(target=countdown, args=(time_label,))
timer_thread.start()


while running:
    if not ball.touch_bottom:
        ball.draw()
        platform.draw()
    else:
        break

    window.update()
    time.sleep(0.01)

canvas.create_text(250, 200, text="Game Over", font=("Arial", 20), fill="red")
window.update()

window.mainloop()
