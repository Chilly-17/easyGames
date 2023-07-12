import turtle
import time
import random
from paddle import Paddle
from pen import Pen
import winsound

wn = turtle.Screen()

wn.title("Pong by Chilly_17")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)


def update():
    wn.update()


# Paddle A
paddle_a = Paddle(x_position=-350)

# Paddle B
paddle_b = Paddle(x_position=350)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 2
ball.dy = 2

y_range = [i * 10 for i in range(1, 21)] + [-i * 10 for i in range(1, 21)]

# Pen
score_a, score_b = 0, 0
pen = Pen()
pen.write(score_a, score_b)

# Keyboard binding
wn.listen()
wn.onkeypress(paddle_a.up, "w")
wn.onkeypress(paddle_a.down, "s")
wn.onkeypress(paddle_b.up, "Up")
wn.onkeypress(paddle_b.down, "Down")

while True:
    time.sleep(1 / 60)
    wn.update()

    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border checking

    if ball.ycor() >= 290:
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
        ball.dy *= -1

    if ball.ycor() <= -290:
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
        ball.dy *= -1

    if ball.xcor() >= 400:
        ball.goto(0, random.choice(y_range))
        ball.dx = -2
        ball.dy = 2
        score_a += 1
        pen.write(score_a, score_b)

    if ball.xcor() <= -400:
        ball.goto(0, random.choice(y_range))
        ball.dx = 2
        ball.dy = 2
        score_b += 1
        pen.write(score_a, score_b)

    # Paddle and ball collisions

    if (
        (ball.xcor() > 340 and ball.xcor() < 350)
        and (
            ball.ycor() < paddle_b.ycor() + 60
            and ball.ycor() > paddle_b.ycor() - 60
        )
    ):
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
        ball.setx(340)
        ball.dx *= -1.1

    if (
        (ball.xcor() < -340 and ball.xcor() > -350)
        and (
            ball.ycor() < paddle_a.ycor() + 60
            and ball.ycor() > paddle_a.ycor() - 60
        )
    ):
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)
        ball.setx(-340)
        ball.dx *= -1.1
