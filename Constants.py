# Shapes
T_TYPE = 0
L_TYPE = 1
J_TYPE = 2
O_TYPE = 3
S_TYPE = 4
Z_TYPE = 5
I_TYPE = 6
NAME = ["T", "L", "J", "O", "S", "Z", "I"]
COLOR = ["purple", "orange", "blue", "yellow", "green", "red", "light blue"]

T_SHAPE = [[-1, 0], [0, 0], [1, 0], [0, 1]]
L_SHAPE = [[-1, 0], [0, 0], [1, 0], [1, 1]]
J_SHAPE = [[-1, 0], [0, 0], [1, 0], [-1, 1]]
O_SHAPE = [[0, 0], [1, 0], [0, 1], [1, 1]]
S_SHAPE = [[-1, 0], [0, 0], [0, 1], [1, 1]]
Z_SHAPE = [[-1, 1], [0, 0], [0, 1], [1, 0]]
I_SHAPE = [[-1, 0], [0, 0], [1, 0], [2, 0]]

TYPE_SHAPE_DICT = {
    T_TYPE: T_SHAPE, 
    L_TYPE: L_SHAPE, 
    J_TYPE: J_SHAPE, 
    O_TYPE: O_SHAPE, 
    S_TYPE: S_SHAPE, 
    Z_TYPE: Z_SHAPE, 
    I_TYPE: I_SHAPE
}

# spin
SPIN_DETECT_LIST_JLSTZ = [[[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]],
                          [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]],
                          [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]],
                          [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]],
                          [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]],
                          [[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]],
                          [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]],
                          [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]]]

SPIN_DETECT_LIST_I = [[[0, 0], [2, 0], [-1, 0], [-1, 2], [2, -1]],
                      [[0, 0], [-2, 0], [1, 0], [1, 2], [-2, -1]],
                      [[0, 0], [2, 0], [-1, 0], [2, 1], [-1, -2]],
                      [[0, 0], [-1, 0], [2, 0], [-1, 2], [2, -1]],
                      [[0, 0], [-2, 0], [1, 0], [-2, 1], [1, -1]],
                      [[0, 0], [2, 0], [-1, 0], [2, 1], [-1, -1]],
                      [[0, 0], [1, 0], [-2, 0], [1, 2], [-2, -1]],
                      [[0, 0], [-2, 0], [1, 0], [-2, 1], [1, -2]]]

DIRECTION_ZERO = 0
DIRECTION_R = 1
DIRECTION_TWO = 2
DIRECTION_L = 3

# Timers
GRAVITY = 1
FAST_FALLING = 0.2
SLOW_FALLING = 1
FALLING_TIME_GAP = SLOW_FALLING
HARDDROP_FREEZE_TIME_GAP = 0.3
FREEZE_TIME = 0.7

# init
MATRIX_WIDTH = 10
MATRIX_HEIGHT = 20

LOOP_NUM = 7

ORIGIN_POSITION = [int(MATRIX_WIDTH/2), MATRIX_HEIGHT + 2]

WALL = -1
BLOCK = 1
EMPTY = -2
SHADOW = -3

FULL_LINE = [WALL] + [BLOCK] * MATRIX_WIDTH + [WALL]
EMPTY_LINE = [WALL] + [EMPTY] * MATRIX_WIDTH + [WALL]

# score
CLEAR_SCORE_LIST = [100, 300, 500, 800]

# draw
CELL_SIZE = 20

# interaction
RIGHT_SPIN = 1
LEFT_SPIN = -1

RIGHT = [1, 0]
LEFT = [-1, 0]
DOWN = [0, -1]