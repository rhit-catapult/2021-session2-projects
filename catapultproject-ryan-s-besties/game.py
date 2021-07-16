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
        # self.hammer = pygame.image.load("hammer.png")
        self.player_number = player_number

        self.health = 100
        # self.hammer_x = 0
        # self.hammer_y = 0
        self.speed = 2
        self.melee_color = (80, 80, 150)

    def draw(self):
        self.draw_weapon()
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)


        self.health_bar()


    def draw_weapon(self):


        # self.hammer = pygame.transform.scale(self.hammer, (30, 30))
        # self.hammer_x = self.x - self.hammer.get_width() / 2 + self.weapon_offset_x
        # self.hammer_y = self.y + self.weapon_offset_y
        #
        # self.screen.blit(self.hammer, (self.hammer_x, self.hammer_y))
        pygame.draw.circle(self.screen, self.melee_color, (self.x, self.y), self.radius * 2)


    def move(self, pressed_keys, other_player):

        if self.player_number == 1:

            if pressed_keys[pygame.K_w] and self.y > 0 + self.radius and not self.hit_by("top", other_player):

                self.y -= self.speed

            if pressed_keys[pygame.K_s] and self.y < 1080 - self.radius and not self.hit_by("bottom", other_player):

                self.y += self.speed

            if pressed_keys[pygame.K_a] and self.x > 0 + self.radius and not self.hit_by("left", other_player):

                self.x -= self.speed


            if pressed_keys[pygame.K_d] and self.x < 1920 - self.radius and not self.hit_by("right", other_player):

                self.x += self.speed


        if self.player_number == 2:
            if pressed_keys[pygame.K_UP] and self.y > 0 + self.radius and not self.hit_by("top", other_player):

                self.y -= self.speed

            if pressed_keys[pygame.K_DOWN] and self.y < 1080 - self.radius and not self.hit_by("bottom", other_player):
                self.y += self.speed

            if pressed_keys[pygame.K_LEFT] and self.x > 0 + self.radius and not self.hit_by("left", other_player):
                self.x -= self.speed


            if pressed_keys[pygame.K_RIGHT] and self.x < 1920 - self.radius and not self.hit_by("right", other_player):
                self.x += self.speed


    def health_bar(self):
        health_bar_percentage = (1 - (self.health / 100)) * 60

        if self.y > 40:
            pygame.draw.rect(self.screen, (239, 35, 60), pygame.Rect(self.x - self.radius,
                                                                     self.y - self.radius - 10,
                                                                     self.radius * 2 - health_bar_percentage, 5))
        else:
            pygame.draw.rect(self.screen, (239, 35, 60), pygame.Rect(self.x - self.radius,
                                                                     self.y - self.radius + self.radius * 2 + 5,
                                                                     self.radius * 2 - health_bar_percentage, 5))

    def melee(self, other_player):

        hammer_hit_box = pygame.Rect((self.x - 20, self.y - 20), (100, 100))
        other_player_hitbox = pygame.Rect(other_player.x, other_player.y, self.radius * 2, self.radius * 2)

        if hammer_hit_box.colliderect(other_player_hitbox):
            other_player.health -= 10
            print("health " + str(other_player.player_number) + ": " + str(other_player.health))

        # temporary
        if other_player.health <= 0:
            print("player" + str(self.player_number) + " has won")

    def hit_by(self, direction, other_player):

        # player_hit_box = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
        other_player_hit_box = pygame.Rect(other_player.x - self.radius, other_player.y - self.radius, self.radius * 2, self.radius * 2)

        if direction == "top":

            return other_player_hit_box.collidepoint((self.x - self.radius, self.y - self.radius)) or other_player_hit_box.collidepoint(
                (self.x + self.radius, self.y - self.radius))


        if direction == "bottom":

            return other_player_hit_box.collidepoint(
                (self.x - self.radius, self.y + self.radius)) or other_player_hit_box.collidepoint(self.x + self.radius,
                                                                                         self.y + self.radius)


        if direction == "left":

            return other_player_hit_box.collidepoint((self.x - self.radius, self.y - self.radius)) or other_player_hit_box.collidepoint(
                (self.x - self.radius, self.y + self.radius))


        if direction == "right":

            return other_player_hit_box.collidepoint(
                (self.x + self.radius, self.y - self.radius)) or other_player_hit_box.collidepoint(
                (self.x + self.radius, self.y + self.radius))






def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("ryan is hot")


    player1 = Player(screen, (141, 153, 174), 80, screen.get_height() / 2, 30, 1)
    player2 = Player(screen, (217, 222, 224), screen.get_width() - 80, screen.get_height() / 2, 30, 2)



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            pressed_keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_q]:
                player1.melee(player2)
            if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_SPACE]:
                player2.melee(player1)

        pressed_keys = pygame.key.get_pressed()

        screen.fill((80, 80, 100))



        player1.move(pressed_keys, player2)
        player2.move(pressed_keys, player1)

        player1.draw()
        player2.draw()

        pygame.display.update()


main()
