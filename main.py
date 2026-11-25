import turtle
import random
import time

# Screen setup
screen = turtle.Screen()
screen.title("Space Asteroid Dodger")
screen.bgcolor("#0b0f19")
screen.setup(width=600, height=700)
screen.tracer(0)

# Background stars for depth
stars = []
for _ in range(25):
    star = turtle.Turtle()
    star.shape("circle")
    star.color("#475569")
    star.shapesize(stretch_wid=0.15, stretch_len=0.15)
    star.penup()
    star.goto(random.randint(-280, 280), random.randint(-330, 330))
    star.speed_y = random.uniform(1.0, 2.5)
    stars.append(star)

# Player ship
player = turtle.Turtle()
player.shape("triangle")
player.color("#38bdf8")
player.shapesize(stretch_wid=1.5, stretch_len=1.5)
player.penup()
player.setheading(90)
player.goto(0, -260)

# Scoreboard pen
score = 0
high_score = 0
score_pen = turtle.Turtle()
score_pen.hideturtle()
score_pen.color("white")
score_pen.penup()
score_pen.goto(0, 305)

# Instruction & Game Over overlay pen
ui_pen = turtle.Turtle()
ui_pen.hideturtle()
ui_pen.penup()

# Game state: "START", "PLAYING", or "GAME_OVER"
game_state = "START"
lasers = []
last_shot_time = 0
SHOT_COOLDOWN = 0.25

def update_score():
    score_pen.clear()
    score_pen.write(
        f"Score: {score}   |   High Score: {high_score}",
        align="center",
        font=("Courier", 15, "bold"),
    )

def draw_popup_box(width, height):
    ui_pen.clear()
    ui_pen.goto(-width / 2, height / 2)
    ui_pen.color("#38bdf8", "#111827")
    ui_pen.pensize(3)
    ui_pen.pendown()
    ui_pen.begin_fill()
    for _ in range(2):
        ui_pen.forward(width)
        ui_pen.right(90)
        ui_pen.forward(height)
        ui_pen.right(90)
    ui_pen.end_fill()
    ui_pen.penup()

def show_instructions():
    draw_popup_box(460, 300)
    ui_pen.goto(0, 95)
    ui_pen.color("#38bdf8")
    ui_pen.write("SPACE ASTEROID DODGER", align="center", font=("Courier", 20, "bold"))

    instructions = [
        ("CONTROLS", "#facc15", 45),
        ("Arrow Keys / WASD : Move Up, Down, Left, Right", "white", 15),
        ("SPACEBAR : Fire Laser", "white", -12),
        ("RULES", "#facc15", -50),
        ("Dodge asteroids (+10) or blast them (+20)", "white", -78),
        ("Press ENTER to Start", "#4ade80", -122),
    ]
    for text, color, y_pos in instructions:
        ui_pen.goto(0, y_pos)
        ui_pen.color(color)
        font_style = "bold" if color in ("#facc15", "#4ade80") else "normal"
        ui_pen.write(text, align="center", font=("Courier", 12, font_style))

def show_game_over():
    draw_popup_box(400, 170)
    ui_pen.goto(0, 25)
    ui_pen.color("#f87171")
    ui_pen.write("GAME OVER", align="center", font=("Courier", 28, "bold"))
    ui_pen.goto(0, -15)
    ui_pen.color("white")
    ui_pen.write(f"Final Score: {score}", align="center", font=("Courier", 15, "normal"))
    ui_pen.goto(0, -52)
    ui_pen.color("#4ade80")
    ui_pen.write("Press 'R' to Play Again", align="center", font=("Courier", 14, "bold"))

# Player movement (4 directions)
def move_left():
    if game_state == "PLAYING":
        x = player.xcor() - 32
        if x > -270:
            player.setx(x)

def move_right():
    if game_state == "PLAYING":
        x = player.xcor() + 32
        if x < 270:
            player.setx(x)

def move_up():
    if game_state == "PLAYING":
        y = player.ycor() + 32
        if y < 250:
            player.sety(y)

def move_down():
    if game_state == "PLAYING":
        y = player.ycor() - 32
        if y > -295:
            player.sety(y)

# Shoot laser
def fire_laser():
    global last_shot_time
    if game_state != "PLAYING":
        return
    current_time = time.time()
    if current_time - last_shot_time >= SHOT_COOLDOWN:
        last_shot_time = current_time
        bolt = turtle.Turtle()
        bolt.shape("square")
        bolt.color("#facc15")
        bolt.shapesize(stretch_wid=0.8, stretch_len=0.2)
        bolt.penup()
        bolt.goto(player.xcor(), player.ycor() + 20)
        lasers.append(bolt)

# Create asteroids
asteroids = []
for _ in range(7):
    rock = turtle.Turtle()
    rock.shape("circle")
    rock.color("#f97316")
    rock.shapesize(stretch_wid=1.3, stretch_len=1.3)
    rock.penup()
    rock.goto(random.randint(-260, 260), random.randint(150, 650))
    rock.speed_y = random.uniform(4.0, 7.5)
    asteroids.append(rock)

def reset_asteroid(rock, speed_boost=0.0):
    rock.goto(random.randint(-260, 260), random.randint(360, 580))
    rock.speed_y += speed_boost

# Start or Restart game
def start_game():
    global game_state
    if game_state == "START":
        ui_pen.clear()
        game_state = "PLAYING"

def restart_game():
    global score, game_state
    if game_state != "GAME_OVER":
        return
    score = 0
    game_state = "PLAYING"
    ui_pen.clear()
    player.goto(0, -260)

    for bolt in lasers:
        bolt.hideturtle()
    lasers.clear()

    for rock in asteroids:
        rock.goto(random.randint(-260, 260), random.randint(150, 650))
        rock.speed_y = random.uniform(4.0, 7.5)

    update_score()

# Keyboard bindings
screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(move_up, "Up")
screen.onkeypress(move_down, "Down")
screen.onkeypress(move_left, "a")
screen.onkeypress(move_right, "d")
screen.onkeypress(move_up, "w")
screen.onkeypress(move_down, "s")
screen.onkeypress(fire_laser, "space")
screen.onkeypress(start_game, "Return")
screen.onkeypress(restart_game, "r")
screen.onkeypress(restart_game, "R")

update_score()
show_instructions()

# Main game loop
try:
    while True:
        screen.update()
        time.sleep(0.02)

        # Animate background stars even on start screen
        for star in stars:
            star.sety(star.ycor() - star.speed_y)
            if star.ycor() < -340:
                star.goto(random.randint(-280, 280), 340)

        if game_state != "PLAYING":
            continue

        # Move lasers upward
        for bolt in lasers[:]:
            bolt.sety(bolt.ycor() + 18)
            if bolt.ycor() > 350:
                bolt.hideturtle()
                lasers.remove(bolt)

        # Move asteroids downward and check collisions
        for rock in asteroids:
            rock.sety(rock.ycor() - rock.speed_y)

            # Check laser hit
            hit_by_laser = False
            for bolt in lasers[:]:
                if bolt.distance(rock) < 25:
                    bolt.hideturtle()
                    lasers.remove(bolt)
                    reset_asteroid(rock, speed_boost=0.1)
                    score += 20
                    if score > high_score:
                        high_score = score
                    update_score()
                    hit_by_laser = True
                    break

            if hit_by_laser:
                continue

            # Asteroid dodged (passed bottom)
            if rock.ycor() < -340:
                reset_asteroid(rock, speed_boost=0.12)
                score += 10
                if score > high_score:
                    high_score = score
                update_score()

            # Check player collision
            if player.distance(rock) < 28:
                game_state = "GAME_OVER"
                show_game_over()
                break

except turtle.Terminator:
    pass
    
