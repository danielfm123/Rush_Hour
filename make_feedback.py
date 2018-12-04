import game
import fn
import pandas as pd
import os

txt_path = 'samples/txt/3.txt'

boards = os.listdir(txt_path)

for b in boards:
    brd = game.Board.fromTxt(txt_path + b)
    feedback = []
    for n in range(2):
        print(b)
        print(n)
        aux = fn.makeFeedback(brd)
        feedback = feedback + aux

    with open('feedback/' + b + '.fback','w+') as f:
        for fbak in feedback:
            f.write(','.join([str(x) for x in fbak]) + '\n')