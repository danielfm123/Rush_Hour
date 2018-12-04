import game
import importlib
import fn
import pandas as pd
import h2o
import h2o.estimators.deeplearning as dl

fn = importlib.reload(fn)
game = importlib.reload(game)

brd = game.Board.fromTxt('samples/txt/3.txt')
brd.toMatrix()
brd.isValid()
len(brd.blocks)
brd.toHuman()

feedback = fn.makeFeedback(brd, bestOnly=True, validOnly=True, bestPath = True)


len(feedback)
sum([x['response'] > 0 for x in feedback])/len(feedback)

dataset = [ [x['response']] + x['board_vec'] + x['movement'] for x in feedback]

#h2o.init()


#ds = h2o.H2OFrame(feedback,destination_frame='dataset')
#ds = ds.split_frame([0.70,0.20],['train','test','validation'])
#y = 'C1'
#x = ds[0].columns.remove('C1')
#
#fit = dl.H2ODeepLearningEstimator(model_id = 'model',
#                                  epochs = 10,
#                                  hidden = [100,100,30],
#                                  stopping_rounds = 0 )
#fit.train(x=x,y=y,training_frame=ds[0],validation_frame=ds[1])
#fit.auc()
#
#h2o.cluster().shutdown()


