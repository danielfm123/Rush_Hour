import game
import importlib
import copy
import random
game = importlib.reload(game)

def randomPop(elements):
    if(len(elements) > 0):
        taken = random.choice(elements)
        elements.remove(taken)
        return taken

brd = game.Board()
b0 = game.Block(1,1,3,True)
b1 = game.Block(0,0,3,False)
b2 = game.Block(1,1,0,False)
target = game.Block.makeTarget(2)

brd.addBlock(b0)
brd.addBlock(b1)
brd.addBlock(b2)
brd.addBlock(target,is_target=True)

brd.isValid()
brd.toMatrix()
brd.didWin()

hsize = 500000
feedback = []
board_queue = [brd]
found_boards = [None for n in range(hsize)]

while len(board_queue) > 0:
    print(len(board_queue))
    current_board = randomPop(board_queue)
    if current_board.didWin():
        print('won!')
    else:
        for b, p in current_board.makeAllMoves():
            test_board = copy.deepcopy(current_board)
            pre_feedback = test_board.getMoveFeedback(b, p)
            if pre_feedback[0]:
                hash_val = hash(test_board) % hsize
                if found_boards[hash_val] is not None:
                    pre_feedback[0] = False
                else:
                    board_queue.append(test_board)
                    found_boards[hash_val] = test_board
            feedback.append(pre_feedback)


# for b in found_boards:
#    print(sum([x == b for x in found_boards]))


# print(len(feedback))

