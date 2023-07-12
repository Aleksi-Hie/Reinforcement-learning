"""
This assigment is about Markov Decision Process.
It is a 2 dimensional world where the agent is able to move in 4 directions.
And the goal is to maximize the reward.
"""
from functools import reduce
import sys
from termcolor import colored, cprint
def actionInBounds(location, action, rows, columns):
    
        if action == "up" and location[1] == 0:
            return False
        if action == "down" and location[1] == rows-1:
            return False
        if action == "left" and location[0] == 0:
            return False
        if action == "right" and location[0] == columns-1:
            return False
        return True

import random
class Agent:
    world = []
    rows = 0
    columns = 0
    episodeLenght = 0
    def getTile(self, location):
        return self.world[location[1]][location[0]]

    class estTileReward:
        def __init__(self):
            self.reward = 0.4
            self.visits = 0
            self.discount_factor = 0.9
        def update(self, reward):
            self.visits += 1
            self.reward += reward           
        def getReward(self):
            if self.visits == 0:
                return self.reward
            return self.reward/self.visits
        

    def __init__(self, rows, columns):

        self.rows = rows
        self.columns = columns
        for i in range(rows):
            self.world.append([])
            for j in range(columns):
                self.world[i].append(self.estTileReward())

    def getAdjacentTile(self, action, location):
        _loc = location.copy()
        if action == "up":
            _loc[1] -= 1
            return self.getTile(_loc)
        elif action == "down":
            _loc[1] += 1
            return self.getTile(_loc)
        elif action == "left":
            _loc[0] -= 1
            return self.getTile(_loc)
        elif action == "right":
            _loc[0] += 1
            return self.getTile(_loc)

    def findGreedyAction(self, location):
        actions =["up", "down", "left", "right"]
        for action in actions:
            if not actionInBounds(location, action, self.rows, self.columns):
                actions.remove(action)
        values  =[]
        for action in actions:
            values.append([action, self.getAdjacentTile(action, location)])
        #same values
        maxValue = -9999
        greedyActions = []
        for value in values:
            if value[1].getReward() > maxValue:
                maxValue = value[1].getReward()
                greedyActions = [value[0]]
            elif value[1].getReward() == maxValue:
                greedyActions.append(value[0])
        greedyAction = random.choice(greedyActions)
        return greedyAction

    def findExploratoryAction(self, location):
        actions =["up", "down", "left", "right"]
        for action in actions:
            if not actionInBounds(location, action, self.rows, self.columns):
                actions.remove(action)
        values  =  []
        for action in actions:
            values.append([action, self.getAdjacentTile(action, location)])
        expAction = min(values, key = lambda x: x[1].visits)
        return expAction
    

    def get_action(self, state):
        actions = ['greedy', 'exploratory']

        greedy = 0.95
        exploratory = 0.05

        action = random.choices(actions,weights = (greedy, exploratory))
        self.episodeLenght += 1
        if action[0] == 'greedy':
            return self.findGreedyAction(state)
        else:
            return self.findExploratoryAction(state)
        
    
    def update(self, state, action, reward):
        tile = self.getTile(state)
        tile.update(reward)

    def printOptimalPolicy(self):
        for i in range(self.rows):
            print("")
            for j in range(self.columns):
                tile = self.world[i][j]
                #print in 2 decimal places with 0 padding
                print("{:.3f}".format(tile.getReward()), end = " ")

                
class Gridworld:
    rows = 0
    columns = 0
    agent_location = [0,0]
    world = []
    

    def randomTiles(self,trapDensity):
        toFill = self.rows*self.columns
        traps = round(toFill*trapDensity)
        goals = 1
        randomSeq = []
        for i in range(goals):
            randomSeq.append(1)
        
        for i in range(traps):
            randomSeq.append(-1)

        for i in range(toFill-traps-goals):
            randomSeq.append(0)
        random.shuffle(randomSeq)
        while(randomSeq[0] == 1 or randomSeq[0] == -1):
            random.shuffle(randomSeq)
        return randomSeq

    def createWorld(self):
        tiles = self.randomTiles(0.3)
        for i in range(0, self.rows):
            self.world.append([])
            for j in range(0, self.columns):
                tile = tiles.pop(0)
                self.world[i].append(tile)


    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.createWorld()

    def reset(self):
        self.agent_location = [0,0]
        return self.agent_location

    
            
    def step(self, action):
        episodeFinished = False
        actions = ["up", "down", "left", "right"]


        if action == "up":
            self.agent_location[1] -= 1
        elif action == "down":
            self.agent_location[1] += 1
        elif action == "left":
            self.agent_location[0] -= 1
        elif action == "right":
            self.agent_location[0] += 1
        
        currTile = self.world[self.agent_location[1]][self.agent_location[0]]
        if currTile == -1 or currTile == 1:
            episodeFinished = True
        return self.agent_location, currTile, episodeFinished

_x = 5
_y = 5
world = Gridworld(_x,_y)
agent = Agent(_x,_y)


def draw():
    for i in range(_y):
        for j in range(_x):
            if i == world.agent_location[1] and j == world.agent_location[0]:
                print(colored("A", "blue"), end = " ")
            else:
                if world.world[i][j] == 1:
                    print(colored("G", "green"), end = " ")
                elif world.world[i][j] == -1:
                    print(colored("T", "red"), end = " ")
                else:
                    print(world.world[i][j], end = " ")
        print()
initState = world.agent_location
def main():
    draw()
    action = agent.get_action(initState)
    print(action)
    userAction = ""
    episodes = 0
    episodeLenght = 0
    timeReward = -0.04
    state, reward, done = world.step(action)
    while(episodes < 10000):
        if(done):
            state = world.reset()
            action = agent.get_action(state)
            agent.update(state, action, reward + timeReward*(episodeLenght))
            episodes += 1
            episodeLenght = 0
        action = agent.get_action(state)
        state, reward, done = world.step(action)
        agent.update(state, action, reward)
        episodeLenght += 1
    agent.printOptimalPolicy()
    #final graphical solve of the problem
    print("")
    draw()
    print("")
    state = world.reset()
    action = agent.findGreedyAction(state)
    while(True):
        state, reward, done = world.step(action)
        action = agent.findGreedyAction(state)
        draw()
        
        userAction = input("Enter action: ")
        print(action)
        if(done):
            break
main()

    