import turtle
import random
import time

# Screen setup
screen = turtle.Screen()
screen.title("Space Asteroid Dodger")
screen.bgcolor("#0b0f19")
screen.setup(width=600, height=700)
screen.tracer(0)

# Player ship
player = turtle.Turtle()
player.shape("triangle")
player.color("#38bdf8")
player.shapesize(stretch_wid=1.5, stretch_len=1.5)
player.penup()
player.setheading(90)
player.goto(0, -280)

# Scoreboard pen
score = 0
high_score = 0
score_pen = turtle.Turtle()
score_pen.hideturtle()
score_pen.color("white")
score_pen.penup()
score_pen.goto(0, 305)

# Game Over message pen
msg_pen = turtle.Turtle()
msg_pen.hideturtle()
msg_pen.color("#f87171")
msg_pen.penup()

# Game state
game_over = False
lasers = []
last_shot_time = 0
SHOT_COOLDOWN = 0.25  # Seconds between shots

def update_score():
    score_pen.clear()
    score_pen.write(
        f"Score: {score}   |   High Score: {high_score}",
        align="center",
        font=("Courier", 15, "bold"),
    )

def show_game_over():
    msg_pen.clear()
    msg_pen.goto(0, 20)
    msg_pen.color("#f87171")
    msg_pen.write("GAME OVER", align="center", font=("Courier", 32, "bold"))
    msg_pen.goto(0, -25)
    msg_pen.color("white")
    msg_pen.write("Press 'R' to Play Again", align="center", font=("Courier", 16, "normal"))

# Player movement
def move_left():
    if not game_over:
        x = player.xcor() - 35
        if x > -270:
            player.setx(x)

def move_right():
    if not game_over:
        x = player.xcor() + 35
        if x < 270:
            player.setx(x)

# Shoot laser
def fire_laser():
    global last_shot_time
    if game_over:
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

# Restart game
def restart_game():
    global score, game_over
    if not game_over:
        return
    score = 0
    game_over = False
    msg_pen.clear()
    player.goto(0, -280)

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
screen.onkeypress(move_left, "a")
screen.onkeypress(move_right, "d")
screen.onkeypress(fire_laser, "space")
screen.onkeypress(restart_game, "r")
screen.onkeypress(restart_game, "R")

update_score()

# Main game loop
try:
    while True:
        screen.update()
        time.sleep(0.02)

        if game_over:
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
                game_over = True
                show_game_over()
                break

except turtle.Terminator:
    pass
