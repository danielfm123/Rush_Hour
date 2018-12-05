import game
import importlib
import random
import pandas as pd
import visualisation
import h2o
import h2o.estimators.deeplearning as dl

visualisation = importlib.reload(visualisation)
game = importlib.reload(game)

brd =game.Board()
brd.fromRsh('samples/rsh/Beat It.rsh')
#brd.fromTxt('samples/txt/3.txt')
brd.toMatrix()
brd.isValid()
len(brd.blocks)
brd.toHuman()
#vis = visualisation.Visualisation(brd)
#brd.moveBlock(1,0,-1)
#vis.new_board(brd)

#brd.shuffle()

feedback = brd.makeFeedback(keepBestPrevious=True, keepValidOnly=True, victoryPath= True, discountRate=1, interactive=False)


#len(feedback)
#sum([x['response'] > 0 for x in feedback])/len(feedback)

#dataset = pd.DataFrame([ [x['response']] + x['board_vec'] + x['movement'] for x in feedback])
#dataset

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


