import game
import importlib
import copy
import random


def randomPop(elements):
    if len(elements) > 0:
        taken = random.choice(elements)
        elements.remove(taken)
        return taken

def makeFeedback(brd, bestOnly = True, validOnly = False, bestPath = True, discountRate = 0.95):
    hsize = 1000000
    feedback_dataset = []
    board_queue = [brd]
    found_boards = [None for n in range(hsize)]
    found_boards[hash(brd) % hsize] = {'board': brd, 'feedback': []}
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
                    elif bestOnly: # me quedo con el mejor?
                        if found_boards[hash_val]['board'].moves < tested_board.moves:
                            feedback['response'] = False
                        else: # no era el mejor
                            found_boards[hash_val]['feedback']['response'] = False
                            found_boards[hash_val]['feedback'] = feedback
                    feedback_dataset.append(feedback)
                elif not validOnly: # keep only valid moves
                    feedback_dataset.append(feedback)

    if bestPath:
        for f in feedback_dataset:
            f['response'] = 0

        for w in winner_boards:
            b = found_boards[w]
            distance = 0
            while len(b['feedback']) > 0:
                #print(b['board'].toHuman())
                b['feedback']['response'] = pow(discountRate,distance)
                prev_board = b['feedback']['board']
                hash_val = hash(prev_board) % hsize
                b = found_boards[hash_val]
                distance += 1
    else:
        for f in feedback_dataset:
            f['response'] = int(f['response'])

    print('hash usage '+ str(sum([h is not None for h in found_boards])/hsize))
    return feedback_dataset

