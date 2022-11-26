import pygame, sys, numpy, random
import number
from keyboard import keyboard

setting = {c.split("=")[0].replace(" ", ""):eval(c.split("=")[1]) for c in open(".\\data\\setting.txt", 'r', encoding='utf-8').read().splitlines()}
print(setting)

window = pygame.display.set_mode((240, 432))
pygame.display.set_icon(pygame.image.load(".\\data\\icon.png"))
pygame.display.set_caption("BREAKOUT")
clock = pygame.time.Clock()

bricks = numpy.ones((6,15))
colors = [(255, 102, 99), (254, 177, 68), (253, 253, 151), (158, 224, 158), (158, 193, 207), (204, 153, 201)]
score = 0
reward = 0

class Plate:
    def __init__(self):
        self.x = 120
        self.size = setting["plate_size"]
        self.speed = setting["plate_speed"]

    def draw(self, keystate):
        if ("left_arrow" in keystate): self.x -= self.speed
        if ("right_arrow" in keystate): self.x += self.speed

        if (self.x-self.size < 0): self.x = self.size
        elif (self.x + self.size > 240): self.x = 240 - self.size

        pygame.draw.rect(window, (255, 255, 255), [self.x-self.size, 416, self.size*2, 8])

class Ball:
    def __init__(self):
        self.xspeed = 2 if random.random() > 0.5 else -2
        self.yspeed = 2
        self.x = random.randint(10, 230)
        self.y = 240
        self.size = 2

    def draw(self):
        global score, reward
        self.x += self.xspeed
        self.y += self.yspeed

        # wall collide
        if (self.x - self.size < 0):
            self.xspeed *= -1
            self.x = self.size
        elif (self.x + self.size > 240):
            self.xspeed *= -1
            self.x = 240 - self.size
        if (self.y - self.size < 48):
            self.yspeed *= -1
            self.y = self.size + 48

        # plate collide
        if ((self.y + self.size >=  416 and self.y + self.size <= 424) and (self.x + self.size > plate.x-plate.size and self.x - self.size < plate.x + plate.size)):
            self.yspeed *= -1
            self.y = 416 - self.size

            distance = self.x - plate.x
            if (distance < 0): distance -= 10
            else: distance += 10
            self.xspeed = distance//10
            if (abs(self.xspeed) > 3): self.xspeed = 3 if self.xspeed > 0 else -3
            reward -= 1

            # print(f"{reward=}")

        # brick collide
        collide = False
        for y, axis_x in enumerate(bricks):
            for x, brick in enumerate(axis_x):
                if (brick):
                    pygame.draw.rect(window, colors[y], [x*16, y*16+112, 16, 16])
                    # pygame.draw.rect(window, colors[y], [x*16+1, y*16+112+1, 16-2, 16-2])
                    if ((self.x - self.size < (x + 1) * 16 ) and 
                            (self.x + self.size > x*16 ) and
                            (self.y - self.size < (y+1)*16 +112) and
                            (self.y + self.size > y*16 +112) and not collide):
                        score += 1
                        reward += 1
                        bricks[y][x] = 0
                        collide = True

                        if (self.x <= x*16 or self.x >= (x+1)*16):
                            self.xspeed *= -1
                        elif (self.y <= y*16 or self.y >= (y+1)*16):
                            self.yspeed *= -1
                        # print(f"{reward=}")

        pygame.draw.rect(window, (255,0,0), (self.x-self.size, self.y-self.size, self.size*2, self.size*2))

    


class system:
    def score():
        s = f"{str(score):0>13}"
        for i, c in enumerate(s):
            number.render(window, c, (i+1)*16, 16)
    
    def display():
        window.fill((0,0,0))
        pygame.draw.rect(window, (255,255,255), [0, 0, 240, 48], 8)
        system.score()

    def event(keystate):
        global score, plate, ball, bricks, reward
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()

        if ('r' in keystate[2]):
            ball = Ball()
            plate = Plate()
            score = 0
            reward = 0
            bricks = numpy.ones((6,15))

plate = Plate()
ball = Ball()

while __name__ == "__main__":
    keystate = keyboard.get_input()

    system.display()
    system.event(keystate)
    plate.draw(keystate[0])
    ball.draw()

    clock.tick(90)
    pygame.display.update()