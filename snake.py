import turtle
import random
import time
import math

# --- Game Theme ---
CANVAS_BG = "#0D0D1A"
CYAN_BRIGHT = "#00F5FF"
TEAL_DARK = "#00ADB5"
CRIMSON_NEON = "#FF2E63"
BLUE_GLOW = "#4D4DFF"
OFF_WHITE = "#EEEEEE"

def setup_border():
    """Builds the glowing arena frame"""
    border_draw = turtle.Turtle()
    border_draw.speed(0)
    border_draw.hideturtle()
    border_draw.penup()
    
    # Outer blurred glow
    border_draw.color("#1A1A3D")
    border_draw.pensize(10)
    border_draw.goto(-315, 255)
    border_draw.pendown()
    for _ in range(2):
        border_draw.forward(630)
        border_draw.right(90)
        border_draw.forward(510)
        border_draw.right(90)
    
    # Main neon line
    border_draw.penup()
    border_draw.color(BLUE_GLOW)
    border_draw.pensize(3)
    border_draw.goto(-310, 250)
    border_draw.pendown()
    for _ in range(2):
        border_draw.forward(620)
        border_draw.right(90)
        border_draw.forward(500)
        border_draw.right(90)

def end_screen(final_pts):
    """Game over text overlay"""
    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("#FF0000")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, 0)
    pen.write("GAME OVER", align="center", font=("Verdana", 40, "bold"))
    pen.goto(0, -50)
    pen.color(OFF_WHITE)
    pen.write(f"Final Score: {final_pts}", align="center", font=("Verdana", 18, "normal"))

def start_game():
    # Window Config
    win = turtle.Screen()
    win.title("Neon Snake v1.0")
    win.bgcolor(CANVAS_BG)
    win.setup(width=700, height=700)
    win.tracer(0) 

    setup_border()

    # Vars
    score = 0
    move_speed = 0.1
    tail_segments = []
    tick = 0 

    # Snake Init
    player = turtle.Turtle("circle")
    player.speed(0)
    player.color(CYAN_BRIGHT)
    player.penup()
    player.goto(0, 0)
    player.direction = "stop"
    player.shapesize(1.1, 1.1)

    # Food Init
    orb = turtle.Turtle("circle")
    orb.speed(0)
    orb.color(CRIMSON_NEON)
    orb.penup()
    orb.goto(0, 100)

    # UI
    hud = turtle.Turtle()
    hud.speed(0)
    hud.color(CYAN_BRIGHT)
    hud.penup()
    hud.hideturtle()
    hud.goto(0, 260)
    hud.write("Score: 0", align="center", font=("Verdana", 20, "bold"))

    # Movement 
    def move_up():
        if player.direction != "down": player.direction = "up"
    def move_down():
        if player.direction != "up": player.direction = "down"
    def move_left():
        if player.direction != "right": player.direction = "left"
    def move_right():
        if player.direction != "left": player.direction = "right"

    win.listen()
    win.onkeypress(move_up, "Up")
    win.onkeypress(move_down, "Down")
    win.onkeypress(move_left, "Left")
    win.onkeypress(move_right, "Right")

    # Logic Loop
    while True:
        win.update()

        # Simple breathing effect for the food orb
        tick += 0.15
        orb_size = 0.8 + (math.sin(tick) * 0.2)
        orb.shapesize(orb_size, orb_size)

        # Wall hit detection
        if abs(player.xcor()) > 300 or player.ycor() > 240 or player.ycor() < -240:
            end_screen(score)
            win.update()
            time.sleep(1)
            win.clear()
            start_game()
            break

        # Check if we ate the orb
        if player.distance(orb) < 20:
            orb.goto(random.randint(-280, 280), random.randint(-230, 230))
            
            new_seg = turtle.Turtle("circle")
            new_seg.color(TEAL_DARK)
            new_seg.penup()
            tail_segments.append(new_seg)
            
            score += 10
            move_speed = max(0.04, move_speed - 0.002) 
            hud.clear()
            hud.write(f"Score: {score}", align="center", font=("Verdana", 20, "bold"))

        # Tail following logic
        for i in range(len(tail_segments)-1, 0, -1):
            tail_segments[i].goto(tail_segments[i-1].pos())

        if len(tail_segments) > 0:
            tail_segments[0].goto(player.pos())

        # Update snake position - using 'player' instead of 'head'
        if player.direction == "up":
            player.sety(player.ycor() + 20)
        elif player.direction == "down":
            player.sety(player.ycor() - 20)
        elif player.direction == "left":
            player.setx(player.xcor() - 20)
        elif player.direction == "right":
            player.setx(player.xcor() + 20)

        # Check self-collision
        for part in tail_segments:
            if part.distance(player) < 15:
                end_screen(score)
                win.update()
                time.sleep(1)
                win.clear()
                start_game()
                break

        time.sleep(move_speed)

if __name__ == "__main__":
    start_game()