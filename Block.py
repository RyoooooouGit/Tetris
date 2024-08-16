import Constants
import threading
import copy
import time

# methods related to only one block
class Block:
    type = Constants.T_TYPE
    shape = Constants.T_SHAPE
    position = Constants.ORIGIN_POSITION
    direction = Constants.DIRECTION_ZERO
    matrix = None
    timer = None
    isFall = True

    def __init__(self, type, matrix):
        self.type = type
        self.shape = copy.copy(Constants.TYPE_SHAPE_DICT[type])
        self.position = [Constants.ORIGIN_POSITION[0], Constants.ORIGIN_POSITION[1]]
        self.direction = Constants.DIRECTION_ZERO
        self.matrix = matrix
        self.timer = None

    # spin and check the possible spin position
    def spin(self, direction, drawQueue):
        if self.type == Constants.O_TYPE:
            return
        spinDetectList = None
        newShape = [[0, 0]] * 4
        if self.type == Constants.I_TYPE:
            for i in range(len(self.shape)):
                newShape[i] = [self.shape[i][0] - 0.5, self.shape[i][1] + 0.5]
                newShape[i] = [newShape[i][1] * direction, -newShape[i][0] * direction]
                newShape[i] = [int(newShape[i][0] + 0.5), int(newShape[i][1] - 0.5)]
                spinDetectList = Constants.SPIN_DETECT_LIST_I
        else:
            for i in range(len(self.shape)):
                newShape[i] = [self.shape[i][1] * direction, -self.shape[i][0] * direction]
                spinDetectList = Constants.SPIN_DETECT_LIST_JLSTZ
        spinType = int(2 * self.direction + (direction + 1)/2)
        spinSuccess = False
        for i in range(len(spinDetectList[spinType])):
            spinSuccess = self.canMove(spinDetectList[spinType][i], newShape)
            if spinSuccess:
                self.shape = newShape
                self.direction = (self.direction + direction) % 4
                self.position = [self.position[0] + spinDetectList[spinType][i][0], self.position[1] + spinDetectList[spinType][i][1]]
                drawQueue.put('update')
                break

    # move left or right  
    def move(self, direction, drawQueue):
        if self.canMove(direction, self.shape):
            self.position[0] += direction[0]
            if self.canMove(Constants.DOWN, self.shape):
                self.cancelTimer()
            else:
                self.resetTimer(Constants.FREEZE_TIME)
            drawQueue.put('update')
    
    # fall to the buttom immediately
    def hardDrop(self, drawQueue):
        for i in range(self.position[1] - 1, -1, -1):
            if(not self.canMove([0, i - self.position[1]], self.shape)):
                self.matrix.score += (2 * (self.position[1] - i - 1))
                self.position[1] = i + 1
                drawQueue.put('update')
                self.cancelTimer()
                time.sleep(Constants.HARDDROP_FREEZE_TIME_GAP)
                self.matrix.freeze()
                drawQueue.put('update')     
                break

    # speed up the falling
    def softDrop(self):
        Constants.FALLING_TIME_GAP = Constants.FAST_FALLING

    # slow down the falling
    def resetSoftDrop(self):
        Constants.FALLING_TIME_GAP = Constants.SLOW_FALLING

    # move down one block
    def fall(self):
        if self.canMove(Constants.DOWN, self.shape):
            self.position[1] = self.position[1] - 1
            if Constants.FALLING_TIME_GAP == Constants.FAST_FALLING:
                self.matrix.score += 1
            self.cancelTimer()
            if not self.canMove(Constants.DOWN, self.shape):
                self.startTimer(Constants.FREEZE_TIME)
   
    # check if too tall to game over
    def isTooTall(self):
        result = False
        for i in range(len(self.shape)):
            if self.position[1] + self.shape[i][1] > Constants.MATRIX_HEIGHT:
                result = True
                break
        return result

    # check obstacles
    def canMove(self, direction, shape):
        result = True
        for i in range(len(shape)):
            xToDetect = self.position[0] + shape[i][0] + direction[0]
            yToDetect = self.position[1] + shape[i][1] + direction[1]
            if self.matrix.matrix[yToDetect][xToDetect] > Constants.EMPTY:
                result = False
                break
        return result

    # return the block where self will fall  
    def generateShadow(self):
        result = Block(self.type, self.matrix)
        for i in range(self.position[1] - 1, -1, -1):
            if(not self.canMove([0, i - self.position[1]], self.shape)):
                result.shape = copy.deepcopy(self.shape)
                result.direction = self.direction
                result.position[0] = self.position[0]
                result.position[1] = i + 1
                break
        return result

    # freeze timers
    def startTimer(self, time):
        if not self.timer:
            self.timer = threading.Timer(time, self.matrix.freeze) # It's important to set the Timer to None in the called function
            self.timer.start()

    def resetTimer(self, time):
        self.cancelTimer()
        self.startTimer(time)
            
    def cancelTimer(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None
