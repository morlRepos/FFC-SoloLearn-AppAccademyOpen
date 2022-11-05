#need more values to get accurate categorical data.
#at least with randomized values.

"""two players to play against each other (the players are actually functions)
the number of games to play in the match
an optional argument to see a log of each game. Set it to True to see these messages.
play(player1, player2, num_games[, verbose])"""
#https://machinelearningmastery.com/make-predictions-scikit-learn/
#I need scikillearn categorial prediction though.
#https://analyticsindiamag.com/complete-guide-to-handling-categorical-data-using-scikit-learn/

import numpy as np
import pandas as pd
import random

from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_blobs
from datetime import datetime

class Player():
    def __init__(self, myDraws=["R","P","S"], smart=False):
        self._smart = smart
        self._best_response = {"R": "P","P": "S", "S": "R"}
        self._my_choices = myDraws
        self._my_moves = []
        self._opponent_moves = []
        self._winCount = 0
        self._looseCount = 0
        self._drawCount = 0

    def __str__(self):
        return "Win:{0} , Loose:{1}, Draw:{2}".format(self._winCount,self._looseCount,self._drawCount)

    def chooseRPC(self):
        if(len(self._opponent_moves) != 0) and self._smart:
            #X, y = make_blobs(n_samples=len(self._opponent_moves), 
            #    centers=3, n_features=1, random_state=0)
            #print(X,y)
            #model = LogisticRegression()
            #model.fit(X, y)
            
            model = LogisticRegression()
            #print(np.array((self._opponent_moves)).reshape(-1, 1))
            #print(np.array((self._opponent_moves)).reshape(1, -1))

            #adding win draw lose [,*] to values
            #print(np.array(self._opponent_moves)[:,0])#rps ords.
            #print(np.array(self._opponent_moves)[:,1])#Win,lose,Draw results.

            #ValueError: This solver needs samples of at least 2 classes in the data, but the data contains only one class: 82
            y = np.array((self._opponent_moves))[:,0]
            #y = [ord('P'),ord('R'),ord('S')]
            #shows Rock Paper Scissor calls in charcode.
            #print(y)
            #show unique RPC selections, has all 3 or not.
            #print(len(set(y)))
            #shows the dated column.
            #print(  (np.array((self._opponent_moves))[:,2]).reshape(-1, 1) )
            if (len(set(y)) != 1):
                model.fit(
                #np.array((self._opponent_moves)).reshape(-1, 1),
                #np.array((self._opponent_moves)).reshape(1, -1)
                ##(np.array((self._opponent_moves))),
                ##using date.
                (np.array((self._opponent_moves))[:,2]).reshape(-1, 1),#single feature
                (np.array(self._opponent_moves)[:,0])
                )
                #can I get it to guess here withtout enter a value..
                Xnew = [[datetime.today().microsecond]]
        
                #print(np.array((self._opponent_moves))[:,2])
                Ynew = model.predict(Xnew)
                debugPredictions = False
                if debugPredictions:
                    print(Ynew) #based on time expects this value from dumb randomizer
                ynew = model.predict_proba(Xnew)
                debugProbabilityValues = False
                if debugProbabilityValues:
                    print(ynew) #what are the chances
                return self._best_response[chr(Ynew[0])]

            else:
                getBest = chr(set(y).pop())
                #print(getBest, self._best_response[getBest])
                return self._best_response[getBest]
        
        else:
            #return "S"
            #return "P"
            #return "R"
            return random.choice(self._my_choices)

    def tallyWinLoose(self, myChoice, yourChoice):
        outcome = ""
        win = 1
        draw = 0
        lose = 2
        if myChoice == yourChoice:
            self._drawCount += 1
            outcome = draw#"Draw"
        elif myChoice == "R": 
            if yourChoice == "S":
                self._winCount += 1
                outcome = win#"Win"
            else:
                self._looseCount += 1
                outcome = lose#"Lose"
        elif myChoice == "P":
            if yourChoice == "R":
                self._winCount += 1
                outcome = win#"Win"
            else:
                self._looseCount += 1
                outcome = lose#"Lose"
        elif myChoice == "S":
            if yourChoice == "P":
                self._winCount += 1
                outcome = win#"Win"
            else:
                self._looseCount += 1
                outcome = lose#"Lose"
        else:
            print(myChoice,yourChoice)
            pass
        dated = datetime.today().microsecond
        self._my_moves.append([ord(myChoice),outcome,dated])
        self._opponent_moves.append([ord(yourChoice),outcome,dated])

def play(p1,p2,n):
    for n in range(n):
        p1_chooses = player1.chooseRPC()
        p2_chooses = player2.chooseRPC()
        
        player1.tallyWinLoose(p1_chooses, p2_chooses)
        player2.tallyWinLoose(p2_chooses, p1_chooses)
    print("Player1 - ",player1)
    print("Player2 - ",player2)
    pass

player1 = Player(smart=True)
player2 = Player(myDraws=["R","R","R","R","R","P","P","S"])

play(player1,player2,100)

#df = pd.read_csv('https://sololearn.com/uploads/files/titanic.csv')
#df['male'] = df['Sex'] == 'male'
#X = df[['Pclass', 'male', 'Age', 'Siblings/Spouses', 'Parents/Children', 'Fare']].values
#print(X)
#y = df['Survived'].values
#print(y)

"""
import pandas as pd
from sklearn.linear_model import LogisticRegression

df = pd.read_csv('https://sololearn.com/uploads/files/titanic.csv')
df['male'] = df['Sex'] == 'male'
X = df[['Pclass', 'male', 'Age', 'Siblings/Spouses', 'Parents/Children', 'Fare']].values
y = df['Survived'].values

model = LogisticRegression()
model.fit(X, y)

print(model.predict([[3, True, 22.0, 1, 0, 7.25]]))
print(model.predict(X[:5]))
print(y[:5])
"""
