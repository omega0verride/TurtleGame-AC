import turtle
import time
from PIL import Image
import os
import getpass
import json
from random import randint
from playsound import playsound
from threading import Thread



# global variables
score = 0
fontsize = 20
timeLimit = 70
startTime = time.time()

img = Image.open("Files/Images/background.gif")
width = img.size[0] + 200
height = img.size[1] + 10
print("w: ", width, " h: ", height, img.size)


def empty_keypress_handler(x=None, y=None):
    pass


def play_sound(file):
    path = os.path.join(os.getcwd(), os.path.normpath(file))
    thread = Thread(target=lambda: playsound(path))
    thread.start()


class Label(turtle.Turtle):
    def __init__(self, text="Default Text", x=0, y=0, textcolor="black", align="center",
                 font=("Courier", 15, "normal")):
        super().__init__()
        self.text = text
        self.x = x
        self.y = y
        self.textcolor = textcolor
        self.align = align
        self.font = font
        self.color(textcolor)
        self.hideturtle()
        self.penup()
        self.goto(self.x, self.y)
        self.write(text, align=self.align, font=self.font)

    def set_text(self, text):
        self.clear()
        self.write(text, align=self.align, font=self.font)

class Coin(turtle.Turtle):
    def __init__(self):
        super().__init__(shape='circle', visible=False)
        self.shape("Files/Images/coin.gif")
        self.color('red')
        self.penup()
        self.showturtle()
        self.coin_img = Image.open("Files/Images/coin.gif")
        self.coin_width = self.coin_img.size[0] / 2
        self.coin_height = self.coin_img.size[1] / 2

class Player(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.step = 20
        self.shape("Files/Images/fox.gif")
        self.penup()
        self.speed(0)
        self.setheading(90)
        self.enable_jump()

        self.playerImg = Image.open("Files/Images/fox.gif")
        self.player_width = self.playerImg.size[0] / 2
        self.player_height = self.playerImg.size[1] / 2

    def move_right(self):
        (x, y) = self.pos()
        if x < width / 2 - 50:
            self.shape("Files/Images/fox.gif")
            self.setx(x + self.step)

    def moveLeft(self):
        (x, y) = self.pos()
        if x > -width / 2 + 40:
            self.shape("Files/Images/foxflipped.gif")
            self.setx(x - self.step)

    def move_up(self):
        if self.ycor() < height / 2:
            self.forward(self.step)

    def move_down(self):
        if self.ycor() > -height / 2 + 160:
            self.backward(self.step)

    def jump_back(self):
        self.backward(100)

    def jump(self, x, y):
        self.forward(100)
        screen.ontimer(self.jump_back, 200)

    def enable_jump(self):
        screen.onclick(self.jump)

    def disable_jump(self):
        screen.onclick(empty_keypress_handler)

    def enable_movement(self):
        screen.onkeypress(self.move_up, "w")
        screen.onkeypress(self.moveLeft, "a")
        screen.onkeypress(self.move_down, "s")
        screen.onkeypress(self.move_right, "d")
        screen.onkeypress(self.move_up, "W")
        screen.onkeypress(self.moveLeft, "A")
        screen.onkeypress(self.move_down, "S")
        screen.onkeypress(self.move_right, "D")

    def disable_movement(self):
        screen.onkeypress(empty_keypress_handler, "w")
        screen.onkeypress(empty_keypress_handler, "a")
        screen.onkeypress(empty_keypress_handler, "s")
        screen.onkeypress(empty_keypress_handler, "d")
        screen.onkeypress(empty_keypress_handler, "W")
        screen.onkeypress(empty_keypress_handler, "A")
        screen.onkeypress(empty_keypress_handler, "S")
        screen.onkeypress(empty_keypress_handler, "D")


class Heart(turtle.Turtle):
    def __init__(self, size, x, y):
        super().__init__(visible=1)
        self.penup()
        self.size = size
        self.x = x
        self.y = y
        self.goto(self.x, self.y)
        self.pensize(1)
        self.color('red', 'red')
        self.begin_fill()
        self.left(140)
        self.forward(111.65 * size)
        self.func()
        self.left(120)
        self.func()
        self.forward(111.65 * size)
        self.hideturtle()
        self.end_fill()

    def func(self):
        for i in range(200):
            self.right(1)
            self.forward(1 * self.size)


class Lives(turtle.Turtle):
    def __init__(self, num_lives, x, y):
        super().__init__(shape='square', visible=0)
        self.size = 0.15
        self.space = 40
        self.x = x - num_lives * self.space
        self.y = y - self.size * 240
        self.numLives = num_lives
        self.constNumLives = num_lives
        self.currentNumLives = self.numLives
        self.hearts = []
        for i in range(self.numLives):
            h = Heart(self.size, self.x + self.space * i, self.y + 0)
            self.hearts.append(h)

    def addManually(self):
        play_sound('Files/Audio/extralife.mp3')
        self.numLives += 1
        self.currentNumLives += 1
        self.hearts.insert(0, Heart(self.size, self.hearts[0].pos()[0] - self.space, self.y + 0))

    def add(self):
        if len(self.hearts):
            self.currentNumLives += 1
            self.hearts.insert(0, Heart(self.size, self.hearts[0].pos()[0] - self.space, self.y + 0))

    def remove(self):
        if len(self.hearts):
            self.hearts[0].clear()
            self.hearts.pop(0)
            self.currentNumLives -= 1

    def animateRemove(self):
        play_sound('Files/Audio/health.mp3')
        for i in range(5):
            screen.ontimer(self.remove, i * 200 + 300)
            screen.ontimer(self.add, i * 200 + 350)
        screen.ontimer(self.remove, 5 * 200 + 400)


class Rules:
    def __init__(self):
        screen.tracer(0, 0)  # update delay 0
        screen.listen()
        labels = []
        screen._bgcolor('#121212')
        labels.append(Label("RULES", 0, height / 2 - 45, textcolor='#BB86FC', font=("Comic Sans MS", fontsize, "bold")))
        labels.append(Label("1. Use W,A,S,D to move around."
                            "\n2. Collect as many coins as possible."
                            "\n3. You can answer a question only once."
                            "\n4. For each correct answer you get +10 points."
                            "\n5. You have 5 lives."
                            "\n6. For each wrong answer you lose 1 life."
                            "\n7. If the time ends or you lose all your lives the game ends."
                            "\n8. If you answer all the questions before the timer you can move "
                            "\n   freely and gather coins with a value of +1."
                            "\n9. For each fact you read you gain 1 life, but they are rare.", 0, height / 2 - 350,
                            textcolor='#CF6679', font=("Comic Sans MS", fontsize, "normal")))
        labels.append(Label("*Press any key to continue", height / 2 + 100, -height / 2 + 20, textcolor='#03DAC6',
                            font=("Comic Sans MS", 13, "normal")))

        self.doubleClicked = 0
        # press any key to continue
        screen.onkeyrelease(self.changeScreen, '')
        # press any mouse button to continue
        screen.onclick(self.changeScreen)
        screen.onclick(self.changeScreen, 2)
        screen.onclick(self.changeScreen, 3)

    def changeScreen(self, x=None, y=None):
        if self.doubleClicked:
            screen.clear()
            global scene
            scene = 2
        self.doubleClicked += 1


class GameMode2():
    def __init__(self):
        self.questionHeight = 200
        self.width = width
        self.height = height + self.questionHeight
        screen.setup(self.width, self.height)
        screen.tracer(0, 0)  # update delay 0
        screen.listen()
        screen.bgcolor('#121212')
        self.startTime = time.time()
        self.timer = Label("Timer: {}".format(timeLimit), 130, self.height / 2 - 30, textcolor='red')
        self.scoreLabel = Label("Score: {}".format(score), -self.width / 2 + 60, self.height / 2 - 30,
                                textcolor='orange')
        self.lives = Lives(5, self.width / 2, self.height / 2)

        self.running = True

        self.currentCoins = 0
        # self.currentQuestionRand=randint(2, 8)
        self.currentQuestionRand = 1

        self.line = turtle.Turtle()
        self.line.pencolor('white')
        self.line.penup()
        self.line.hideturtle()
        self.line.goto(-self.width / 2, -self.height / 2 + self.questionHeight)
        self.line.pendown()
        self.line.forward(self.width)

        self.coin = Coin()

        self.player0 = Player()
        self.moveCoinToRandLocation()
        self.player0.enable_movement()
        self.questions = [
            ["How do you access the first element of an array?", "\n[1] array[]", "\n[2] array[0]", "\n[3] array[1]",
             2],
            ["The action of doing something over and over again, repeating code?", "\n[1] Program", "\n[2] Bug",
             "\n[3] Loop", "\n[4] Code", 3],
            ["A set of instructions that can be performed with or without a computer:", "\n[1] Bug", "\n[2] Debug",
             "\n[3] Loop", "\n[4] Algorithm", 4],
            ["An error, or mistake, that prevents the program from being run correctly:", "\n[1] Bug", "\n[2] Debug",
             "\n[3] Loop", "\n[4] Algorithm", 1],
            ["Finding and fixing errors or mistakes in programs:", "\n[1] Sequencing", "\n[2] Debugging",
             "\n[3] Looping", "\n[4] Decomposing", 2]
        ]

    def moveCoinToRandLocation(self):
        self.coin.goto(randint(-self.width / 2 + 30, self.width / 2 - 30),
                       randint(-self.height / 2 + 25 + self.questionHeight,
                               self.height / 2 - 45 - int(self.coin.coin_height)))
        if self.player0.pos()[0] - self.player0.player_width <= self.coin.pos()[0] + self.coin.coin_width and \
                self.player0.pos()[0] + self.player0.player_width >= self.coin.pos()[
            0] - self.coin.coin_width and \
                self.coin.pos()[1] + self.player0.player_height >= self.player0.pos()[1] >= self.coin.pos()[
            1] - self.player0.player_height:  # make sure the coin does not go to the same location as before
            self.moveCoinToRandLocation()

    def generateQuestion(self):
        play_sound('Files/Audio/coin.wav')
        if len(self.questions):
            self.player0.disable_movement()
            self.player0.disable_jump()
            self.index = randint(0, len(self.questions) - 1)
            q = ''.join(self.questions[self.index][0:len(self.questions[self.index]) - 1])
            print(q)
            self.question = Label(q, 0, -height / 2 - 25, "white")
            self.enable_answers()
        else:
            print("OUT of Questions!")
            global score
            score += 1
            if self.ans == None:
                self.ans = Label("You finished all questions!\nCollect as many coins as you want.", 0, -height / 2,
                                 "gold")
                play_sound('Files/Audio/completed.mp3')

    def endQuestion(self):
        self.question.clear()
        self.ans.clear()
        self.ans = None
        self.ans0.clear()
        self.questions.pop(self.index)
        self.player0.enable_movement()
        self.player0.enable_jump()

    def checkAns(self, choice):
        if choice == self.questions[self.index][-1]:
            self.disable_answers()
            play_sound('Files/Audio/correct.mp3')
            self.ans0 = Label("")
            self.ans = Label("Correct!", 0, -height / 2 - 50, "green")
            global score
            score += 10
            screen.ontimer(self.endQuestion, 1500)
        else:
            self.disable_answers()
            self.ans0 = Label("Wrong!", 0, -height / 2 - 50, "red")
            self.ans = Label(
                "Correct answer: " + self.questions[self.index][self.questions[self.index][-1]].lstrip('\n'), 0,
                -height / 2 - 70, "green")
            self.lives.animateRemove()
            screen.ontimer(self.endQuestion, 2000)

    def enable_answers(self):
        screen.onkeypress(lambda: self.checkAns(1), "1")
        screen.onkeypress(lambda: self.checkAns(2), "2")
        screen.onkeypress(lambda: self.checkAns(3), "3")
        screen.onkeypress(lambda: self.checkAns(4), "4")

    def disable_answers(self):
        screen.onkeypress(empty_keypress_handler, "1")
        screen.onkeypress(empty_keypress_handler, "2")
        screen.onkeypress(empty_keypress_handler, "3")
        screen.onkeypress(empty_keypress_handler, "4")

    def exitPrep(self):
        try:
            self.ans.clear()
        except:
            pass
        try:
            self.ans0.clear()
        except:
            pass
        try:
            self.question.clear()
        except:
            pass
        self.disable_answers()
        self.player0.disable_movement()
        self.player0.disable_jump()

    def changeScene(self):
        global scene
        scene = 5

    def ranOutOfTime(self):
        print("Out of time")
        play_sound("Files/Audio/finish.mp3")
        self.exitPrep()
        self.label = Label("Your Time Is Over!", 0, -height / 2, textcolor="red", font=("Comic Sans MS", 30, "bold"))
        screen.ontimer(self.changeScene, 3000)

    def outOfLives(self):
        print("Out of lives")
        self.exitPrep()
        play_sound("Files/Audio/finish.mp3")
        self.label = Label("You Lost All Your Lives!", 0, -height / 2, textcolor="red",
                           font=("Comic Sans MS", 30, "bold"))
        screen.ontimer(self.changeScene, 3000)

    def update(self):
        self.scoreLabel.set_text("Score: {}".format(score))
        self.currentTimerVal = timeLimit - int(time.time() - self.startTime)
        if self.currentTimerVal >= 0:
            self.timer.set_text("Timer: {}".format(self.currentTimerVal))
        if self.player0.pos()[0] - self.player0.player_width <= self.coin.pos()[0] + self.coin.coin_width and \
                self.player0.pos()[0] + self.player0.player_width >= self.coin.pos()[
            0] - self.coin.coin_width and \
                self.coin.pos()[1] + self.player0.player_height >= self.player0.pos()[1] >= self.coin.pos()[
            1] - self.player0.player_height:
            self.moveCoinToRandLocation()
            self.currentCoins += 1
            if self.currentCoins >= self.currentQuestionRand:
                # self.currentQuestionRand=randint(2, 8)
                self.currentQuestionRand = 1
                self.generateQuestion()
                self.currentCoins = 0
        if self.running:
            if (self.currentTimerVal) <= 0:
                self.running = False
                self.ranOutOfTime()
            if self.lives.currentNumLives <= 0:
                self.running = False
                self.outOfLives()



def Play():
    # Screen setup
    global screen
    screen = turtle.Screen()
    screen.bgcolor('#121212')
    screen.tracer(0, 0)  # update delay 0
    screen.setup(width, height)
    screen.cv._rootwindow.resizable(False, False)
    screen.listen()

    screen.addshape("Files/Images/fox.gif")
    screen.addshape("Files/Images/foxflipped.gif")
    screen.addshape("Files/Images/coin.gif")
    screen.addshape("Files/Images/background.gif")

    # Current game scene
    global scene, game
    scene = 1

    while True:
        try:
            game.update()
        except:
            pass
        screen.update()
        if scene == 1:
            scene = -1
            gameStartTime = time.time()
            game = Rules()
        if scene == 2:
            scene = 0
            screen.clear()
            game = GameMode2()
        if scene == 3:
            scene = 0
            screen.clear()


if __name__ == "__main__":
    Play()
