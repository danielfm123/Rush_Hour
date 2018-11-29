import game
import importlib
import copy
game = importlib.reload(game)

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

feedback = []
board_queue = [brd]
previous_boards = []

while len(board_queue) > 0:
    current_board = board_queue.pop()
    previous_boards.append(current_board.getBoardVector())
    print(current_board.toMatrix())
    if current_board.didWin():
        print('won!')
    else:
        for b, p in current_board.makeAllMoves():
            test_board = copy.deepcopy(current_board)
            pre_feedback = test_board.getMoveFeedback(b, p)
            if pre_feedback[0]:
                if test_board.getBoardVector() in previous_boards:
                    print('repeated board')
                    pre_feedback[0] = False
                else:
                    print('new board found')
                    board_queue.append(test_board)
                    previous_boards.append(test_board.getBoardVector())
            else:
                print('ilegal move')
            feedback.append(test_board.getMoveFeedback(b, p))

