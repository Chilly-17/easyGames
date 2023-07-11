import turtle


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


class PaddleMove:
    def __init__(self, paddle):
        self.paddle = paddle

    def up(self):
        paddle = self.paddle
        y = paddle.ycor()
        if y < 240:
            y += 20
            paddle.sety(y)

    def down(self):
        paddle = self.paddle
        y = paddle.ycor()
        if y > -240:
            y -= 20
            paddle.sety(y)
