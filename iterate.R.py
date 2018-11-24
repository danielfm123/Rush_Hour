import game
import importlib
game = importlib.reload(game)

brd = game.Board()
b0 = game.Block(1,1,3,True)
b1 = game.Block(0,0,3,False)
b2 = game.Block(1,1,0,False)
target = game.Block.makeTarget(2)

blocks = [b0,b1,b2]
brd.addBlock(blocks)
brd.addBlock(target,is_target=True)

feedback = []

