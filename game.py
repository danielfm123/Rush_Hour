import numpy as np

possible_moves = [-1,1]

class Block:

    def __init__(self, x, y, length , horizontal):
        self.horizontal = horizontal
        self.length = length
        self.x = x
        self.y = y

    def move(self,n):
        if(self.horizontal):
            self.x  = self.x + n
        else:
            self.y = self.y + n

    def getVector(self,size = 6):
        vector = [0] * size * size
        if self.horizontal:
            for n in range(self.length):
                vector[self.y*size + self.x + n] = 1
        else:
            for n in range(self.length):
                vector[(self.y+n)*size + self.x] = 1
        return vector

    def makeTarget(x):
        return Block(x,2,2,True)

    def __str__(self):
        return 'x:{} y:{} length:{} horizontal:{}'.format(str(self.x),str(self.y),str(self.length),str(self.horizontal))

class Board:

    def __init__(self,max_blocks = 15):
        self.size = 6
        self.blocks = []
        self.max_blocks = max_blocks
        self.target_set = False
        self.moves = 0

    def fromTxt(file):
        game = Board()
        with open(file,'r') as f:
            lineas = f.read().splitlines()
        for l in lineas:
            param = l.split(' ')
            bloque = Block(int(param[0]),int(param[1]),int(param[3]),param[2]=='h')
            game.addBlock(bloque,param[4]=='R')
        return game

    def __hash__(self):
        return hash(str(self.getBoardVector()))


    def addBlock(self, block, is_target=False):
        if len(self.blocks) > self.max_blocks:
            exit('More blocks than slots!')
        if is_target:
            self.target_set = True
            self.blocks = [block] + self.blocks
        else:
            self.blocks = self.blocks + [block]


    def isBlockInside(self,block_num):
        block = self.blocks[block_num]
        if (block.x >= 0 and block.y >= 0):
            if block.horizontal:
                if (block.x + block.length <= self.size):
                    return True
            else:
                if (block.y + block.length <= self.size):
                    return True
        else:
            return False

    def toMatrix(self):
        try:
            matrix = np.zeros((self.size, self.size))
            for block in self.blocks:
                if block.length > 0:
                    if block.horizontal:
                        for x in range(block.x, block.x + block.length):
                            matrix[block.y, x] = matrix[block.y, x] + 1
                    else:
                        for y in range(block.y, block.y + block.length):
                            matrix[y, block.x] = matrix[y, block.x] + 1
            return matrix
        except:
            return np.matrix([99])

    def toHuman(self):
        if self.isValid():
            matrix = np.zeros((self.size, self.size))
            for n in range(len(self.blocks)):
                block = self.blocks[n]
                if block.length > 0:
                    if block.horizontal:
                        for x in range(block.x, block.x + block.length):
                            matrix[block.y, x] = matrix[block.y, x] + n+1
                    else:
                        for y in range(block.y, block.y + block.length):
                            matrix[y, block.x] = matrix[y, block.x] + n+1
            return matrix
        else:
            return None

    def isValid(self):
        for b in range(len(self.blocks)):
            if not self.isBlockInside(b):
                return False
        if np.max(self.toMatrix()) > 1:
            return False
        return True

    def moveBlock(self,block_number, n):
        block = self.blocks[block_number]
        if block.length == 0:
            return False
        block.move(n)
        if self.isValid():
            self.moves = self.moves + 1
            return True
        else:
            block.move(-n)
            return False

    def didWin(self):
        if self.blocks[0].x == 4 and self.target_set:
            return True
        else:
            return False

    def getBoardVector(self):
        vector = []
        for b in self.blocks:
                vector = vector + b.getVector()
        vector = vector + [0,0,0,0]*(self.max_blocks - len(self.blocks))
        return vector

    def getMoveFeedback(self,block_number,n):
        board = self.getBoardVector()
        movement = [0]*self.max_blocks
        movement[block_number] = n
        feedbabk = self.moveBlock(block_number, n)
        return  [feedbabk] + board + movement

    def makeAllMoves(self):
        for b in range(len(self.blocks)):
            for p in possible_moves:
                yield b, p
                

