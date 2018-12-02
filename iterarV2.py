import game
import importlib
import copy
import random
import fn

game = importlib.reload(game)

brd = game.Board.fromTxt('samples/txt/1.txt')

hsize = 1000000
feedback = []
board_queue = [brd]
found_boards = [None for n in range(hsize)]

while len(board_queue) > 0:
    #print(len(board_queue), len(feedback))
    current_board =fn.randomPop(board_queue)
    if current_board.didWin():
        print('won!')
    else:
        for b, p in current_board.makeAllMoves():
            test_board = copy.deepcopy(current_board)
            pre_feedback = test_board.getMoveFeedback(b, p)
            if pre_feedback[0]:
                hash_val = hash(test_board) % hsize
                if found_boards[hash_val] is None:
                    board_queue.append(test_board)
                    found_boards[hash_val] = test_board
                else:
                    pre_feedback[0] = False
            feedback.append(pre_feedback)

a = fn.makeFeedback(brd)

#validaciones
valid_boards = []
for b in found_boards:
    if b is not None:
        valid_boards.append(b)

b = random.choice(valid_boards)
vec = b.getBoardVector()
print(sum([x.getBoardVector() == vec for x in valid_boards]))

#uso del hash
sum([h is not None for h in found_boards])/hsize


print(len(feedback))

