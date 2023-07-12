import turtle


# General paddle settings

class Paddle:
    def __init__(self, x_position):
        paddle = turtle.Turtle()
        paddle.speed(0)
        paddle.shape("square")
        paddle.color("white")
        paddle.shapesize(stretch_wid=5, stretch_len=1)
        paddle.penup()
        paddle.goto(x_position, 0)
        paddle.ycor()
        self.paddle = paddle

    def up(self):
        y = self.paddle.ycor()
        if y < 240:
            y += 20
            self.paddle.sety(y)
            return self.paddle.ycor()

    def down(self):
        y = self.paddle.ycor()
        if y > -240:
            y -= 20
            self.paddle.sety(y)
            return self.paddle.ycor()

    def ycor(self):
        return self.paddle.ycor()
