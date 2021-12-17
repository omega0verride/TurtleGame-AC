import turtle
import os
from PIL import Image
from playsound import playsound


def play_sound(file):
    path = os.path.join(os.getcwd(), os.path.normpath(file))
    playsound(path)


class Label(turtle.Turtle):
    def __init__(self, text="Default Text", x=0, y=0, textcolor="white", align="center",
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
    def __init__(self, x=0, y=0):
        super().__init__(shape='circle', visible=True)
        self.shape("coin.gif")
        self.color('red')
        self.penup()
        self.setposition(x, y)
        # do not worry about the part below
        self.coin_img = Image.open("coin.gif")
        self.coin_width = self.coin_img.size[0] / 2
        self.coin_height = self.coin_img.size[1] / 2


class Game:
    def __init__(self, ):
        # Screen setup
        screen = turtle.Screen()
        screen.tracer(0, 0)  # update delay 0 this makes everything the turtle draws appear immediately

        screen.bgcolor('#121212')  # set the color of the background you can use 'red', 'blue'
        # or any hex value https://htmlcolors.com/google-color-picker
        # you can try to set an image as a background if you are curious, but you will have to change the
        # width and height based on that image
        width = 1000
        height = 600
        screen.setup(width, height)  # set the width and height of the window that will be created

        screen.cv._rootwindow.resizable(False, False)  # make the window non-resizable
        screen.listen()  # listen for key presses and other input from the user we will need this later

        # every image that we want to use as a turtle image needs to be added as a shape to the screen
        # it is recommended to use 'gif' format https://ezgif.com/apng-to-gif
        # these files need to be placed in the same folder or in the specified path
        screen.addshape("coin.gif")
        screen.addshape("Files/Images/fox.gif")
        screen.addshape("Files/Images/foxflipped.gif")
        screen.addshape("Files/Images/background.gif")

        # playsound('Files/Audio/coin.mp3')  # how to add sound effects to your game, this will not work on replit
        # but you can try on your device

        # this is an example of how to create a turtle based on the image that you specify (i.e a coin)
        mycoin = turtle.Turtle()
        mycoin.shape("coin.gif")  # we set one of the shapes that we added above, note this image needs to be in the
        # folder you are working
        mycoin.penup()  # we set turtle.penup in order to not see the traces that turtle leaves by default
        mycoin.setposition(150, 100)  # we can move this coin around by using setposition(x, y)

        # as we advance in this project we will use classes, you do not need to know much about them other than they
        # let us use the same code again without having to write it multiple times
        # if we take for example the class specified above it is the same code that we just wrote
        # class Coin(turtle.Turtle):
        #     def __init__(self, x=0, y=0):
        #         super().__init__(shape='circle', visible=True)
        #         self.shape("coin.gif")
        #         self.color('red')
        #         self.penup()
        #         self.setposition(x, y)
        #         # do not worry about the part below
        #         self.coin_img = Image.open("coin.gif")
        #         self.coin_width = self.coin_img.size[0] / 2
        #         self.coin_height = self.coin_img.size[1] / 2

        # using this we can create as many coins as we want without writing the code again.
        c = Coin(200, 10)
        c1 = Coin(125, 50)

        # ---------------- Task 1 ---------------------
        # based on this, your task is to create a Player, something similar to the coin example, you can use
        # any of the solutions we showed. The player is just a turtle with an image of your desire, you can use the
        # included image "Files/Images/fox.gif" for testing
        # later on we will learn how to make the player move
        # ---------------------------------------------

        # Using turtle we can write text to the screen, to do this we use the .write method.
        mylabel = turtle.Turtle()  # create the turtle
        mylabel.hideturtle()  # hide it, we do not need the turtle if we are writing
        mylabel.penup()  # set penup to not leave traces behind
        mylabel.goto(-350, height / 2 - 40)  # set position, you can change this by your desire, this is a
        # demonstration of using variables
        mylabel.color("white")  # set the color of the text
        # set the text, alignment, and font in the specified format
        mylabel.write("a text of my desire", align="center", font=("Courier", 15, "normal"))
        # ---------------- Task 2 ---------------------
        # create some labels for the game like Score: Time: etc. you can use the code explained above or the
        # Class Label created by us. Play around with the code to get familiar with it.
        # the Label class can be used as below
        # Label("text", x, y, textcolor, alignment, font)
        l1 = Label("test")
        l2 = Label("test with pos", x=-200, y=50)
        l3 = Label("test red", x=-200, y=100, textcolor='red')
        l4 = Label("test red italic", x=-200, y=150, textcolor='red', font=("Courier", 20, "italic"))
        # later we will learn how to update the text

        # ---------------- Task 3 ---------------------
        # the final task is drawing a heart shape for the health of the player.
        # You can refer to the links below on how to do this. However, we want the heart shape to match the size of the
        # other objects so make sure it has a reasonable size
        # https://medium.com/analytics-vidhya/draw-heart-with-python-using-turtle-7bd8b9ef31d9
        # https://github.com/ayushi7rawat/Youtube-Projects/blob/master/Heart%20with%20turtle/main.py
        # we will later learn how to make an array of hearts and remove one when the player loses 1 life

        # the screen need to stay updated and reflect the changes that we make, for that reason we use a while loop
        while True:
            screen.update()


if __name__ == "__main__":
    game = Game()
