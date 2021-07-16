import pygame, sys, math, random, time


class Player:
    def __init__(self, screen, color, x, y, radius, player_number, menu):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.weapon_offset_x = radius
        self.weapon_offset_y = -25
        # self.hammer = pygame.image.load("hammer.png")
        self.player_number = player_number
        self.menu = menu

        self.health = 100
        # self.hammer_x = 0
        # self.hammer_y = 0
        self.speed = 3
        self.melee_color = (80, 80, 150)
        self.is_facing = ""

    def draw(self):
        # self.draw_weapon()
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

        self.health_bar()


    # def draw_weapon(self):
    #
    #
    #     # self.hammer = pygame.transform.scale(self.hammer, (30, 30))
    #     # self.hammer_x = self.x - self.hammer.get_width() / 2 + self.weapon_offset_x
    #     # self.hammer_y = self.y + self.weapon_offset_y
    #     #
    #     # self.screen.blit(self.hammer, (self.hammer_x, self.hammer_y))
    #     pygame.draw.circle(self.screen, self.melee_color, (self.x, self.y), self.radius * 2)


    def move(self, pressed_keys, other_player):

        if self.player_number == 1:

            if pressed_keys[pygame.K_r] and self.y > 0 + self.radius and not self.hit_by("top", other_player):

                self.y -= self.speed

                self.is_facing = "up"

            if pressed_keys[pygame.K_f] and self.y < 1080 - self.radius and not self.hit_by("bottom", other_player):

                self.y += self.speed

                self.is_facing = "down"

            if pressed_keys[pygame.K_d] and self.x > 0 + self.radius and not self.hit_by("left", other_player):

                self.x -= self.speed

                self.is_facing = "left"

            if pressed_keys[pygame.K_g] and self.x < 1920 - self.radius and not self.hit_by("right", other_player):

                self.x += self.speed

                self.is_facing = "right"

        if self.player_number == 2:
            if pressed_keys[pygame.K_UP] and self.y > 0 + self.radius and not self.hit_by("top", other_player):

                self.y -= self.speed

                self.is_facing = "up"

            if pressed_keys[pygame.K_DOWN] and self.y < 1080 - self.radius and not self.hit_by("bottom", other_player):
                self.y += self.speed

                self.is_facing = "down"

            if pressed_keys[pygame.K_LEFT] and self.x > 0 + self.radius and not self.hit_by("left", other_player):
                self.x -= self.speed

                self.is_facing = "left"


            if pressed_keys[pygame.K_RIGHT] and self.x < 1920 - self.radius and not self.hit_by("right", other_player):
                self.x += self.speed

                self.is_facing = "right"

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

        if self.health <= 0:
            self.menu.end_game(self)


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

    def hit_bullet(self, bullet):
        player_hit_box = pygame.Rect(self.x - 30, self.y - 30, 60, 60)
        return player_hit_box.colliderect(bullet.hit_box)

        

class Item:
    def __init__(self, screen, x, y, slot, cooldown, damage, hit_box, texture, offset, menu):
        self.x = x
        self.y = y
        self.screen = screen
        self.slot = slot
        self.cooldown = cooldown
        self.damage = damage
        self.hit_box = hit_box
        self.texture = texture
        self.offset = offset
        self.menu = menu

    def deal_damage(self, other_player):
        if self.menu.game_status == "play":
            other_player.health -= self.damage
            print("health " + str(other_player.player_number) + ": " + str(other_player.health))

    def update_pos(self, player):
        self.x = player.x
        self.y = player.y
        if self.offset == -1:
            self.x -= self.texture.get_width() / 2 + 20

    def flip(self):
        self.texture = pygame.transform.flip(self.texture, True, False)
        self.offset *= -1

    def draw(self):
        self.screen.blit(self.texture, (self.x, self.y))


class Melee(Item):
    def __init__(self, screen, x, y, slot, color, menu):
        self.cooldown = 0.1
        self.damage = 8
        self.color = color
        self.hit_box = pygame.Rect(x - 50, y - 50, 100, 100)
        self.texture = pygame.image.load("gun.png")
        self.offset = 0
        self.menu = menu
        self.melee_radius = 30
        self.is_animating = False
        Item.__init__(self, screen, x, y, slot, self.cooldown, self.damage, self.hit_box, self.texture, self.offset, self.menu)

    def attack(self, x, y, other_player):
        self.hit_box = pygame.Rect(x - 50, y - 50, 100, 100)
        other_player_hit_box = pygame.Rect(other_player.x - 30, other_player.y - 30, 60, 60)
        if self.hit_box.colliderect(other_player_hit_box):
            self.deal_damage(other_player)
        self.is_animating = True

    def draw(self, x, y):
        if self.is_animating:
            if self.melee_radius < 60:
                self.melee_radius += 3.5
            if self.melee_radius >= 60:
                self.melee_radius = 0
                self.is_animating = False

            pygame.draw.circle(self.screen, self.color, (x, y), self.melee_radius, 3)


class Gun(Item):
    def __init__(self, screen, x, y, slot, menu):
        self.x = x
        self.y = y
        self.cooldown = 0.5
        self.damage = 3
        self.texture = pygame.image.load("gun.png")
        self.texture = pygame.transform.scale(self.texture, (int(self.texture.get_width() / 10),
                                                             int(self.texture.get_height() / 10)))
        self.menu = menu
        self.hit_box = pygame.Rect(self.x, self.y, self.texture.get_width(), self.texture.get_height())
        self.offset = 1
        self.bullet_list = []
        self.bullet_speed_x = 10
        self.bullet_speed_y = 10
        Item.__init__(self, screen, self.x, self.y, slot, self.cooldown, self.damage, self.hit_box, self.texture, self.offset, self.menu)

    def fire(self):
        new_bullet = Bullet(self.screen, self.x, self.y, self.bullet_speed_x, self.bullet_speed_y, self.damage)
        self.bullet_list.append(new_bullet)

    def keys_1(self, player1, player2, player1_weapon, player2_weapon, event):
        pressed_keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_q]:
            player1_weapon.attack(player1.x, player1.y, player2)
        if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_PERIOD]:
            player2_weapon.attack(player2.x, player2.y, player1)

        if self.slot == 1 and self.offset == 1 and pressed_keys[pygame.K_d]:
            self.flip()
        if self.slot == 1 and self.offset == -1 and pressed_keys[pygame.K_g]:
            self.flip()
        if self.slot == 2 and self.offset == 1 and pressed_keys[pygame.K_LEFT]:
            self.flip()
        if self.slot == 2 and self.offset == -1 and pressed_keys[pygame.K_RIGHT]:
            self.flip()

        if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_a] and self.slot == 1:
            if player1.is_facing == "up":
                self.bullet_speed_y = -10
                self.bullet_speed_x = 0
                self.fire()
            elif player1.is_facing == "right":
                self.bullet_speed_x = 10
                self.bullet_speed_y = 0
                self.fire()
            elif player1.is_facing == "down":
                self.bullet_speed_y = 10
                self.bullet_speed_x = 0
                self.fire()
            elif player1.is_facing == "left":
                self.bullet_speed_x = -10
                self.bullet_speed_y = 0
                self.fire()
        if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_COMMA] and self.slot == 2:
            if player2.is_facing == "up":
                self.bullet_speed_y = -10
                self.bullet_speed_x = 0
                self.fire()
            elif player2.is_facing == "right":
                self.bullet_speed_x = 10
                self.bullet_speed_y = 0
                self.fire()
            elif player2.is_facing == "down":
                self.bullet_speed_y = 10
                self.bullet_speed_x = 0
                self.fire()
            elif player2.is_facing == "left":
                self.bullet_speed_x = -10
                self.bullet_speed_y = 0
                self.fire()

    def keys_2(self, player1, player2):
        for bullets in self.bullet_list:
            bullets.move_x()
            bullets.move_y()
            bullets.draw()

        if self.slot == 1:
            self.update_pos(player1)
        elif self.slot == 2:
            self.update_pos(player2)

    def remove_hit_bullets(self):
        for k in range(len(self.bullet_list) -1, -1, -1):
            if self.bullet_list[k].has_hit or self.bullet_list[k].y > 1085 or self.bullet_list[k].y < -5 or \
                    self.bullet_list[k].x < -5 or self.bullet_list[k].x > 1925:
                del self.bullet_list[k]


class Bullet:
    def __init__(self, screen, x, y, speed_x, speed_y, damage):
        self.screen = screen
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.has_hit = False
        self.damage = damage
        self.hit_box = pygame.Rect(self.x - 5, self.y - 5, 10, 10)

    def move_x(self):
        self.x += self.speed_x

    def move_y(self):
        self.y += self.speed_y

    def draw(self):
        pygame.draw.circle(self.screen, pygame.Color("Black"), (self.x, self.y), 5)
        self.hit_box = pygame.Rect(self.x - 5, self.y - 5, 10, 10)


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.game_status = "play"

    def end_game(self, player):
        font1 = pygame.font.Font(None, 80)
        font2 = pygame.font.Font(None, 60)
        if player.player_number == 1:
            caption1 = font1.render("Player 2" + " Wins!", True, pygame.Color("white"))
            caption2 = font2.render("Press Space to Play Again!", True, (20, 20, 28))
            self.screen.blit(caption1, (self.screen.get_width() / 2 - caption1.get_width() / 2, self.screen.get_height()/2 - 40))
            self.screen.blit(caption2, (self.screen.get_width() / 2 - caption2.get_width() / 2, self.screen.get_height()/2 + 40))

        if player.player_number == 2:
            caption1 = font1.render("Player 1" + " Wins!", True, pygame.Color("white"))
            caption2 = font2.render("Press Space to Play Again!", True, (20, 20, 28))
            self.screen.blit(caption1, (self.screen.get_width() / 2 - caption1.get_width() / 2, self.screen.get_height()/2 - 40))
            self.screen.blit(caption2, (self.screen.get_width() / 2 - caption2.get_width() / 2, self.screen.get_height()/2 + 40))

        self.game_status = "ended"


def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Street Fighter: Circle Edition")

    menu = Menu(screen)

    player1 = Player(screen, (196,92,84), 80, screen.get_height() / 2, 30, 1, menu)
    player2 = Player(screen, (80,140,140), screen.get_width() - 80, screen.get_height() / 2, 30, 2, menu)

    player1_weapon = Melee(screen, player1.x, player1.y, 1, (196,92,84), menu)
    player2_weapon = Melee(screen, player2.x, player2.y, 2, (80,140,140), menu)

    gun1 = Gun(screen, 500, 500, 1, menu)
    gun2 = Gun(screen, screen.get_width() - 500, 500, 2, menu)

    clock = pygame.time.Clock()
    while True:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            gun1.keys_1(player1, player2, player1_weapon, player2_weapon, event)
            gun2.keys_1(player1, player2, player1_weapon, player2_weapon, event)

            pressed_keys = pygame.key.get_pressed()

            if menu.game_status == "ended":
                if event.type == pygame.KEYDOWN and pressed_keys[pygame.K_SPACE]:
                    menu.game_status = "play"
                    player1.health = 100
                    player2.health = 100
                    player1.x = 80
                    player1.y = screen.get_height() / 2
                    player2.x = screen.get_width() - 80
                    player2.y = screen.get_height() / 2

        screen.fill((212, 196, 172))

        # Controls Display
        # Player 1
        font = pygame.font.Font(None, 25)
        caption1_1 = font.render("Player 1:", True, (0, 0, 0))
        caption1_2 = font.render("r - up d - left", True, (0, 0, 0))
        caption1_3 = font.render("f - down g - right", True, (0, 0, 0))
        caption1_4 = font.render("a - shoot q - melee", True, (0, 0, 0))
        caption2_1 = font.render("Player 2:", True, (0, 0, 0))
        caption2_2 = font.render("arrow keys", True, (0, 0, 0))
        caption2_3 = font.render(", - shoot . - melee", True, (0, 0, 0))
        screen.blit(caption1_1, (20, 980))
        screen.blit(caption1_2, (20, 1000))
        screen.blit(caption1_3, (20, 1020))
        screen.blit(caption1_4, (20, 1040))
        screen.blit(caption2_1, (screen.get_width() - 160, 1000))
        screen.blit(caption2_2, (screen.get_width() - 160, 1020))
        screen.blit(caption2_3, (screen.get_width() - 160, 1040))

        player1.move(pressed_keys, player2)
        player2.move(pressed_keys, player1)

        gun1.keys_2(player1, player2)
        gun2.keys_2(player1, player2)

        player1_weapon.draw(player1.x, player1.y)
        player2_weapon.draw(player2.x, player2.y)

        for bullets in gun1.bullet_list:
            if player2.hit_bullet(bullets) and menu.game_status == "play":
                player2.health -= bullets.damage
                bullets.has_hit = True

        for bullets in gun2.bullet_list:
            if player1.hit_bullet(bullets) and menu.game_status == "play":
                player1.health -= bullets.damage
                bullets.has_hit = True

        gun1.remove_hit_bullets()
        gun2.remove_hit_bullets()

        player1.draw()
        player2.draw()

        gun1.draw()
        gun2.draw()

        pygame.display.update()


main()

