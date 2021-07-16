import sys
import time
import math
from math import sin, cos, radians

import pygame
from pygame import Vector2

class Track():
    def __init__(self, screen, x, y, image):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = image
        
    def move(self, dx, dy):
        self.x = 550 + dx
        self.y = -1500 + dy
    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))


class Walls:
    def __init__(self, screen, x, y, width, height):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.startx = x
        self.starty = y
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, dx, dy):
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.x = self.startx + dx
        self.y = self.starty + dy

    def collide(self, rect):
        return self.hitbox.collidepoint(self.screen.get_width()/2 - 17.5, self.screen.get_height()/2 - 17.5)
    
class Car:
    def __init__(self, screen, x, y, image):

        self.screen = screen
        self.x = x
        self.y = y
        self.position = Vector2(x, y)
        self.speed = 0
        self.max_speed = 30
        self.image = pygame.image.load(image)
        self.angle = 270
        self.brakeforce = 5
        self.regspeed = 25
        self.hitboxplayer = 0
    def draw(self):
        rotated = pygame.transform.rotate(self.image, self.angle)
        self.rect = rotated.get_rect()
        self.screen.blit(rotated, self.position - (self.rect.width / 2, self.rect.height / 2))
        self.hitboxplayer = (self.x - 17.5, self.y - 17.5, 35, 35)

def main():

    pygame.init()
    pygame.display.set_caption("Py-Race")
    screen = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    hz = 60
    car = Car(screen, screen.get_width() / 2, screen.get_height() / 2, "917_10.png")
    speed = 0.0
    dx = 0
    dy = 0
    gas_pedal = False
    turn_angle = 0
    textColor = (255, 255, 255)
    trackimage = pygame.image.load("test_track1.png")
    track = Track(screen, -184, 2100, trackimage)
    o = 1
    p = 3
    laptime = "20"  # will later be the time between reaching the same location
    lap = o  # will later be the lap on / total laps to finish
    sector = [100.000, 100.000, 100.000]  # will later be the time to reach the sector locations
    font = pygame.font.Font(None, 56)
    s = 0
    right = 550
    up = 1500
    starttime = time.time()
    sectorlast = [100.000, 100.000, 100.000]
    backgroundmusic = pygame.mixer.Sound("Mario Kart 8 Music - Thwomp Fortress- My Rendition.ogg")
    backgroundmusic.play(-1)
    readyforlap = False
    walls = []
    Wall1 = Walls(screen, 760 + right, 760 - up, 80, 3280)
    walls.append(Wall1)
    Wall2 = Walls(screen, 760+ right, 3960- up, 3280, 80)
    walls.append(Wall2)
    Wall3 = Walls(screen, 1560+ right, 3160- up, 3280, 80)
    walls.append(Wall3)
    Wall4 = Walls(screen, 760+ right, 2360-up, 3280, 80)
    walls.append(Wall4)
    Wall5 = Walls(screen, 2360+ right, 760- up, 80, 1680)
    walls.append(Wall5)
    Wall6 = Walls(screen, 2360+ right, 760- up, 1680, 80)
    walls.append(Wall6)
    Wall7 = Walls(screen, 1560+ right, -40- up, 80, 1680)
    walls.append(Wall7)
    Wall8 = Walls(screen, 3160+ right, 1560- up, 1680, 80)
    walls.append(Wall8)
    Wall9 = Walls(screen, 0+ right, 0- up, 40, 4800)
    walls.append(Wall9)
    Wall10 = Walls(screen, 0+ right, 0- up, 4880, 40)
    walls.append(Wall10)
    Wall11 = Walls(screen, 4760+ right, 0- up, 40, 4800)
    walls.append(Wall11)
    Wall12 = Walls(screen, 0+ right, 4760- up, 4800, 40)
    walls.append(Wall12)


    while True:
        lap = f"{o}/{p}"
        laptime = round(time.time() - starttime, 3)
        for wall in walls:
            if wall.collide(car.hitboxplayer):
                if speed >= 0:
                    speed = 0
                    dx -= -50 * cos(radians(car.angle))
                    dy -= 50 * sin(radians(car.angle))
                if speed < 0:
                    speed = 0
                    dx -= 50 * cos(radians(car.angle))
                    dy -= 50 * sin(radians(car.angle))







        startarea = pygame.Rect(20 + track.x - screen.get_width()/2, 2400 + track.y - screen.get_height()/2, 900, 50)
        if startarea.collidepoint(0,0) and readyforlap:
            o += 1

            if o == 4:
                sector[s] = round(time.time() - starttime, 3)
                o = 1
            else:
                sector[s] = round(time.time() - starttime, 3)
                laptime = round(time.time()-starttime, 3)
            if sector[s] < sectorlast[0]:
                sectorlast[2] = sectorlast[1]
                sectorlast[1] = sectorlast[0]
                sectorlast[0] = sector[s]
            elif sector[s] < sectorlast[1]:
                sectorlast[2] = sectorlast[1]
                sectorlast[1] = sector[s]
            elif sector[s] < sectorlast[2]:
                sectorlast[2] = sector[s]
            if s == 2:
                s=0
            else:
                s += 1
            starttime=time.time()
            readyforlap = False
        if track.x >= -4400 and track.y <= -2400:
            readyforlap = True

        for event in pygame.event.get():
            pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if pressed[pygame.K_g]:
                    sys.exit()
        pressed = pygame.key.get_pressed()




        # Gas and brake
        if pressed[pygame.K_w]:
            gas_pedal = True
        else:
            gas_pedal = False

        # Speed - sensitive steering
        turn_angle = -0.025 * speed + 4

        # Steering
        if pressed[pygame.K_d] and abs(speed) > 0:
           car.angle -= turn_angle
        elif pressed[pygame.K_a] and abs(speed) > 0:
            car.angle += turn_angle

        # Speed limiter
        if speed > car.max_speed:
            speed = car.max_speed
        elif speed < (-car.max_speed + 10):
            speed = -car.max_speed + 10

        # Brake and gas
        if gas_pedal:
            speed += 0.125
        elif pressed[pygame.K_s]:
            speed -= 0.125
        else:
            if(speed > 1):
                speed -= 0.25
            elif(speed < -1):
                speed += 0.25
            else: speed = 0



        dx += -speed * cos(radians(car.angle))
        dy += speed * sin(radians(car.angle))
        screen.fill((67, 67, 67))
        track.move(dx, dy)
        track.draw()
        car.draw()
        clock.tick(hz)
        speedt = font.render("Speed: "+ str(speed * 7.5), True, textColor)
        screen.blit(speedt, (10, 25))
        lapp = font.render("Lap: "+ str(o), True, textColor)
        screen.blit(lapp, (10, 75))
        laptimee = font.render(f"Current: {laptime}", True, textColor)
        screen.blit(laptimee, (10, 125))
        sectorstart = font.render("Latest laps:", True, textColor)
        screen.blit(sectorstart, (10, 175))
        sector1 = font.render(f"Lap 1: {sector[0]}", True, textColor)
        screen.blit(sector1, (10, 225))
        sector2 = font.render(f"Lap 2: {sector[1]}", True, textColor)
        screen.blit(sector2, (10, 275))
        sector3 = font.render(f"Lap 3: {sector[2]}", True, textColor)
        screen.blit(sector3, (10, 325))
        sectorstartlast = font.render("Best Laps:", True, textColor)
        screen.blit(sectorstartlast, (10, 400))
        sector1last = font.render(f"1: {sectorlast[0]}", True, textColor)
        screen.blit(sector1last, (10, 450))
        sector2last = font.render(f"2: {sectorlast[1]}", True, textColor)
        screen.blit(sector2last, (10, 500))
        sector3last = font.render(f"3: {sectorlast[2]}", True, textColor)
        screen.blit(sector3last, (10, 550))
        for wall in walls:
            wall.move(dx, dy)

        pygame.display.update()



main()