#!/usr/bin/env python3

import turtle

counter = 0

while counter < 36:
    for i in range(4):

        turtle.forward(50)
        turtle.right(90)

    counter += 1
    turtle.right(10)

turtle.done()