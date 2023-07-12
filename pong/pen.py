import turtle


# Pen
class Pen:
    def __init__(self):
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0, 260)

    def write(self, a_score, b_score):
        self.pen.clear()
        self.pen.write(
            f"PlayerA: {a_score} PlayerB: {b_score}",
            align="center",
            font=("Courier", 24, "normal")
        )
