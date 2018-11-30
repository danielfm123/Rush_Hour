import game
import numpy as np
import copy

import importlib
game = importlib.reload(game)

g = game.Board.fromTxt('samples/txt/1.txt')
b = g.blocks[1]
b.getVector()