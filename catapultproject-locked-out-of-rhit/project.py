import pygame
import sys
import random
import time

class Word_Generator:
    def __init__(self):
        with open('words.txt', 'r') as filehandle:
            self.words = filehandle.read().split('\n')

    def _get_random_word(self):
        return self.words[random.randrange(0, len(self.words))]

    def _remove_a_letter(self, word):
        letter_to_remove = word[random.randrange(0, len(word))]
        display_word = word.replace(letter_to_remove, "_")
        return letter_to_remove, display_word

    def generate_words(self, number_of_words):
        letters_removed = []
        display_words = []
        while True:
            if len(letters_removed) == number_of_words:
                return letters_removed, display_words
            word = self._get_random_word()
            letter, display_word = self._remove_a_letter(word)
            if not letter in letters_removed:
                letters_removed.append(letter)
                display_words.append(display_word)


class Arrow:
    def __init__(self, screen, game):
        """
        :type game: Game
        """
        self.screen = screen
        self.arrow_image = pygame.image.load("tinyarrow.PNG")
        self.game = game

        # pygame.transform.rotate(self.arrow_image, 1.5)
        # self.screen.blit(self.arrow_image, (200, 200))

    def draw (self):
        topleft = (80, 50)
        rotated_image = pygame.transform.rotate(self.arrow_image, self.game.angle)
        new_rect = rotated_image.get_rect(center=self.arrow_image.get_rect(topleft=topleft).center)

        self.screen.blit(rotated_image, new_rect)

    def move(self):
        self.game.angle -= 3


class Life_Display:
    def __init__(self, screen, game):
        self.screen = screen
        self.life_image = pygame.image.load("life.PNG")
        self.life_lost_image = pygame.image.load("lifelost.PNG")
        self.game = game
        IMAGE_SIZE = 69
        self.life_lost_image = pygame.transform.scale(self.life_lost_image, (IMAGE_SIZE, IMAGE_SIZE))
        self.life_image = pygame.transform.scale(self.life_image, (IMAGE_SIZE, IMAGE_SIZE))

    def draw(self):
        self.screen.blit(self.life_image, (401, 0))
        self.screen.blit(self.life_image, (476, 0))
        self.screen.blit(self.life_image, (551, 0))
        if self.game.lives < 3:
            self.screen.blit(self.life_lost_image, (400, 0))
        if self.game.lives < 2:
            self.screen.blit(self.life_lost_image, (475, 0))
        if self.game.lives < 1:
            self.screen.blit(self.life_lost_image, (550, 0))


class Timer_Display:
    def __init__(self, screen, game):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 30)
        self.game = game

    def draw(self):
        seconds_elapsed = round(time.time() - self.game.round_start_time)
        seconds_remaining = self.game.round_durations[self.game.round - 1] - seconds_elapsed
        if seconds_remaining <= 0:
            self.game.lives = 0
        caption = self.font.render(f"Time: {seconds_remaining}", True, (0, 0, 0))
        self.screen.blit(caption, (5, 40))


class Round_Display:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font = pygame.font.SysFont(None, 30)

    def draw(self):
        caption = self.font.render(f"Round: {self.game.round}", True, (0, 0, 0))
        self.screen.blit(caption, (5, 5))


class Display_Words:
    def __init__(self, screen, game):
        """
        :type game: Game
        """
        # ^ this is for autofill purposes

        self.screen = screen
        self.game = game
        self.font = pygame.font.SysFont(None, 30)
        self.star_image = pygame.image.load("star.PNG")
        self.wire_cutter_image = pygame.image.load("wire_cutters.PNG")

    def draw(self):
        if self.game.active_index == 0:
            self.screen.blit(self.wire_cutter_image, (self.screen.get_width() / 2 + 40, 35))

        elif self.game.active_index == 1:
            self.screen.blit(self.wire_cutter_image, (540, 160))

        elif self.game.active_index == 2:
            self.screen.blit(self.wire_cutter_image, (475, 375))

        elif self.game.active_index == 3:
            self.screen.blit(self.wire_cutter_image, (self.screen.get_width() / 2 - 150, 450))

        elif self.game.active_index == 4:
            self.screen.blit(self.wire_cutter_image, (50, 375))

        elif self.game.active_index == 5:
            self.screen.blit(self.wire_cutter_image, (50, 175))

        if self.game.is_card_active[0]:
            # self.screen.blit(self.wire_cutter_image, (200, 200)
            caption0 = self.font.render(self.game.display_words[0], True, (0, 0, 0))
            self.screen.blit(caption0, (self.screen.get_width() / 2 - caption0.get_width() / 2, 65))
        else:
            self.screen.blit(self.star_image, (self.screen.get_width() / 2 - 20, 35))

        if self.game.is_card_active[1]:
            caption1 = self.font.render(self.game.display_words[1], True, (0, 0, 0))
            self.screen.blit(caption1, (540 - caption1.get_width() / 2, 160))
        else:
            self.screen.blit(self.star_image, (540, 160))

        if self.game.is_card_active[2]:
            caption2 = self.font.render(self.game.display_words[2], True, (0, 0, 0))
            self.screen.blit(caption2, (540 - caption2.get_width() / 2, 350))
        else:
            self.screen.blit(self.star_image, (540, 350))

        if self.game.is_card_active[3]:
            caption3 = self.font.render(self.game.display_words[3], True, (0, 0, 0))
            self.screen.blit(caption3, (self.screen.get_width() / 2 - caption3.get_width() / 2, 500))
        else:
            self.screen.blit(self.star_image, (self.screen.get_width() / 2 - 20, 500))

        if self.game.is_card_active[4]:
            caption4 = self.font.render(self.game.display_words[4], True, (0, 0, 0))
            self.screen.blit(caption4, (100 - caption4.get_width() / 2, 350))
        else:
            self.screen.blit(self.star_image, (100, 350))

        if self.game.is_card_active[5]:
            caption5 = self.font.render(self.game.display_words[5], True, (0, 0, 0))
            self.screen.blit(caption5, (100 - caption5.get_width() / 2, 160))
        else:
            self.screen.blit(self.star_image, (100, 160))


class Game:
    def __init__(self):
        self.round = 1
        self.lives = 3
        self.feedback_message = ""
        self.word_generator = Word_Generator()
        self.missing_letters, self.display_words = self.word_generator.generate_words(6)
        self.active_index = random.randrange(0, 6)
        self.is_card_active = [True, True, True, True, True, True]
        self.round_start_time = time.time()
        self.round_durations = [120, 90, 60, 45, 30, 15]
        self.final_word = "Bob"
        self.angle = 0

    def reset(self):
        self.round = 1
        self.lives = 3
        self.feedback_message = ""
        self.missing_letters, self.display_words = self.word_generator.generate_words(6)
        self.active_index = random.randrange(0, 6)
        self.is_card_active = [True, True, True, True, True, True]
        self.round_start_time = time.time()
        self.angle = 0

    def start_next_round(self):
        self.round = self.round + 1
        self.round_start_time = time.time()
        self.missing_letters, self.display_words = self.word_generator.generate_words(6)
        self.active_index = random.randrange(0, 6)
        self.is_card_active = [True, True, True, True, True, True]

    def get_index(self):
        self.angle = self.angle % 360
        if 60 < self.angle <= 120:
            return 0
        elif 120 < self.angle <= 180:
            return 5
        elif 180 < self.angle <= 240:
            return 4
        elif 240 < self.angle <= 300:
            return 3
        elif 300 < self.angle <= 360:
            return 2
        else:
            return 1

    def __repr__(self):
        return f"\nRound:{self.round} Lives: {self.lives} Feedback Message: {self.feedback_message} \n" + \
        f"Missing Letters: {self.missing_letters} \nDisplay Words: {self.display_words} \nActive Index: {self.active_index} Is card active: {self.is_card_active}\n"

    def select_next_index(self):
        while True:
            if self.is_card_active[self.active_index]:
                break
            self.active_index = random.randrange(0, 6)
        self.final_word = self.display_words[self.active_index].replace("_", self.missing_letters[self.active_index])

    def guess(self, index, letter):
        sparkle_sparkle_sound = pygame.mixer.Sound("Level_XP Sounds (Minecraft) - Sound Effects for editing.wav")
        oof_sound = pygame.mixer.Sound("Minecraft Damage (Oof) - Sound Effect (HD).wav")
        get_hit_sound = pygame.mixer.Sound("Minecraft hit sound - 1080p60fps.wav")

        print(f"The User Guessed: index {index} letter {letter}")
        if index == self.active_index and letter == self.missing_letters[self.active_index]:
            self.is_card_active[index] = False
            if self.is_round_over():
                self.start_next_round()
                self.feedback_message = "Next Round"
                sparkle_sparkle_sound.play()
            else:
                self.select_next_index()
                self.feedback_message = "Correct"
                sparkle_sparkle_sound.play()
        elif index != self.active_index and letter == self.missing_letters[self.active_index]:
            self.feedback_message = "Correct letter, bad timing"
            get_hit_sound.play()
            self.lives = self.lives - 1

        elif index == self.active_index and letter != self.missing_letters[self.active_index]:
            self.feedback_message = "Wrong letter, good timing"
            get_hit_sound.play()
            self.lives = self.lives - 1

        elif index != self.active_index and letter != self.missing_letters[self.active_index]:
            self.feedback_message = "Wrong letter, bad timing"
            get_hit_sound.play()
            self.lives = self.lives - 1

    def is_round_over(self):
        for k in range(6):
            if self.is_card_active[k] == True:
                return False
        return True


class Final_Word_Display:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font = pygame.font.SysFont(None, 30)

    def draw(self):
        if self.game.lives <= 0:
            caption = self.font.render(self.game.final_word, True, (0, 150, 150))
            self.screen.blit(caption, (self.screen.get_width() - caption.get_width() - 10, 5))


class Feedback_Display:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font = pygame.font.SysFont(None, 30)

    def draw(self):
        caption = self.font.render(self.game.feedback_message, True, (0, 150, 150))
        self.screen.blit(caption, (self.screen.get_width() / 2 - caption.get_width()/2, 550))



def main():
    pygame.init()
    # turn on pygame

    pygame.display.set_caption("Defuse the bomb by typing in the missing letter(s) of the word next to the wire cutters!")
    # create a screen

    screen = pygame.display.set_mode((640, 580))
    # determine screen dimensions

    life_image = pygame.image.load("life.PNG")
    # load full heart image

    life_lost_image = pygame.image.load("lifelost.PNG")
    # load empty heart image

    bomb_image = pygame.image.load("bomb.png")
    # load bomb image

    circle_image = pygame.image.load("circle.PNG")
    # load circle image

    gameover_image = pygame.image.load("gameover.PNG")
    # load the game over page

    game = Game()
    arrow = Arrow(screen, game)
    life_display = Life_Display(screen, game)
    print(game)
    font = pygame.font.Font(None, 25)
    round = Round_Display(screen, game)
    feedback_display = Feedback_Display(screen, game)
    timer = Timer_Display(screen, game)
    display_words = Display_Words(screen, game)
    final_word_display = Final_Word_Display(screen, game)
    clock = pygame.time.Clock()
    clock.tick(60)
    # set the frame rate
    exploding_sound = pygame.mixer.Sound("TNT explosion.wav")
    # load the exploding TNT MC sound

    while True:
        for event in pygame.event.get():
            pressed_keys = pygame.key.get_pressed()
            # checking for pressed keys
            if event.type == pygame.QUIT:
                sys.exit()
                # so that you can exit the game
            if event.type == pygame.KEYDOWN:
                if game.lives <= 0:
                    if pressed_keys[pygame.K_y]:
                        game.reset()
                        # game resets when you hit y when you have no lives left
                # print(event.unicode, game.get_index())
                else:
                    game.guess(game.get_index(), event.unicode)
                    if game.lives <= 0:
                        exploding_sound.play()
                    time.sleep(.5)
                    # makes the arrow pause for 0.5 seconds after you select a letter
                    print(game)

        screen.fill((255, 255, 255))
        if game.lives <= 0:
            screen.blit(gameover_image, (0, 0))
            round.draw()
            final_word_display.draw()
            pygame.display.update()
            continue

        screen.blit(circle_image, (40, 60))
        arrow.move()
        arrow.draw()
        screen.blit(bomb_image, (170, 160))
        round.draw()
        feedback_display.draw()
        timer.draw()
        display_words.draw()
        life_display.draw()
        pygame.display.update()


main()
