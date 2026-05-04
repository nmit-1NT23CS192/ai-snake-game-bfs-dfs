import tkinter as tk
import random
from collections import deque

WIDTH = 400
HEIGHT = 400
CELL = 20

root = tk.Tk()
root.title("AI Snake Game using BFS and DFS")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

info_label = tk.Label(root, text="", font=("Arial", 12))
info_label.pack()

snake = [(100, 100)]
direction = "Right"
food = (200, 200)

score = 0
level = 1
speed = 150
running = True
paused = False
ai_mode = False
algorithm = "BFS"
move_job = None


def bfs(start, goal):
    queue = deque([(start, [])])
    visited = {start}
    snake_body = set(snake[1:])

    while queue:
        current, path = queue.popleft()

        if current == goal:
            return path + [current]

        x, y = current

        for dx, dy in [(CELL, 0), (-CELL, 0), (0, CELL), (0, -CELL)]:
            next_cell = (x + dx, y + dy)

            if (
                0 <= next_cell[0] < WIDTH and
                0 <= next_cell[1] < HEIGHT and
                next_cell not in visited and
                next_cell not in snake_body
            ):
                visited.add(next_cell)
                queue.append((next_cell, path + [current]))

    return []


def dfs(start, goal):
    stack = [(start, [])]
    visited = {start}
    snake_body = set(snake[1:])

    while stack:
        current, path = stack.pop()

        if current == goal:
            return path + [current]

        x, y = current

        for dx, dy in [(CELL, 0), (-CELL, 0), (0, CELL), (0, -CELL)]:
            next_cell = (x + dx, y + dy)

            if (
                0 <= next_cell[0] < WIDTH and
                0 <= next_cell[1] < HEIGHT and
                next_cell not in visited and
                next_cell not in snake_body
            ):
                visited.add(next_cell)
                stack.append((next_cell, path + [current]))

    return []


def draw():
    canvas.delete("all")

    for i, (x, y) in enumerate(snake):
        color = "lime" if i == 0 else "green"
        canvas.create_rectangle(x, y, x + CELL, y + CELL, fill=color)

    fx, fy = food
    canvas.create_oval(fx, fy, fx + CELL, fy + CELL, fill="red")


def place_food():
    global food

    while True:
        new_food = (
            random.randint(0, (WIDTH - CELL) // CELL) * CELL,
            random.randint(0, (HEIGHT - CELL) // CELL) * CELL
        )

        if new_food not in snake:
            food = new_food
            break


def update_label():
    mode = "AI" if ai_mode else "Manual"
    info_label.config(
        text=f"Score: {score} | Level: {level} | Mode: {mode} | Algorithm: {algorithm}"
    )


def move():
    global direction, score, level, speed, running, move_job

    if not running:
        return

    if paused:
        move_job = root.after(speed, move)
        return

    if ai_mode:
        path = bfs(snake[0], food) if algorithm == "BFS" else dfs(snake[0], food)

        if len(path) > 1:
            next_cell = path[1]
            dx = next_cell[0] - snake[0][0]
            dy = next_cell[1] - snake[0][1]

            if dx > 0:
                direction = "Right"
            elif dx < 0:
                direction = "Left"
            elif dy > 0:
                direction = "Down"
            elif dy < 0:
                direction = "Up"

    x, y = snake[0]

    if direction == "Up":
        y -= CELL
    elif direction == "Down":
        y += CELL
    elif direction == "Left":
        x -= CELL
    elif direction == "Right":
        x += CELL

    new_head = (x, y)

    if (
        x < 0 or x >= WIDTH or
        y < 0 or y >= HEIGHT or
        new_head in snake
    ):
        game_over()
        return

    snake.insert(0, new_head)

    if new_head == food:
        score += 1

        if score % 5 == 0:
            level += 1
            speed = max(50, speed - 10)

        place_food()
    else:
        snake.pop()

    update_label()
    draw()
    move_job = root.after(speed, move)


def change_direction(event):
    global direction

    if ai_mode:
        return

    if event.keysym == "Up" and direction != "Down":
        direction = "Up"
    elif event.keysym == "Down" and direction != "Up":
        direction = "Down"
    elif event.keysym == "Left" and direction != "Right":
        direction = "Left"
    elif event.keysym == "Right" and direction != "Left":
        direction = "Right"


def toggle_pause():
    global paused

    paused = not paused
    pause_btn.config(text="Resume" if paused else "Pause")


def toggle_ai():
    global ai_mode

    ai_mode = not ai_mode
    update_label()


def toggle_algorithm():
    global algorithm

    algorithm = "DFS" if algorithm == "BFS" else "BFS"
    update_label()


def restart():
    global snake, direction, score, level, speed, running, paused, move_job

    if move_job is not None:
        root.after_cancel(move_job)
        move_job = None

    snake = [(100, 100)]
    direction = "Right"
    score = 0
    level = 1
    speed = 150
    running = True
    paused = False

    pause_btn.config(text="Pause")
    place_food()
    update_label()
    draw()
    move()


def game_over():
    global running

    running = False
    canvas.create_text(
        WIDTH / 2,
        HEIGHT / 2,
        text="GAME OVER",
        fill="white",
        font=("Arial", 22, "bold")
    )


frame = tk.Frame(root)
frame.pack(pady=5)

pause_btn = tk.Button(frame, text="Pause", command=toggle_pause)
pause_btn.pack(side="left", padx=5)

tk.Button(frame, text="Restart", command=restart).pack(side="left", padx=5)
tk.Button(frame, text="Toggle AI", command=toggle_ai).pack(side="left", padx=5)
tk.Button(frame, text="Toggle BFS/DFS", command=toggle_algorithm).pack(side="left", padx=5)

root.bind("<KeyPress>", change_direction)

place_food()
update_label()
draw()
move()

root.mainloop()