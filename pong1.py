import turtle

wn = turtle.Screen()

wn.title("Pong by Chilly_17")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)


# General paddle settings
def create_paddle(x_position):
    paddle = turtle.Turtle()
    paddle.speed(0)
    paddle.shape("square")
    paddle.color("white")
    paddle.shapesize(stretch_wid=5, stretch_len=1)
    paddle.penup()
    paddle.goto(x_position, 0)
    return paddle


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


class PaddleMove:
    def __init__(self, paddle):
        self.paddle = paddle

    def up(self):
        paddle = self.paddle
        y = paddle.ycor()
        y += 20
        paddle.sety(y)

    def down(self):
        paddle = self.paddle
        y = paddle.ycor()
        y -= 20
        paddle.sety(y)


paddle_a_func = PaddleMove(paddle_a)
paddle_b_func = PaddleMove(paddle_b)


# Keyboard binding
wn.listen()
wn.onkeypress(paddle_a_func.up, "w")
wn.onkeypress(paddle_a_func.down, "s")
wn.onkeypress(paddle_b_func.up, "up")
wn.onkeypress(paddle_b_func.down, "down")


# Main loop
while True:
    wn.update()
