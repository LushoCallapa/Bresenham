import arcade
import pymunk
from game_object import Box

WIDTH = 800
HEIGHT = 800
TITLE = "boxes"

class Car:
    def __init__(self, x, y, space):
        mass = 5
        moment = pymunk.moment_for_box(mass, (100, 70))
        chassis_body = pymunk.Body(mass, moment)
        chassis_body.position = (x, y)
        # shape
        chassis_shape = pymunk.Poly.create_box(chassis_body, (100, 70))
        chassis_shape.elasticity = 0.3
        chassis_shape.friction = 0.5

        # wheels
        wheel_radius = 20
        wheel_offset_x = 40
        wheel_offset_y = 35

        f_wheel_body = pymunk.Body()
        f_wheel_body.position = (x + wheel_offset_x, y - wheel_offset_y)
        f_wheel_shape = pymunk.Circle(f_wheel_body, wheel_radius)
        f_wheel_shape.density = 0.01
        f_wheel_shape.friction = 0.5
        f_wheel_shape.elasticity = 1
        self.f_wheel_sprite = arcade.SpriteCircle(wheel_radius, arcade.color.GREEN)
        
        r_wheel_body = pymunk.Body()
        r_wheel_body.position = (x - wheel_offset_x, y - wheel_offset_y)
        r_wheel_shape = pymunk.Circle(r_wheel_body, wheel_radius)
        r_wheel_shape.density = 0.01
        r_wheel_shape.friction = 0.5
        r_wheel_shape.elasticity = 1
        self.r_wheel_sprite = arcade.SpriteCircle(wheel_radius, arcade.color.GREEN)

        # Joints: usando DampedSpring en lugar de PinJoint
        f_spring = pymunk.DampedSpring(chassis_body, f_wheel_body, (wheel_offset_x, -wheel_offset_y), (0, 0), rest_length=0.01, stiffness=2000, damping=10)
        r_spring = pymunk.DampedSpring(chassis_body, r_wheel_body, (-wheel_offset_x, -wheel_offset_y), (0, 0), rest_length=0.01, stiffness=2000, damping=10)

        # Motors para agregar fuerza rotacional
        f_motor = pymunk.SimpleMotor(chassis_body, f_wheel_body, 10)
        r_motor = pymunk.SimpleMotor(chassis_body, r_wheel_body, 10)

        space.add(chassis_body, chassis_shape)
        space.add(f_wheel_body, f_wheel_shape)
        space.add(r_wheel_body, r_wheel_shape)
        space.add(f_spring)
        space.add(f_motor)
        space.add(r_spring)
        space.add(r_motor)

        self.chassis_sprite = arcade.SpriteSolidColor(100, 70, arcade.color.RED)

        self.sprites = arcade.SpriteList()
        self.sprites.append(self.chassis_sprite)
        self.sprites.append(self.f_wheel_sprite)
        self.sprites.append(self.r_wheel_sprite)
        self.chassis_body = chassis_body
        self.chassis_shape = chassis_shape
        self.f_wheel = f_wheel_shape
        self.r_wheel = r_wheel_shape
        
    
    def update(self):
        self.chassis_sprite.center_x = self.chassis_shape.body.position.x
        self.chassis_sprite.center_y = self.chassis_shape.body.position.y
        self.chassis_sprite.radians = self.chassis_shape.body.angle

        self.f_wheel_sprite.center_x = self.f_wheel.body.position.x
        self.f_wheel_sprite.center_y = self.f_wheel.body.position.y
        self.f_wheel_sprite.radians = self.f_wheel.body.angle

        self.r_wheel_sprite.center_x = self.r_wheel.body.position.x
        self.r_wheel_sprite.center_y = self.r_wheel.body.position.y
        self.r_wheel_sprite.radians = self.r_wheel.body.angle



class App(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        # crear espacio
        self.space = pymunk.Space()
        self.space.gravity = (0, -900)

        self.car = Car(200, 50, self.space)
        self.lines = []
        self.add_static()
        # sprites
        self.sprites = arcade.SpriteList() 
        self.sprites.extend(self.car.sprites)

        # Agregar obstáculo diagonal
        self.add_obstacle()

    def on_update(self, delta_time: float):
        self.space.step(1 / 60) # OJO
        self.car.update()
        self.sprites.update()

    def on_draw(self):
        arcade.start_render()
        self.sprites.draw()

    def add_static_segment(self, x0, y0, x1, y1):
        segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        segment_shape = pymunk.Segment(segment_body, [x0, y0], [x1, y1], 0)
        segment_shape.friction = 0.1
        self.space.add(segment_body, segment_shape)
        self.lines.append((x0, y0, x1, y1))

    def add_static(self):
        # agregar piso
        self.add_static_segment(0, 0, WIDTH, 0)
        self.add_static_segment(WIDTH, 0, WIDTH, HEIGHT)
    
    def add_obstacle(self):
        # Agregar una línea diagonal como obstáculo
        x0, y0 = 500, 0
        x1, y1 = 510, 5

        # Línea en pymunk
        segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        segment_shape = pymunk.Segment(segment_body, [x0, y0], [x1, y1], 10)
        segment_shape.friction = 0.5
        segment_shape.color = arcade.color.RED
        self.space.add(segment_body, segment_shape)

        # Línea en arcade para dibujo
        self.lines.append((x0, y0, x1, y1))

    def draw_obstacles(self):
        for x0, y0, x1, y1 in self.lines:
            arcade.draw_line(x0, y0, x1, y1, arcade.color.RED, 10)

    def on_draw(self):
        arcade.start_render()
        self.sprites.draw()
        self.draw_obstacles()  # Asegúrate de dibujar los obstáculos en cada frame


if __name__ == "__main__":
    app = App()
    arcade.run()
