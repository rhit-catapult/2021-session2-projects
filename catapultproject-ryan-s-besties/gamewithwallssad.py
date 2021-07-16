import pygame, sys, math, random, time


class Player:
    def __init__(self, screen, color, x, y, radius, player_number, map):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.weapon_offset_x = radius
        self.weapon_offset_y = -25
        self.hammer = pygame.image.load("hammer.png")
        self.player_number = player_number
        self.map = map
        self.health = 100
        self.hammer_x = 0
        self.hammer_y = 0
        self.speed = 2

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

        self.draw_weapon()
        self.health_bar()

    def draw_weapon(self):
        self.hammer = pygame.transform.scale(self.hammer, (30, 30))
        self.hammer_x = self.x - self.hammer.get_width() / 2 + self.weapon_offset_x
        self.hammer_y = self.y + self.weapon_offset_y

        self.screen.blit(self.hammer, (self.hammer_x, self.hammer_y))

    def move(self, pressed_keys, other_player):

        if self.player_number == 1:

            if pressed_keys[pygame.K_w] and self.y > 0 + self.radius and not self.hit_by("top", other_player):
                self.map.wall_collision("top", self)
                print(self.map.wall_hit_top)
                if not self.map.wall_hit_top:
                    self.y -= self.speed

            if pressed_keys[pygame.K_s] and self.y < 1080 - self.radius and not self.hit_by("bottom", other_player):
                self.map.wall_collision("bottom", self)
                if not self.map.wall_hit_bottom:
                    self.y += self.speed

            if pressed_keys[pygame.K_a] and self.x > 0 + self.radius and not self.hit_by("left", other_player):
                self.map.wall_collision("left", self)
                if not self.map.wall_hit_left:
                    self.x -= self.speed
                    if self.weapon_offset_x > 0:
                        self.weapon_offset_x *= -1
                        self.hammer = pygame.transform.flip(self.hammer, True, False)

            if pressed_keys[pygame.K_d] and self.x < 1920 - self.radius and not self.hit_by("right", other_player):
                self.map.wall_collision("right", self)
                if not self.map.wall_hit_right:
                    self.x += self.speed
                    if self.weapon_offset_x < 0:
                        self.weapon_offset_x *= -1
                        self.hammer = pygame.transform.flip(self.hammer, True, False)

        if self.player_number == 2:
            if pressed_keys[pygame.K_UP] and self.y > 0 + self.radius and not self.hit_by("top", other_player) \
                    and not self.map.wall_hit == True:
                self.y -= self.speed

            if pressed_keys[pygame.K_DOWN] and self.y < 1080 - self.radius and not self.hit_by("bottom", other_player) \
                    and not self.map.wall_hit == True:
                self.y += self.speed

            if pressed_keys[pygame.K_LEFT] and self.x > 0 + self.radius and not self.hit_by("left", other_player) \
                    and not self.map.wall_hit == True:
                self.x -= self.speed
                if self.weapon_offset_x > 0:
                    self.weapon_offset_x *= -1
                    self.hammer = pygame.transform.flip(self.hammer, True, False)

            if pressed_keys[pygame.K_RIGHT] and self.x < 1920 - self.radius and not self.hit_by("right", other_player) \
                    and not self.map.wall_hit == True:
                self.x += self.speed
                if self.weapon_offset_x < 0:
                    self.weapon_offset_x *= -1
                    self.hammer = pygame.transform.flip(self.hammer, True, False)

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


class Map:
    def __init__(self, screen):
        self.screen = screen
        self.wall_arrangement = [(500, 500), (700, 700)]
        self.wall_hit_boxes = []
        self.wall_hit_top = False
        self.wall_hit_bottom = False
        self.wall_hit_left = False
        self.wall_hit_right = False

        for walls in self.wall_arrangement:
            self.wall_hit_boxes.append(pygame.Rect(walls, (60, 60)))



    def draw(self):
        for walls in self.wall_arrangement:

            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(walls, (60, 60)))


    def wall_collision(self, direction, player):
        counter_top = 0
        counter_bottom = 0
        counter_left = 0
        counter_right = 0
        for wall_hit_box in self.wall_hit_boxes:

            if direction == "top":

                if wall_hit_box.collidepoint((player.x - player.radius, player.y - player.radius))\
                        or wall_hit_box.collidepoint((player.x + player.radius, player.y - player.radius)):
                    self.wall_hit_top = True
                    print("top works" + str(wall_hit_box) + str(self.wall_hit_top))

                # elif not wall_hit_box.collidepoint(
                #     (player.x + player.radius, player.y - player.radius)) \
                #         or wall_hit_box.collidepoint((player.x + player.radius, player.y + player.radius)):
                #     self.wall_hit_top = False
                #     print("top works" + str(wall_hit_box) + str(self.wall_hit_top))
            if direction == "bottom":

                if wall_hit_box.collidepoint(
                    (player.x - player.radius, player.y + player.radius))\
                        or wall_hit_box.collidepoint((player.x + player.radius, player.y + player.radius)):
                    self.wall_hit_bottom = True
                    print("tbot works" + str(wall_hit_box) + str(self.wall_hit_bottom))
                # elif not wall_hit_box.collidepoint(
                #     (player.x + player.radius, player.y - player.radius)) \
                #         or wall_hit_box.collidepoint((player.x + player.radius, player.y + player.radius)):
                #
                #     self.wall_hit_bottom = False
                #     print("tbot works" + str(wall_hit_box) + str(self.wall_hit_bottom))

            if direction == "left":

                if wall_hit_box.collidepoint((player.x - player.radius, player.y - player.radius)) \
                        or wall_hit_box.collidepoint((player.x - player.radius, player.y + player.radius)):
                    self.wall_hit_left = True
                    print("lef works" + str(wall_hit_box) + str(self.wall_hit_left))
                # elif not wall_hit_box.collidepoint(
                #     (player.x + player.radius, player.y - player.radius)) \
                #         or wall_hit_box.collidepoint((player.x + player.radius, player.y + player.radius)):
                #
                #     self.wall_hit_left = False
                #     print("lef works" + str(wall_hit_box) + str(self.wall_hit_left))

            if direction == "right":

                if wall_hit_box.collidepoint(
                    (player.x + player.radius, player.y - player.radius)) \
                        or wall_hit_box.collidepoint((player.x + player.radius, player.y + player.radius)):
                    self.wall_hit_right = True
                    print("rigtp works" + str(wall_hit_box) + str(self.wall_hit_right))
                # elif not wall_hit_box.collidepoint(
                #     (player.x + player.radius, player.y - player.radius)) \
                #         or wall_hit_box.collidepoint((player.x + player.radius, player.y + player.radius)):
                #     self.wall_hit_right = False
                #     print("rigtp works" + str(wall_hit_box) + str(self.wall_hit_right))

        for wall_hit_box in self.wall_hit_boxes:

            if not wall_hit_box.collidepoint((player.x - player.radius, player.y - player.radius))\
                    or wall_hit_box.collidepoint((player.x + player.radius, player.y - player.radius)):
                counter_top += 1
            if counter_top == len(self.wall_hit_boxes):
                self.wall_hit_top = False


            if not wall_hit_box.collidepoint(
                (player.x - player.radius, player.y + player.radius))\
                    or wall_hit_box.collidepoint((player.x + player.radius, player.y + player.radius)):
                counter_bottom += 1
            if counter_bottom == len(self.wall_hit_boxes):
                self.wall_hit_bottom = False


            if not wall_hit_box.collidepoint((player.x - player.radius, player.y - player.radius)) \
                    or wall_hit_box.collidepoint((player.x - player.radius, player.y + player.radius)):
                counter_left += 1
            if counter_left == len(self.wall_hit_boxes):
                self.wall_hit_left = False


            if not wall_hit_box.collidepoint(
                (player.x + player.radius, player.y - player.radius)) \
                    or wall_hit_box.collidepoint((player.x + player.radius, player.y + player.radius)):
                counter_right += 1
            if counter_right == len(self.wall_hit_boxes):
                self.wall_hit_right = False





        # self.wall_hit_top = False
        # self.wall_hit_bottom = False
        # self.wall_hit_left = False
        # self.wall_hit_right = False





def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("ryan is hot")

    map = Map(screen)
    player1 = Player(screen, (141, 153, 174), 80, screen.get_height() / 2, 30, 1, map)
    player2 = Player(screen, (217, 222, 224), screen.get_width() - 80, screen.get_height() / 2, 30, 2, map)

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
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

        map.draw()

        player1.move(pressed_keys, player2)
        player2.move(pressed_keys, player1)

        player1.draw()
        player2.draw()

        pygame.display.update()


main()
