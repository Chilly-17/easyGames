import turtle
import time
from paddle import create_paddle, PaddleMove

wn = turtle.Screen()

wn.title("Pong by Chilly_17")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)


# Paddle A
paddle_a = create_paddle(-350)

# Paddle B
paddle_b = create_paddle(350)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 1
ball.dy = 1

paddle_a_func = PaddleMove(paddle_a)
paddle_b_func = PaddleMove(paddle_b)


# Keyboard binding
wn.listen()
wn.onkeypress(paddle_a_func.up, "w")
wn.onkeypress(paddle_a_func.down, "s")
wn.onkeypress(paddle_b_func.up, "Up")
wn.onkeypress(paddle_b_func.down, "Down")


while True:
    time.sleep(1 / 60)
    wn.update()

    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border checking
    if ball.ycor() >= 290:
        ball.dy *= -1

    if ball.ycor() <= -290:
        ball.dy *= -1

    if ball.xcor() >= 400:
        ball.goto(0, 0)
        ball.dx *= -1
        ball.dy *= -1

    if ball.xcor() <= -400:
        ball.goto(0, 0)
        ball.dx *= -1
        ball.dy *= -1

    # Paddle and ball collisions
    if (
        (ball.xcor() > 340 and ball.xcor() < 350)
        and (
            ball.ycor() < paddle_b.ycor() + 60
            and ball.ycor() > paddle_b.ycor() - 60
        )
    ):
        ball.setx(340)
        ball.dx *= -1

    if (
        (ball.xcor() < -340 and ball.xcor() > -350)
        and (
            ball.ycor() < paddle_a.ycor() + 60
            and ball.ycor() > paddle_a.ycor() - 60
        )
    ):
        ball.setx(-340)
        ball.dx *= -1
