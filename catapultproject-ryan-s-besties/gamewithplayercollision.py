import pygame, sys, math, random, time


class Player:
    def __init__(self, screen, color, x, y, radius, player_number):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.weapon_offset_x = radius
        self.weapon_offset_y = -25
        self.hammer = pygame.image.load("hammer.png")
        self.player_number = player_number
        # self.angle = 360

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

        self.draw_weapon()
        self.health_bar()

    def draw_weapon(self):
        self.hammer = pygame.transform.scale(self.hammer, (30, 30))

        self.screen.blit(self.hammer, (self.x - self.hammer.get_width()/2 +
                                       self.weapon_offset_x, self.y + self.weapon_offset_y))

    def move(self, pressed_keys, other_player):
        if self.player_number == 1:
            if pressed_keys[pygame.K_w] and self.y > 0 + self.radius and not self.hit_by(other_player):
                self.y -= 1
            elif pressed_keys[pygame.K_w] and self.y > 0 - self.radius:
                self.y += 2

            if pressed_keys[pygame.K_s] and self.y < 1080 - self.radius and not self.hit_by(other_player):
                self.y += 1
            elif pressed_keys[pygame.K_s] and self.y < 1080 - self.radius:
                self.y -= 2

            if pressed_keys[pygame.K_a] and self.x > 0 + self.radius and not self.hit_by(other_player):
                self.x -= 1
                if self.weapon_offset_x > 0:
                    self.weapon_offset_x *= -1
                    self.hammer = pygame.transform.flip(self.hammer, True, False)
            elif pressed_keys[pygame.K_a] and self.y < 1920 - self.radius:
                self.x += 2

            if pressed_keys[pygame.K_d] and self.x < 1920 - self.radius and not self.hit_by(other_player):
                self.x += 1
                if self.weapon_offset_x < 0:
                    self.weapon_offset_x *= -1
                    self.hammer = pygame.transform.flip(self.hammer, True, False)
            elif pressed_keys[pygame.K_d] and self.y < 1920 - self.radius:
                self.x -= 2

        if self.player_number == 2:
            if pressed_keys[pygame.K_UP] and self.y > 0 + self.radius and not self.hit_by(other_player):
                self.y -= 1
            elif pressed_keys[pygame.K_UP] and self.y > 0 - self.radius:
                self.y += 2

            if pressed_keys[pygame.K_DOWN] and self.y < 1080 - self.radius and not self.hit_by(other_player):
                self.y += 1
            elif pressed_keys[pygame.K_DOWN] and self.y < 1080 - self.radius:
                self.y -= 2

            if pressed_keys[pygame.K_LEFT] and self.x > 0 + self.radius and not self.hit_by(other_player):
                self.x -= 1
                if self.weapon_offset_x > 0:
                    self.weapon_offset_x *= -1
                    self.hammer = pygame.transform.flip(self.hammer, True, False)
            elif pressed_keys[pygame.K_LEFT] and self.x > 0 - self.radius:
                self.x += 2

            if pressed_keys[pygame.K_RIGHT] and self.x < 1920 - self.radius and not self.hit_by(other_player):
                self.x += 1
                if self.weapon_offset_x < 0:
                    self.weapon_offset_x *= -1
                    self.hammer = pygame.transform.flip(self.hammer, True, False)
            elif pressed_keys[pygame.K_RIGHT] and self.x < 1920 - self.radius:
                self.x -= 2

    def health_bar(self):
        pygame.draw.rect(self.screen, (239, 35, 60), pygame.Rect(self.x - self.radius,
                                                                 self.y - self.radius - 10, self.radius * 2, 5))

    def melee(self):
        if self.player_number == 1:
            print("1 melee")
        if self.player_number == 2:
            print("2 melee")
        # if self.angle > 300:
        #     self.hammer = pygame.transform.rotate(self.hammer, self.angle)
        #     self.angle -= 10
        #     print(self.angle)
        # if self.angle <= 360 and self.angle < 360:
        #     self.hammer = pygame.transform.rotate(self.hammer, self.angle)
        #     self.angle += 10

    def hit_by(self, other_player):
        player_hit_box = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
        other_player_hit_box = pygame.Rect(other_player.x, other_player.y, self.radius * 2, self.radius * 2)
        if player_hit_box.colliderect(other_player_hit_box):
            return True
        else:
            return False


        # hero_hit_box = pygame.Rect(self.x, self.y,
        #                            self.image_with_umbrella.get_width(), self.image_with_umbrella.get_height())
        # return hero_hit_box.collidepoint(raindrop.x, raindrop.y)


def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("ryan is hot")

    player1 = Player(screen, (141, 153, 174), 80, screen.get_height()/2, 30, 1)
    player2 = Player(screen, (217, 222, 224), screen.get_width() - 80, screen.get_height()/2, 30, 2)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            pressed_keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_q]:
                player1.melee()
            if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_SPACE]:
                player2.melee()


        pressed_keys = pygame.key.get_pressed()

        screen.fill((80, 80, 100))

        player1.move(pressed_keys, player2)
        player2.move(pressed_keys, player1)



        player1.draw()
        player2.draw()



        pygame.display.update()

main()
