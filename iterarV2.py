import game
import importlib
import copy
import random
import fn

fn = importlib.reload(fn)

brd = game.Board.fromTxt('samples/txt/1.txt')

brd.getMoveFeedback(0,1)
brd.getMoveFeedback(0,-1)
brd.moves

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

