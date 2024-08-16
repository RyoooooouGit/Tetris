import Block
import copy
import random
import time
import Constants

# methods related to the interaction between blocks and the whole matrix
class Matrix:
    matrix = []
    newBlockList = []
    index = 0
    holdedBlock = None
    blockNow = None
    isGameOver = False
    holdSwitched = False
    score = 0

    def __init__(self):
        self.matrix = self.initEmptyMatrix()
        self.newBlockList = []
        self.generateNewBlock()
        self.generateNewBlock()
        self.isGameOver = False
        self.holdSwitched = False
        self.score = 0
        self.spawn()

    def initEmptyMatrix(self):
        result = []
        result.append([Constants.WALL] * (Constants.MATRIX_WIDTH + 2))
        for i in range(1, Constants.MATRIX_HEIGHT + 4):
            result.append(copy.copy(Constants.EMPTY_LINE))
        return result

    def generateNewBlock(self):
        newBlockList = list(range(Constants.LOOP_NUM))
        random.shuffle(newBlockList)
        for i in range(Constants.LOOP_NUM):
            self.newBlockList.append(Block.Block(newBlockList[i], self))

    # call fall() every second and draw till the game over
    def falling(self, drawQueue):
        self.isGameOver = False
        while not self.isGameOver:
            self.blockNow.fall()
            drawQueue.put('update')
            time.sleep(Constants.FALLING_TIME_GAP)  
        print("Game Over! Your total score is", self.score)  

    # hold one block for player to change the sequence of blocks (only one holding in one falling)
    def hold(self):
        if self.holdSwitched:
            return
        if self.holdedBlock == None:
            self.holdedBlock = Block.Block(self.blockNow.type, self)
            self.spawn()
        else:
            temp = self.holdedBlock
            self.holdedBlock = Block.Block(self.blockNow.type, self)
            self.blockNow = Block.Block(temp.type, self)
        self.holdSwitched = True

    # A block added into the matrix
    def spawn(self):
        self.blockNow = self.newBlockList.pop(0)
        if len(self.newBlockList) == Constants.LOOP_NUM:
            self.generateNewBlock()
        self.holdSwitched = False

    # find full lines and clear
    def lineClear(self):
        numberOfClear = 0
        for i in range(Constants.MATRIX_HEIGHT, 0, -1):
            full = True
            for j in range(1, Constants.MATRIX_WIDTH + 1):
                if self.matrix[i][j] == Constants.EMPTY:
                    full = False
            if full:
                del self.matrix[i]
                self.matrix.append(copy.copy(Constants.EMPTY_LINE))
                numberOfClear += 1
        if numberOfClear != 0:
            self.score += Constants.CLEAR_SCORE_LIST[numberOfClear - 1]
        return numberOfClear != 0

    # add the block into the matrix and can't move anymore
    def freeze(self):
        for i in range(len(self.blockNow.shape)):
            self.matrix[self.blockNow.position[1] + self.blockNow.shape[i][1]][self.blockNow.position[0] + self.blockNow.shape[i][0]] = self.blockNow.type
        lineClear = self.lineClear()
        if (not lineClear) and self.blockNow.isTooTall():
            self.isGameOver = True
        self.blockNow.cancelTimer()
        self.spawn()
        return lineClear

    # add shadow and moving block into matrix and output it
    def generateOutputMatrix(self):
        matrixForOutput = copy.deepcopy(self.matrix)

        shadow = self.blockNow.generateShadow()
        for i in range(len(shadow.shape)):
            matrixForOutput[shadow.position[1] + shadow.shape[i][1]][shadow.position[0] + shadow.shape[i][0]] = Constants.SHADOW
            
        for i in range(len(self.blockNow.shape)):
            matrixForOutput[self.blockNow.position[1] + self.blockNow.shape[i][1]][self.blockNow.position[0] + self.blockNow.shape[i][0]] = self.blockNow.type
     
        return matrixForOutput
