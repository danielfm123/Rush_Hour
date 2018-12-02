import game
import importlib
import copy
import random


def randomPop(elements):
    if len(elements) > 0:
        taken = random.choice(elements)
        elements.remove(taken)
        return taken

def makeFeedback(brd):
    hsize = 1000000
    feedback = []
    board_queue = [brd]
    found_boards = [None for n in range(hsize)]

    while len(board_queue) > 0:
        # print(len(board_queue), len(feedback))
        current_board = randomPop(board_queue)
        if current_board.didWin():
            print('won!')
            #pass
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

    print('hash usage '+ str(sum([h is not None for h in found_boards])/hsize))
    return  feedback