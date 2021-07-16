import pygame
import sys
import random


class Card:
    def __init__(self, screen, suit, value):
        self.screen = screen
        self.suit = suit
        self.value = value
        self.image = pygame.image.load(str(self.value) + self.suit + ".png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 11, self.image.get_height() // 11))

    def draw(self, x, y):
        pass
        self.screen.blit(self.image, (x, y))

    def __repr__(self):
        return self.suit + str(self.value)


class Deck:
    def __init__(self, screen):
        self.screen = screen
        suitList = ["H", "D", "C", "S"]
        self.cardList = []
        for k in range(1, 14):
            for suit in suitList:
                self.cardList.append(Card(self.screen, suit, k))
        random.shuffle(self.cardList)

    def __repr__(self):
        return self.cardList

    def shuffle(self):
        suitList = ["H", "D", "C", "S"]
        self.cardList = []
        for k in range(1, 14):
            for suit in suitList:
                self.cardList.append(Card(self.screen, suit, k))
        random.shuffle(self.cardList)

    def drawCard(self):
        if len(self.cardList) == 0:
            self.shuffle()
            return self.drawCard()
        else:
            return self.cardList.pop()


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.deck = Deck(self.screen)
        self.playerMoney = 100
        self.playerScore = 0
        self.AIScore = 0
        self.playerCardsDrawn = []
        self.gameStatus = "Start"
        self.AICardsDrawn = []
        self.bet = 0
        self.twoBet = 0
        self.gameOverOne = False
        self.gameOverTwo = False
        self.hasWonOne = False
        self.hasWonTwo = False
        self.playerTwoScore = 0
        self.playerTwoCardsDrawn = []
        self.playerTwoMoney = 100
        self.activePlayer = 1
        self.playerOneDone = False
        self.playerTwoDone = False
        self.canBet = True

    def convertValue(self, card):
        x = 0
        y = 0
        if self.activePlayer == 1:
            if 1 < card.value < 10:
                return card.value
            elif card.value == 1:
                for k in range(len(self.playerCardsDrawn)):
                    if self.playerCardsDrawn[k].value != 1:
                        x += self.convertValue(self.playerCardsDrawn[k])
                    else:
                        if y == 1:
                            return 1
                        else:
                            y += 1
                if x <= 10:
                    return 11
                else:
                    return 1
            else:
                return 10
        else:
            if 1 < card.value < 10:
                return card.value
            elif card.value == 1:
                for k in range(len(self.playerTwoCardsDrawn)):
                    if self.playerTwoCardsDrawn[k].value != 1:
                        x += self.convertValue(self.playerTwoCardsDrawn[k])
                if x <= 10:
                    return 11
                else:
                    return 1
            else:
                return 10

    def AIConvertValue(self, card):
        x = 0
        if 1 < card.value < 10:
            return card.value
        elif card.value == 1:
            for k in range(len(self.AICardsDrawn)):
                if self.AICardsDrawn[k].value != 1:
                    x += self.AIConvertValue(self.AICardsDrawn[k])
            print(x)
            if x <= 10:
                return 11
            else:
                return 1
        else:
            return 10

    def loseOne(self):
        self.playerMoney -= self.bet
        if self.playerMoney < 10:
            self.gameOverOne = True

    def winOne(self):
        self.playerMoney += self.bet
        if self.playerMoney >= 5000:
            self.hasWonOne = True

    def loseTwo(self):
        self.playerTwoMoney -= self.twoBet
        if self.playerTwoMoney < 10:
            self.gameOverTwo = True

    def winTwo(self):
        self.playerTwoMoney += self.twoBet
        if self.playerTwoMoney >= 5000:
            self.hasWonTwo = True

    def manageEnd(self):
        if self.AIScore == 21:
            self.gameStatus = "Dealer Win"
            self.loseOne()
            self.loseTwo()
        if self.playerOneDone and self.playerTwoDone:
            while self.AIScore < 17:
                self.AIPlay()
            #if self.AIScore == 21:
             #   self.gameStatus = "Dealer Win"
             #   self.loseOne()
             #   self.loseTwo()
            if self.AIScore > 21:
                if self.playerScore <= 21:
                    self.winOne()
                else:
                    self.loseOne()
                    self.gameStatus = "Dealer Bust Player One Bust"
                if self.playerTwoScore <= 21:
                    self.winTwo()
                else:
                    self.gameStatus = "Dealer Bust Player Two Bust"
                    self.loseTwo()
                if self.gameStatus != "Dealer Bust Player One Bust" or self.gameStatus != "Dealer Bust Player Two Bust":
                    self.gameStatus = "Dealer Bust"
            elif self.playerScore > 21 and self.playerTwoScore > 21:
                self.loseOne()
                self.loseTwo()
                self.gameStatus = "Player One Bust Player Two Bust"
            elif self.playerScore > 21:
                if self.playerTwoScore > self.AIScore:
                    self.winTwo()
                    self.gameStatus = "Player Two Win"
                elif self.playerTwoScore < self.AIScore:
                    self.loseTwo()
                    self.gameStatus = "Dealer Win"
                else:
                    self.gameStatus = "Player Two Push"
                self.loseOne()
            elif self.playerTwoScore > 21:
                if self.playerScore > self.AIScore:
                    self.winOne()
                    self.gameStatus = "Player One Win"
                elif self.playerScore < self.AIScore:
                    self.loseOne()
                    self.gameStatus = "Dealer Win"
                else:
                    self.gameStatus = "Player One Push"
                self.loseTwo()
            else:
                self.gameStatus = ""
                if self.playerScore > self.AIScore:
                    self.winOne()
                    self.gameStatus += "Player One Win "
                if self.playerScore == self.AIScore:
                    self.gameStatus += "Player One Push "
                if self.playerTwoScore > self.AIScore:
                    self.winTwo()
                    self.gameStatus += "Player Two Win"
                if self.playerTwoScore == self.AIScore:
                    self.gameStatus += "Player Two Push"
                if self.playerScore < self.AIScore and self.playerTwoScore < self.AIScore:
                    self.loseTwo()
                    self.loseOne()
                    self.gameStatus = "Dealer Win"
                elif self.playerTwoScore < self.AIScore:
                    self.loseTwo()
                if self.playerScore < self.AIScore:
                    self.loseOne()

    def resetTurn(self):
        self.playerScore = 0
        self.playerTwoScore = 0
        self.AIScore = 0
        self.bet = 0
        self.twoBet = 0
        self.playerCardsDrawn = []
        self.playerTwoCardsDrawn = []
        self.AICardsDrawn = []
        self.gameStatus = "Start"
        if not self.gameOverOne:
            self.playerOneDone = False
        if not self.gameOverTwo:
            self.playerTwoDone = False
        if not self.gameOverOne:
            self.activePlayer = 1
        else:
            self.activePlayer = 2
        self.canBet = True

    def AIPlay(self):
        x = 0
        if self.AIScore < 17:
            y = self.deck.drawCard()
            self.AICardsDrawn.append(y)
        for k in range(len(self.AICardsDrawn)):
            x += self.AIConvertValue(self.AICardsDrawn[k])
        self.AIScore = x

    def takeTurn(self, x):
        y = 0
        z = 0
        a = 0
        b = 0
        if self.activePlayer == 1 and not self.playerOneDone and not self.canBet:
            if self.gameStatus == "Start":
                self.gameStatus = "Ongoing"
            if x == "hit":
                if self.bet != 0:
                    if len(self.playerCardsDrawn) == 0:
                        self.playerCardsDrawn.append(self.deck.drawCard())
                        if not self.gameOverTwo:
                            self.playerTwoCardsDrawn.append(self.deck.drawCard())
                            self.playerTwoCardsDrawn.append(self.deck.drawCard())
                        self.AIPlay()
                        self.AIPlay()
                        if self.AIScore == 21:
                            self.manageEnd()
                        for i in range(len(self.playerCardsDrawn)):
                            a += self.convertValue(self.playerCardsDrawn[i])
                        self.activePlayer = 2
                        for j in range(len(self.playerTwoCardsDrawn)):
                            b += self.convertValue(self.playerTwoCardsDrawn[j])
                        self.activePlayer = 1
                        if a == 21 or b == 21:
                            self.manageEnd()
                    self.playerCardsDrawn.append(self.deck.drawCard())
                    for k in range(len(self.playerCardsDrawn)):
                        y += self.convertValue(self.playerCardsDrawn[k])
                    self.playerScore = y
                    if self.playerScore > 21:
                        self.manageEnd()
                        self.playerOneDone = True
                        if not self.playerTwoDone:
                            self.activePlayer = 2
            if x == "stand" and self.bet != 0:
                self.manageEnd()
                self.playerOneDone = True
                if not self.playerTwoDone:
                    self.activePlayer = 2
        elif not self.playerTwoDone and not self.canBet:
            if self.gameStatus == "Start":
                self.gameStatus = "Ongoing"
            if len(self.playerTwoCardsDrawn) == 0:
                self.playerTwoCardsDrawn.append(self.deck.drawCard())
                self.AIPlay()
                self.AIPlay()
            if x == "hit":
                self.playerTwoCardsDrawn.append(self.deck.drawCard())
                for i in range(len(self.playerTwoCardsDrawn)):
                    z += self.convertValue(self.playerTwoCardsDrawn[i])
                self.playerTwoScore = z
                if self.playerTwoScore > 21:
                    self.playerTwoDone = True
                    self.manageEnd()
            if x == "stand" and self.twoBet != 0:
                self.playerTwoDone = True
                self.manageEnd()
        else:
            self.manageEnd()


class viewController:
    def __init__(self, screen, screenWidth, screenHeight):
        self.screen = screen
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.game = Game(screen)
        self.deckImage = pygame.image.load("red_back.png")
        self.deckImage = pygame.transform.scale(self.deckImage,
                                                (self.deckImage.get_width() // 11, self.deckImage.get_height() // 11))
        self.standButtonImage = pygame.image.load("test button stand.png")
        self.font = pygame.font.Font(None, 35)
        self.chipImage = pygame.image.load("pokerchip.png")
        self.chipImage = pygame.transform.scale(self.chipImage, (100, 100))
        self.betImage = pygame.image.load("lock bet button.png")

    def draw(self):
        self.screen.blit(self.deckImage, (self.screenWidth - self.deckImage.get_width() - 30, 30))
        self.screen.blit(self.betImage, (400 - self.betImage.get_width() / 2, 500))
        self.screen.blit(self.standButtonImage,
                         (400 - self.standButtonImage.get_width() / 2, 500 - self.standButtonImage.get_height()))
        self.screen.blit(self.font.render("Player One Money: " + str(self.game.playerMoney), True, (255, 255, 255)),
                         (10, 10))
        self.screen.blit(self.font.render("Player One Bet: " + str(self.game.bet), True, (255, 255, 255)), (10, 40))
        self.screen.blit(self.font.render("Player Two Money: " + str(self.game.playerTwoMoney), True, (255, 255, 255)),
                         (10, 545))
        self.screen.blit(self.font.render("Player Two Bet: " + str(self.game.twoBet), True, (255, 255, 255)), (10, 575))
        self.screen.blit(self.chipImage, (700, 500))
        self.screen.blit(self.font.render("10", True, (255, 255, 255)), (737, 540))
        self.screen.blit(self.chipImage, (700, 400))
        self.screen.blit(self.font.render("25", True, (255, 255, 255)), (737, 440))
        self.screen.blit(self.chipImage, (700, 300))
        self.screen.blit(self.font.render("50", True, (255, 255, 255)), (737, 340))
        self.screen.blit(self.chipImage, (700, 200))
        self.screen.blit(self.font.render("100", True, (255, 255, 255)), (730, 240))
        if self.game.gameStatus == "Ongoing" or self.game.gameStatus == "Start":
            if self.game.activePlayer == 1:
                self.screen.blit(self.font.render("Player One's Turn", True, (255, 255, 255)), (300, 10))
            else:
                self.screen.blit(self.font.render("Player Two's Turn", True, (255, 255, 255)), (300, 10))
        else:
            self.screen.blit(self.font.render("Round End", True, (255, 255, 255)), (300, 10))
        x = 0
        y = 0
        z = 0
        for k in range(len(self.game.playerCardsDrawn)):
            self.screen.blit(self.game.playerCardsDrawn[k].image, (
                self.screenWidth / 4 + (x * self.game.playerCardsDrawn[k].image.get_width() / 2),
                self.screenHeight / 3))
            x += 1
        for j in range(len(self.game.playerTwoCardsDrawn)):
            self.screen.blit(self.game.playerTwoCardsDrawn[j].image, (
                self.screenWidth / 4 + (z * self.game.playerTwoCardsDrawn[j].image.get_width() / 2),
                self.screenHeight / 2))
            z += 1
        for i in range(len(self.game.AICardsDrawn)):
            self.screen.blit(self.game.AICardsDrawn[i].image, (
                self.screenWidth / 4 + (y * self.game.AICardsDrawn[i].image.get_width() / 2),
                self.screenHeight / 6))
            y += 1
        if len(self.game.AICardsDrawn) == 2 and self.game.AIScore != 21 and (
                self.game.gameStatus == "Ongoing" or self.game.gameStatus == "Start"):
            self.screen.blit(self.deckImage, (
                self.screenWidth / 4 + (self.game.AICardsDrawn[0].image.get_width() / 2), self.screenHeight / 6))
        if self.game.gameStatus != "Ongoing" and self.game.gameStatus != "Start":
            self.screen.blit(self.font.render(self.game.gameStatus, True, (255, 255, 255)), (10, 400))

    def checkEvent(self, event):
        if event.type == pygame.KEYDOWN:
            keyPressed = pygame.key.get_pressed()
            if keyPressed[pygame.K_SPACE] and self.game.gameStatus != "Ongoing":
                self.game.resetTurn()
                return
        if self.game.gameStatus != "Ongoing" and self.game.gameStatus != "Start":
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePosX, mousePosY = pygame.mouse.get_pos()
            if (self.screenWidth - self.deckImage.get_width() - 20) < mousePosX < (
                    self.screenWidth - 20) and 30 < mousePosY < 30 + self.deckImage.get_height() and self.game.bet != 0:
                self.game.takeTurn("hit")
            if self.game.gameOverOne:
                if (self.screenWidth - self.deckImage.get_width() - 20) < mousePosX < (
                        self.screenWidth - 20) and 30 < mousePosY < 30 + self.deckImage.get_height() and self.game.twoBet != 0:
                    self.game.takeTurn("hit")
            if 400 - self.standButtonImage.get_width() / 2 < mousePosX < 400 + self.standButtonImage.get_width() / 2 and 500 - self.standButtonImage.get_height() < mousePosY < 500 and self.game.gameStatus == "Ongoing":
                self.game.takeTurn("stand")
            if 400 - self.betImage.get_width() / 2 < mousePosX < 400 + self.betImage.get_width() / 2 and 500 < mousePosY < 500 + self.betImage.get_height() and self.game.gameStatus == "Start" and self.game.canBet:
                if self.game.activePlayer == 1 and self.game.bet != 0 and self.game.canBet:
                    if not self.game.gameOverTwo:
                        self.game.activePlayer = 2
                    else:
                        self.game.canBet = False
                elif self.game.twoBet != 0 and self.game.canBet:
                    if not self.game.gameOverOne:
                        self.game.activePlayer = 1
                    self.game.canBet = False
            if self.game.canBet:
                if 700 < mousePosX < 800 and 500 < mousePosY < 600 and self.game.gameStatus == "Start":
                    if self.game.activePlayer == 1:
                        if self.game.bet + 10 <= self.game.playerMoney:
                            self.game.bet += 10
                    else:
                        if self.game.twoBet + 10 <= self.game.playerTwoMoney:
                            self.game.twoBet += 10
                if 700 < mousePosX < 800 and 400 < mousePosY < 500 and self.game.gameStatus == "Start":
                    if self.game.activePlayer == 1:
                        if self.game.bet + 25 <= self.game.playerMoney:
                            self.game.bet += 25
                    else:
                        if self.game.twoBet + 25 <= self.game.playerTwoMoney:
                            self.game.twoBet += 25
                if 700 < mousePosX < 800 and 300 < mousePosY < 400 and self.game.gameStatus == "Start":
                    if self.game.activePlayer == 1:
                        if self.game.bet + 50 <= self.game.playerMoney:
                            self.game.bet += 50
                    else:
                        if self.game.twoBet + 50 <= self.game.playerTwoMoney:
                            self.game.twoBet += 50
                if 700 < mousePosX < 800 and 200 < mousePosY < 300 and self.game.gameStatus == "Start":
                    if self.game.activePlayer == 1:
                        if self.game.bet + 100 <= self.game.playerMoney:
                            self.game.bet += 100
                    else:
                        if self.game.twoBet + 100 <= self.game.playerTwoMoney:
                            self.game.twoBet += 100


def main():
    pygame.init()
    pygame.display.set_caption("Blackjack")
    screenWidth = 800
    screenHeight = 600
    background = pygame.image.load("background.jpeg")
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    ViewController = viewController(screen, screenWidth, screenHeight)
    font1 = pygame.font.Font(None, 30)
    space_message = font1.render("Press space to clear the table", True, (255, 255, 255))
    dealHitMessage = font1.render("Deal/Hit", True, (255, 255, 255))
    font = pygame.font.Font(None, 30)
    player_message = font.render("Player One", True, (255, 255, 255))
    player_two_message = font.render("Player Two", True, (255, 255, 255))
    dealer_message = font.render("Dealer", True, (255, 255, 255))
    bigFont = pygame.font.Font(None, 64)
    music = pygame.mixer.Sound("music.mp3")
    music.play(-1)
    while True:
        if ViewController.game.gameOverOne and ViewController.game.gameOverTwo:
            screen.fill((0, 0, 0))
            screen.blit(bigFont.render("Game Over", True, (255, 255, 255)), (300, 275))
            screen.blit(bigFont.render("Click to play again", True, (255, 255, 255)), (screenWidth /2 - 150, 400))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    ViewController = viewController(screen, screenWidth, screenHeight)
            continue
        if ViewController.game.hasWonOne:
            screen.fill((0, 0, 0))
            screen.blit(bigFont.render("Player One Wins", True, (255, 255, 255)), (225, 275))
            screen.blit(bigFont.render("Click to play again", True, (255, 255, 255)), (screenWidth / 2 - 150, 400))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    ViewController = viewController(screen, screenWidth, screenHeight)
            continue
        if ViewController.game.hasWonTwo:
            screen.fill((0, 0, 0))
            screen.blit(bigFont.render("Player Two Wins", True, (255, 255, 255)), (225, 275))
            screen.blit(bigFont.render("Click to play again", True, (255, 255, 255)), (screenWidth / 2 - 150, 400))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    ViewController = viewController(screen, screenWidth, screenHeight)
            continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            ViewController.checkEvent(event)
        screen.fill((0, 127, 0))
        screen.blit(background, (0, 0))
        screen.blit(dealHitMessage,
                    (screenWidth - ViewController.deckImage.get_width() - 30,
                     ViewController.deckImage.get_height() + 35))
        screen.blit(space_message, (screen.get_width() / 2 - space_message.get_width() / 2, screen.get_height() - 25,
                                    screenWidth - ViewController.deckImage.get_width() - 30,
                                    ViewController.deckImage.get_height() + 35))
        screen.blit(player_message,
                    (ViewController.deckImage.get_width() / 2, 225))
        screen.blit(player_two_message,
                    (ViewController.deckImage.get_width() / 2, 325))
        screen.blit(dealer_message,
                    (ViewController.deckImage.get_width() / 2, 125))
        if ViewController.game.playerMoney < 0:
            ViewController.game.playerMoney = 0
        if ViewController.game.playerTwoMoney < 0:
            ViewController.game.playerTwoMoney = 0
        ViewController.draw()
        pygame.display.update()


main()
