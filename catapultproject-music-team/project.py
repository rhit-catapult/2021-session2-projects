import pygame
import sys
import random
import time
rando = 0
pos = []



class Scoreboard:
    def __init__(self, screen, x, y):
        self.x = x
        self.y = y
        self.screen = screen
        self.score = 0
    def draw(self):
        self.font = pygame.font.SysFont("Impact", 20)
        caption1 = self.font.render(f"Score: {self.score} ", True, (255, 255, 255))

        self.screen.blit(caption1, (5, 5))
    # def music(self):

class Blocks:
    def __init__(self, screen, object_speed):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.boost_image = pygame.image.load("boost square.png")
        self.boost_image.set_colorkey((255, 255, 255))
        self.hitbox = pygame.Rect(self.x, self.y, self.boost_image.get_width(), self.boost_image.get_height())
        self.speed = object_speed
    def move(self):
        self.y += self.speed

    def draw(self, position):
        if position == 0:
            self.x = 8
            self.screen.blit(self.boost_image, (self.x, self.y))
            self.hitbox = pygame.Rect(self.x, self.y, self.boost_image.get_width(), self.boost_image.get_height())
        if position == 1:
            self.x = 135
            self.screen.blit(self.boost_image, (self.x, self.y))
            self.hitbox = pygame.Rect(self.x, self.y, self.boost_image.get_width(), self.boost_image.get_height())
        if position == 2:
            self.x = 262
            self.screen.blit(self.boost_image, (self.x, self.y))
            self.hitbox = pygame.Rect(self.x, self.y, self.boost_image.get_width(), self.boost_image.get_height())
        if position == 3:
            self.x = 389
            self.screen.blit(self.boost_image, (self.x, self.y))
            self.hitbox = pygame.Rect(self.x, self.y, self.boost_image.get_width(), self.boost_image.get_height())

    def off_screen(self):
        if self.y > self.screen.get_height():
            return True

    def changeSpeed(self, speed):
        self.speed = speed


class RoadLine:
    def __init__(self, screen, x, y, object_speed):
        self.screen = screen
        self.x = x
        self.y = y
        self.speed = object_speed

    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.line(self.screen, (255, 255, 255), (self.x, self.y), (self.x, self.y - 100), 400)

    def off_screen(self):
        if self.y > self.screen.get_height():
            return True
        else:
            return False

    def changeSpeed(self, speed):
        self.speed = speed

class Lanes:
    def __init__(self, screen, x):
        self.screen = screen
        self.x = x
        self.road_image = pygame.image.load("road.jpg")

    def draw(self):
        self.screen.blit(self.road_image, (self.x, 0))


class Car:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.car_image = pygame.image.load("pixel_car-removebg-preview.png")
        self.hitbox = pygame.Rect(self.x, self.y, self.car_image.get_width(), self.car_image.get_height())


    def draw(self):
        self.screen.blit(self.car_image, (self.x, self.y))

    def hit_by_rubble(self, rubble):
        car_hit_box = pygame.Rect(self.x, self.y, self.car_image.get_width(), self.car_image.get_height())
        return car_hit_box.colliderect(rubble.hitbox)

    def hit_by_boost(self, boost1):
        car_hit_box = pygame.Rect(self.x, self.y, self.car_image.get_width(), self.car_image.get_height())
        return car_hit_box.colliderect(boost1.hitbox)

    def move(self, counter):
        if counter == 0:
            self.screen.blit(self.car_image, (8, 502))
            self.x = 8
            self.y = 502
        if counter == 1:
            self.screen.blit(self.car_image, (135, 502))
            self.x = 135
            self.y = 502
        if counter == 2:
            self.screen.blit(self.car_image, (262, 502))
            self.x = 262
            self.y = 502
        if counter == 3:
            self.screen.blit(self.car_image, (389, 502))
            self.x = 389
            self.y = 502




class Obstacle:
    def __init__(self, screen, object_speed):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.rubble_image = pygame.image.load("rubble.png")
        self.hitbox = pygame.Rect(self.x, self.y, self.rubble_image.get_width(), self.rubble_image.get_height())
        self.speed = object_speed

    def draw(self, position):
        if position == 0:
            self.x = 8
            self.screen.blit(self.rubble_image, (8, self.y))
            self.hitbox = pygame.Rect(self.x, self.y, self.rubble_image.get_width(), self.rubble_image.get_height())
        if position == 1:
            self.x = 127
            self.screen.blit(self.rubble_image, (127, self.y))
            self.hitbox = pygame.Rect(self.x, self.y, self.rubble_image.get_width(), self.rubble_image.get_height())
        if position == 2:
            self.x = 254
            self.screen.blit(self.rubble_image, (254, self.y))
            self.hitbox = pygame.Rect(self.x, self.y, self.rubble_image.get_width(), self.rubble_image.get_height())
        if position == 3:
            self.x = 381
            self.screen.blit(self.rubble_image, (381, self.y))
            self.hitbox = pygame.Rect(self.x, self.y, self.rubble_image.get_width(), self.rubble_image.get_height())

    def move(self):
        self.y += self.speed

    def off_screen(self):
        if self.y > self.screen.get_height():
            return True

    def changeSpeed(self, speed):
        self.speed = speed



def main():
    pygame.init()
    pygame.mixer.music.load("Sonic Forces Boost Sound Effect.mp3")
    boost_sounds = pygame.mixer.Sound("Sonic Forces Boost Sound Effect.mp3")
    pygame.mixer.music.load("8- bit explosion sound effect [SFX].mp3")
    explosion_music = pygame.mixer.Sound("8- bit explosion sound effect [SFX].mp3")
    main_music = pygame.mixer.Sound("Dj Nate - Club Step.mp3")
    pygame.mixer.music.load("Dj Nate - Club Step.mp3")
    main_music.play()
    rando = random.randrange(0, 4)
    pos = [1, 1, 1, 1]
    pos[rando] = 0
    for x in range(len(pos)):
        if pos[x] != 0:
            pos[x] = 2
    print(pos)
    counter = 0
    speed = 1
    game_over = False
    pygame.display.set_caption("Rubble Road")
    screen = pygame.display.set_mode((495, 700))
    clock = pygame.time.Clock()
    clock.tick(60)
    rubble = Obstacle(screen, speed)
    rubble2 = Obstacle(screen, speed)
    rubble3 = Obstacle(screen, speed)
    car = Car(screen, 4, 502)
    line1 = RoadLine(screen, 254, 0, speed + 2)
    boost1 = Blocks(screen, speed)
    road1 = Lanes(screen, 0)
    road2 = Lanes(screen, 127)
    road3 = Lanes(screen, 254)
    road4 = Lanes(screen, 381)
    scoreboard = Scoreboard(screen, 5, 5)
    font1 = pygame.font.SysFont(None, 50)
    caption1 = font1.render(f"GAME OVER", True, (255, 255, 255))
    font2 = pygame.font.SysFont(None, 30)
    caption2 = font2.render(f"Press SPACE to Restart!", True, (255, 255, 255))

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[pygame.K_SPACE]:
                    rubble.y = 0 - rubble.rubble_image.get_height()
                    rubble2.y = 0 - rubble.rubble_image.get_height()
                    rubble3.y = 0 - rubble.rubble_image.get_height()
                    boost1.y = 0 - rubble.rubble_image.get_height()
                    scoreboard.score = 0
                    speed = 1
                    rubble3.changeSpeed(speed)
                    rubble2.changeSpeed(speed)
                    rubble.changeSpeed(speed)
                    boost1.changeSpeed(speed)
                    line1.changeSpeed(speed + 2)
                    game_over = False
            if game_over == False:
                if event.type == pygame.KEYDOWN:
                    pressed_keys = pygame.key.get_pressed()
                    if pressed_keys[pygame.K_LEFT]:
                        counter -= 1
                        if counter < 0:
                            counter = 0
                        car.move(counter)

                    if pressed_keys[pygame.K_RIGHT]:
                        counter += 1
                        if counter > 3:
                            counter = 3
                        car.move(counter)

        if game_over == True:
            explosion_image = pygame.image.load("explosionn.png")
            screen.blit(explosion_image, (car.x - 50, car.y - 63))
            screen.blit(caption1, (141, screen.get_width() / 2))
            screen.blit(caption2, (141, screen.get_height() / 2))

            pygame.display.update()

            continue

        if line1.off_screen():
            line1.y = 0


        screen.fill((156, 155, 151))
        line1.move()
        line1.draw()
        road1.draw()
        road2.draw()
        road3.draw()
        road4.draw()
        boost1.move()
        rubble.move()
        rubble3.move()
        rubble2.move()
        scoreboard.draw()
        j = 0
        for k in range(len(pos)):
            if pos[k] == 0:
                boost1.draw(k)
            if pos[k] == 2:
                if j == 0:
                    rubble.draw(k)
                    j += 1
                    continue
                if j == 1:
                    rubble2.draw(k)
                    j += 1
                    continue
                if j == 2:
                    rubble3.draw(k)
                    j += 1
                    continue

        car.draw()
        if car.hit_by_rubble(rubble) or car.hit_by_rubble(rubble2) or car.hit_by_rubble(rubble3):
            explosion_music.play()
            game_over = True
        if boost1.off_screen():
            boost_sounds.play()
            boost1.y = 0 - rubble.rubble_image.get_height()
        if rubble.off_screen():
            rubble.y = 0 - rubble.rubble_image.get_height()
            random.shuffle(pos)
        if rubble2.off_screen():
            rubble2.y = 0 - rubble.rubble_image.get_height()
        if rubble3.off_screen():
            speed += .15
            rubble3.changeSpeed(speed)
            rubble2.changeSpeed(speed)
            rubble.changeSpeed(speed)
            boost1.changeSpeed(speed)
            line1.changeSpeed(speed + 2)
            rubble3.y = 0 - rubble.rubble_image.get_height()
            scoreboard.score += 10

        pygame.display.update()


main()
