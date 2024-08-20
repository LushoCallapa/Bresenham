import math
import arcade
import pymunk

class Box(arcade.Sprite):
    def __init__(self, x, y, space: pymunk.Space):
        super().__init__("9.pymunk/img/caja.png", 0.1)
        # body
        mass = 5
        moment = pymunk.moment_for_box(mass, (self.width, self.height))
        body = pymunk.Body(mass, moment)
        body.position = (x, y)
        # shape
        shape = pymunk.Poly.create_box(body, (self.width, self.height))
        shape.elasticity = 0.3
        shape.friction = 0.5

        space.add(body, shape)

        self.body = body
        self.shape = shape

    def update(self):
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.radians = self.shape.body.angle
