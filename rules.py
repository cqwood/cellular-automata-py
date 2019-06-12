import random

from utils import randomColor

class Conways():
    def __init__(self):
        self.colors = { "Alive": (255,255,255), "Dead": (0,0,0) }
        self.states = ["Alive", "Dead"]

    def run(self, cell, neighborhood):
        del neighborhood[4] #I don't count
        liveNeighbors = neighborhood.count("Alive")
        if cell.getState() == "Alive":
            if 1 >= liveNeighbors or liveNeighbors >= 4:
                return "Dead"
        else: # dead
            if liveNeighbors == 3:
                return "Alive"
        return cell.getState()

    def getColor(self, state):
        return self.colors[state]

    def startState(self):
        return random.choice(self.states)

    def clearState(self):
        return "Dead"

    def leftMouseState(self):
        return "Alive"
    def rightMouseState(self):
        return "Dead"

class ColorfulConway(Conways):
    def getColor(self, state):
        return self.colors[state] if state == "Dead" else randomColor()

class ForestFire(Conways):
    def __init__(self):
        self.colors = { "Tree": (50,255,50), "Dead": (0,0,0), "Burning": (255,0,0)}
        self.states = ["Tree", "Dead", "Burning"]

    def run(self, cell, neighborhood):
        neighborhood = self.pruneNeighborhood(neighborhood)
        shouldburn = neighborhood.count("Burning")
        if cell.getState() == "Tree" and shouldburn:
            return "Burning"
        elif cell.getState() == "Tree":
            if random.randrange(0,100001) % 100000 == 0:
                return "Burning"
            else:
                return "Tree"
        elif cell.getState() == "Burning":
            return "Dead"
        elif cell.getState() == "Dead":
            if random.randrange(0,1001) % 100 == 0:
                return "Tree"
            else:
                return "Dead"

    def pruneNeighborhood(self, neighborhood):
        del neighborhood[4] #I don't count
        return neighborhood

    def leftMouseState(self):
        return "Burning"

    def rightMouseState(self):
        return "Tree"

class ForestFireAdvanced(ForestFire):
    def __init__(self):
        self.colors = { "Tree": (50,255,50), "Empty": (0,0,0), "Burning": (255,0,0), "Dead": (100,100,100)}
        self.states = ["Tree", "Dead", "Burning", "Empty"]

    def run(self, cell, neighborhood):
        neighborhood = self.pruneNeighborhood(neighborhood)
        burning = neighborhood.count("Burning")
        shouldburn = (burning and  cell.getState() == "Dead") or burning > 1
        if (cell.getState() == "Tree" or cell.getState() == "Dead") and shouldburn:
            return "Burning"
        elif cell.getState() == "Tree":
            if random.randrange(0,1001) % 1000 == 0 or (neighborhood.count("Tree") + neighborhood.count("Dead")) > 5:
                return "Dead"
            else:
                return "Tree"
        elif cell.getState() == "Burning":
            return "Empty"
        elif cell.getState() == "Empty":
            if random.randrange(0,1001) % 100 == 0:
                return "Tree"
            else:
                return "Empty"
        elif cell.getState() == "Dead":
            if random.randrange(0,100001) % 10000 == 0:
                return "Burning"
            else:
                return "Dead"

class WindyForestFireSouth(ForestFire):
    def pruneNeighborhood(self, neighborhood):
        del neighborhood[8]
        del neighborhood[7]
        del neighborhood[6]
        del neighborhood[5]
        del neighborhood[4]
        return neighborhood

class WindyForestFireEast(ForestFire):
    def pruneNeighborhood(self, neighborhood):
        del neighborhood[4]
        del neighborhood[3]
        del neighborhood[2]
        del neighborhood[1]
        del neighborhood[0]
        return neighborhood