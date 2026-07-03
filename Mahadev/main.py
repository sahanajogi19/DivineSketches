import turtle
import json
import time
import os
import math

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_FILE = os.path.join(BASE_DIR, "mahakal_paths.json")

PENCIL_DELAY = 0
NEON_DELAY = 0
UPDATE_EVERY_POINTS = 120

PENCIL_DARK = (77, 77, 77)
PENCIL_WHITE = (255, 255, 255)
BLUE_GLOW = (0, 109, 255)
BLUE_MAIN = (0, 183, 255)
BLUE_BRIGHT = (143, 243, 255)

screen = turtle.Screen()
screen.setup(width=1.0, height=1.0)
screen.bgcolor("black")
screen.title("Mahadev Sketch")
screen.colormode(255)
screen.tracer(0, 0)

t = turtle.Turtle()
t.hideturtle()
t.speed(0)


def clean_point(point):
    try:
        if not isinstance(point, (list, tuple)) or len(point) < 2:
            return None

        x = float(point[0])
        y = float(point[1])

        if not math.isfinite(x) or not math.isfinite(y):
            return None

        return x, y
    except:
        return None


def clean_path(path):
    if not isinstance(path, list):
        return []

    cleaned = []
    for point in path:
        fixed = clean_point(point)
        if fixed is not None:
            cleaned.append(fixed)

    return cleaned


def load_paths():
    if not os.path.exists(PATH_FILE):
        raise FileNotFoundError(f"File not found: {PATH_FILE}")

    with open(PATH_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "paths" not in data:
        raise KeyError("JSON must contain 'paths'")

    paths = []
    for path in data["paths"]:
        cleaned = clean_path(path)
        if len(cleaned) >= 2:
            paths.append(cleaned)

    if not paths:
        raise ValueError("No valid paths found.")

    return paths


def fit_screen_to_paths(paths):
    all_x = []
    all_y = []

    for path in paths:
        for x, y in path:
            all_x.append(x)
            all_y.append(y)

    min_x = min(all_x)
    max_x = max(all_x)
    min_y = min(all_y)
    max_y = max(all_y)

    padding_x = 100
    padding_y = 100

    screen.setworldcoordinates(
        min_x - padding_x,
        min_y - padding_y,
        max_x + padding_x,
        max_y + padding_y
    )


def draw_path(path, color, width, delay):
    if len(path) < 2:
        return

    t.pencolor(color)
    t.pensize(width)

    t.penup()
    t.goto(path[0][0], path[0][1])
    t.pendown()

    for i, (x, y) in enumerate(path[1:], start=1):
        try:
            t.goto(x, y)
        except turtle.TurtleGraphicsError:
            continue

        if i % UPDATE_EVERY_POINTS == 0:
            screen.update()
            if delay > 0:
                time.sleep(delay)

    t.penup()
    screen.update()


def draw_all_paths(paths, color, width, delay, phase_name):
    print(f"Starting: {phase_name}")

    for index, path in enumerate(paths, start=1):
        draw_path(path, color, width, delay)

        if index % 50 == 0:
            print(f"{phase_name}: {index}/{len(paths)} paths done")

    print(f"Completed: {phase_name}")


def show_completed_message():
    msg = turtle.Turtle()
    msg.hideturtle()
    msg.penup()
    msg.color("white")
    msg.goto(0, 0)

    msg.write(
        "ॐ नमः शिवाय",
        align="center",
        font=("Arial", 30, "bold")
    )

    screen.update()


def save_screenshot():
    canvas = screen.getcanvas()
    canvas.postscript(file="mahadev_sketch.eps")
    print("Screenshot saved as mahadev_sketch.eps")


def main():
    try:
        paths = load_paths()
        print(f"Loaded {len(paths)} valid paths.")

        fit_screen_to_paths(paths)

        # Phase 1: Pencil sketch
        draw_all_paths(paths, PENCIL_DARK, 5, PENCIL_DELAY, "Dark Pencil")
        draw_all_paths(paths, PENCIL_WHITE, 1, PENCIL_DELAY, "White Pencil")

        time.sleep(0.5)

        # Phase 2: Neon sketch
        draw_all_paths(paths, BLUE_GLOW, 7, NEON_DELAY, "Blue Glow")
        draw_all_paths(paths, BLUE_MAIN, 3, NEON_DELAY, "Blue Main")
        draw_all_paths(paths, BLUE_BRIGHT, 1, NEON_DELAY, "Blue Bright")

        print("Sketch completed.")
        show_completed_message()
        save_screenshot()

    except Exception as e:
        print("Error:", e)

    turtle.done()


if __name__ == "__main__":
    main()