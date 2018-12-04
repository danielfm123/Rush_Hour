import numpy as np
import copy
import random


def randomPop(elements):
    if len(elements) > 0:
        taken = random.choice(elements)
        elements.remove(taken)
        return taken


class Block:

    def __init__(self, x, y, length , horizontal):
        self.horizontal = horizontal
        self.length = length
        self.x = x
        self.y = y

    def move(self,dx,dy):
            self.x = self.x + dx
            self.y = self.y + dy

    def getVector(self,size = 6):
        vector = [0] * size * size
        if self.horizontal:
            for n in range(self.length):
                vector[self.y*size + self.x + n] = 1
        else:
            for n in range(self.length):
                vector[(self.y+n)*size + self.x] = 1
        return [1,int(self.horizontal)] + vector #existence, horizontal, used spaces

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
        self.blocks_number = 0
        self.commited = False

    def fromTxt(file: str):
        game = Board()
        with open(file,'r') as f:
            lineas = f.read().splitlines()
        for l in lineas:
            param = l.split(' ')
            bloque = Block(int(param[0]),int(param[1]),int(param[3]),param[2]=='h')
            game.addBlock(bloque,param[4]=='R')
        game.commitBoard()
        return game

    def __hash__(self):
        return hash(str(self.getBoardVector()))


    def addBlock(self, block:int, is_target=False):
        if self.commited:
            print('Board Commited, cant add blocks')
            return False
        if len(self.blocks) > self.max_blocks:
            exit('More blocks than slots!')
        if is_target:
            self.target_set = True
            self.blocks = [block] + self.blocks
        else:
            self.blocks = self.blocks + [block]
        self.blocks_number += 1
        return True

    def commitBoard(self):
        self.blocks = self.blocks + [None for x in range(len(self.blocks), self.max_blocks)]

    def isBlockInside(self,block_num):
        block = self.blocks[block_num]
        if block is None:
            return True
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
                if block is not None:
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
                if block is not None:
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

    def moveBlock(self,block_number, dx, dy, testOnly = False,force = False):
        if testOnly:
            return copy.deepcopy().moveBlock(block_number,dx,dy,False)
        block = self.blocks[block_number]
        if block is None:
            return False
        if (block.horizontal and dy != 0) or (not block.horizontal and dx != 0 ):
            return False
        block.move(dx, dy)
        if self.isValid():
            self.moves = self.moves + 1
            return True
        elif not force:
            block.move(-dx, -dy)
            return False

    def didWin(self):
        if self.blocks[0].x == 4 and self.target_set:
            return True
        else:
            return False

    def getBoardVector(self):
        vector = []
        for b in self.blocks:
            if b is not None:
                vector = vector + b.getVector()
            else:
                vector = vector + [0,0] + [0]*self.size*self.size
        return vector

    def getMoveResponse(self, block_number, dx, dy):
        board_vec = self.getBoardVector()
        board = copy.deepcopy(self)
        movement = [0,0] * self.max_blocks
        movement[2 * block_number] = dx
        movement[2 * block_number + 1] = dy
        response = self.moveBlock(block_number, dx,dy)
        return {'response':response, 'board_vec': board_vec, 'board' : board,  'movement': movement}

    def makeAllMoves(self):
        for b in range(len(self.blocks)):
            block = self.blocks[b]
            if block is not None:
                if block.horizontal:
                    for p in [(-1, 0), (1, 0)]:
                        yield b, p
                else:
                    for p in [(0, -1), (0, 1)]:
                        yield b, p

    def shuffle(self):
        rojo = self.blocks[0]
        resto = self.blocks[1:]
        random.shuffle(resto)
        self.blocks = [rojo] + resto

    def makeFeedback(self, bestOnly=True, validOnly=False, bestPath=True, discountRate=0.95):
        hsize = 1000000
        feedback_dataset = []
        board_queue = [self]
        found_boards = [None for n in range(hsize)]
        found_boards[hash(self) % hsize] = {'board': self, 'feedback': []}
        winner_boards = []

        while len(board_queue) > 0:
            # print(len(board_queue), len(feedback))
            current_board = randomPop(board_queue)
            if current_board.didWin():
                print('won!')
                winner_boards.append(hash(current_board) % hsize)
            else:
                for b, p in current_board.makeAllMoves():
                    tested_board = copy.deepcopy(current_board)
                    feedback = tested_board.getMoveResponse(b, p[0], p[1])
                    if feedback['response']:
                        hash_val = hash(tested_board) % hsize
                        if found_boards[hash_val] is None:
                            board_queue.append(tested_board)
                            found_boards[hash_val] = {'board': tested_board, 'feedback': feedback}
                        elif bestOnly:  # me quedo con el mejor?
                            if found_boards[hash_val]['board'].moves < tested_board.moves:
                                feedback['response'] = False
                            else:  # no era el mejor
                                found_boards[hash_val]['feedback']['response'] = False
                                found_boards[hash_val]['feedback'] = feedback
                        feedback_dataset.append(feedback)
                    elif not validOnly:  # keep only valid moves
                        feedback_dataset.append(feedback)

        if bestPath:
            for f in feedback_dataset:
                f['response'] = -1

            for w in winner_boards:
                b = found_boards[w]
                distance = 0
                while len(b['feedback']) > 0:
                    # print(b['board'].toHuman())
                    b['feedback']['response'] = pow(discountRate, distance)
                    prev_board = b['feedback']['board']
                    hash_val = hash(prev_board) % hsize
                    b = found_boards[hash_val]
                    distance += 1
        else:
            for f in feedback_dataset:
                f['response'] = 1 if ['response'] else -1

        print('hash usage ' + str(sum([h is not None for h in found_boards]) / hsize))
        return feedback_dataset


