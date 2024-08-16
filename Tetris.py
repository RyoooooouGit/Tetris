import queue
import threading
import turtle
import keyboard

import Matrix
import Constants

class Tetris:
    def __init__(self):
        self.drawQueue = queue.Queue()
        self.running = True
    
    # listen the key operations all the time and call related methods
    def keyboard_listener(self, event):
        if event.event_type == 'down':
            if event.name == "a":
                self.tetrisMatrix.blockNow.move(Constants.LEFT, self.drawQueue)
            elif event.name == "d":
                self.tetrisMatrix.blockNow.move(Constants.RIGHT, self.drawQueue)
            elif event.name == "w":
                self.tetrisMatrix.blockNow.hardDrop(self.drawQueue)
            elif event.name == "s":
                self.tetrisMatrix.blockNow.softDrop()
            elif event.name == "j":
                self.tetrisMatrix.blockNow.spin(Constants.LEFT_SPIN, self.drawQueue)
            elif event.name == "l":
                self.tetrisMatrix.blockNow.spin(Constants.RIGHT_SPIN, self.drawQueue)
            elif event.name == "k":
                self.tetrisMatrix.hold()
        elif event.event_type == 'up':
            if event.name == "s":
                self.tetrisMatrix.blockNow.resetSoftDrop()
    
    '''
        # ask player to play again
        def checkIfRestart(self):
            result = None
            yOrn = input("Do you want to play again?(y/n) ").upper()
            if yOrn == "N":
                print("Thank you for playing!")
                result = True
            elif yOrn == "Y":
                result = False
            else:
                print("Invalid input!")
                result = self.checkIfRestart()
            return result
    '''
    
    # main method
    def rungame(self):
        # isQuit = False
        # while(not isQuit):
        self.running = True
        self.tetrisMatrix = Matrix.Matrix()
        keyboard.hook(lambda event: self.keyboard_listener(event))
        threading.Thread(target=self.drawingLoop, daemon=True).start()
        self.tetrisMatrix.falling(self.drawQueue)
        # isQuit = self.checkIfRestart()
        self.running = False

    # draw whenever receive the queue signal
    def drawingLoop(self):
        while self.running:
            try:
                self.drawQueue.get(timeout=1)  # Wait for update signal
                self.drawAll()
            except queue.Empty:
                pass

    # draw single square, the left up point of the square is [x, y]
    def drawSquare(self, x, y, color):
        turtle.penup()
        turtle.goto(x, y)
        turtle.pendown()
        turtle.begin_fill()
        turtle.fillcolor(color)
        for _ in range(4):
            turtle.forward(Constants.CELL_SIZE)
            turtle.right(90)
        turtle.end_fill()

    # draw the main game area with wall and blocks in it
    def drawMain(self):
        turtle.penup()
        turtle.goto(-Constants.MATRIX_WIDTH * Constants.CELL_SIZE / 2, Constants.MATRIX_HEIGHT * Constants.CELL_SIZE / 2)
        turtle.pendown()
        turtle.forward(10 * Constants.CELL_SIZE)
        matrixForOutput = self.tetrisMatrix.generateOutputMatrix()
        for i in range(Constants.MATRIX_HEIGHT + 2):
            for j in range(Constants.MATRIX_WIDTH + 2):
                x = j * Constants.CELL_SIZE - (Constants.MATRIX_WIDTH + 2) * Constants.CELL_SIZE / 2
                y = (-Constants.MATRIX_HEIGHT + 2 * i) * Constants.CELL_SIZE / 2
                
                if matrixForOutput[i][j] == Constants.WALL:
                    self.drawSquare(x, y, 'black')
                elif matrixForOutput[i][j] == Constants.SHADOW:
                    self.drawSquare(x, y, 'gray')
                elif matrixForOutput[i][j] != Constants.EMPTY:
                    self.drawSquare(x, y, Constants.COLOR[matrixForOutput[i][j]])

    # draw single block with outer square (for hold and next block)
    def drawBlock(self, block, center, word):
        turtle.penup()
        turtle.goto(center[0], center[1] - 4 * Constants.CELL_SIZE)
        turtle.pendown()
        turtle.write(word, align="center", font=("Century Gothic", 10, "normal"))

        turtle.penup()
        turtle.goto(center[0] - 3 * Constants.CELL_SIZE, center[1] + 3 * Constants.CELL_SIZE)
        turtle.pendown()
        for i in range(4):
            turtle.forward(6 * Constants.CELL_SIZE)
            turtle.right(90)
        
        position = [0, 0]
        if block.type == Constants.I_TYPE:
            position = [center[0] - Constants.CELL_SIZE, center[1] + Constants.CELL_SIZE/2]
        elif block.type == Constants.O_TYPE:
            position = [center[0] - Constants.CELL_SIZE, center[1]]
        else:
            position = [center[0] - Constants.CELL_SIZE/2, center[1]]

        for i in range(len(block.shape)):
            self.drawSquare(position[0] + Constants.CELL_SIZE * block.shape[i][0], position[1] + Constants.CELL_SIZE * block.shape[i][1], Constants.COLOR[block.type])

    # draw real-time score
    def drawScore(self):
        turtle.penup()
        turtle.goto((Constants.MATRIX_WIDTH / 2 + 3) * Constants.CELL_SIZE,  (Constants.MATRIX_HEIGHT / 2 - 10) * Constants.CELL_SIZE)
        turtle.pendown()
        turtle.write("SCORE: "+str(self.tetrisMatrix.score), align="left", font=("Century Gothic", 14, "normal"))

    # conbine all the drawings
    def drawAll(self):
        turtle.clear()

        turtle.speed(0)
        turtle.hideturtle()
        turtle.tracer(0)

        self.drawMain()
        if self.tetrisMatrix.holdedBlock:
            center = [-(Constants.MATRIX_WIDTH / 2 + 6) * Constants.CELL_SIZE, (Constants.MATRIX_HEIGHT / 2 - 2) * Constants.CELL_SIZE]
            self.drawBlock(self.tetrisMatrix.holdedBlock, center, "HOLDING")
        center = [(Constants.MATRIX_WIDTH / 2 + 6) * Constants.CELL_SIZE, (Constants.MATRIX_HEIGHT / 2 - 2) * Constants.CELL_SIZE]
        self.drawBlock(self.tetrisMatrix.newBlockList[0], center, "NEXT BLOCK")

        self.drawScore()

        turtle.update()

game = Tetris()
game.rungame()

