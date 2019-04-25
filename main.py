import pygame
import time
import random
pygame.init()
pygame.display.set_caption("Cellular Awesomeness")
screen = pygame.display.set_mode((1100,1100))


def randomColor():
    return (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))

class ConwaysRules():
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

    def states(self):
        return self.states

    def startState(self):
        return random.choice(self.states)

    def clearState(self):
        return "Dead"

    def leftMouseState(self):
        return "Alive"
    def rightMouseState(self):
        return "Dead"

class ColorfulConway(ConwaysRules):
    def getColor(self, state):
        return self.colors[state] if state == "Dead" else randomColor()

class ForestFire(ConwaysRules):
    def __init__(self):
        self.colors = { "Tree": (50,255,50), "Dead": (0,0,0), "Burning": (255,0,0)}
        self.states = ["Tree", "Dead", "Burning"]
    def run(self, cell, neighborhood):
        del neighborhood[4] #I don't count
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

    def leftMouseState(self):
        return "Burning"

##class WindyForestFire(ForestFire):
##    def run(self, cell, neighborhood):
##        del neighborhood[8]
##        del neighborhood[7]
##        del neighborhood[6]
##        del neighborhood[5]
##        del neighborhood[4] #I don't count
##        return super(WindyForestFire, self).run(cell, neighborhood)

class Cell:
    def __init__(self, location, rule):
        self.location = location
        self.coords = (10+location[0]*10, 10+location[1]*10)
        self.surface = pygame.Surface((10,10))
        self.debug = False
        self.rule = rule
        
        self.state = self.rule.startState()
        self.surface.fill(self.rule.getColor(self.state))

    def render(self, screen):
        self.surface.fill(self.rule.getColor(self.state))
        screen.blit(self.surface, self.coords)

    def update(self, neighborhood):
        self.state = self.rule.run(self, neighborhood)

    def __str__(self):
        return "location: "+ str(self.location) + "   state: " + str(self.state)
    
    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state
    
    def getLocation(self):
        return self.location

    def setDebug(self, status):
        self.debug = status

class Grid:
    def __init__(self, size, rule):
        self.cells = []
        self.width = size[0]
        self.height = size[1]
        self.rule = rule
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.cells.append( Cell( (x, y), rule ) )
        self.saveNeighborhood()

    def update(self):
        self.saveNeighborhood()
        for cell in self.cells:
            neighbors = []
            for neighbor in self.getNeighborhood(cell.getLocation()):
                neighbors.append(self.getOldState(neighbor))
            cell.update(neighbors)

    def saveNeighborhood(self):
        self.oldStates = []
        for cell in self.cells:
            self.oldStates.append(cell.getState())

    def render(self, screen):
        for cell in self.cells:
            cell.render(screen)

    def getCell(self, location):
        return self.cells[location[1]+(location[0]*self.height)]

    def getRule(self):
        return self.rule

    def getOldState(self, location):
        return self.oldStates[location[1]+(location[0]*self.height)]

    def clear(self):
        for cell in self.cells:
            cell.setState(self.rule.clearState())

    def seed(self):
        for cell in self.cells:
            cell.setState(self.rule.startState())

    def getNeighborhood(self, location):
        right = 0 if location[0] == self.width-1 else location[0]+1
        bottom = 0 if location[1] == self.height-1 else location[1]+1
        left = self.width-1 if location[0] == 0 else location[0]-1
        top = self.height-1 if location[1] == 0 else location[1]-1
        return [
            (left, top),                   (location[0], top),               (right, top),
            (left, location[1]),    (location[0], location[1]), (right, location[1]),
            (left, bottom),           (location[0], bottom),        (right, bottom) ]


grid = Grid( (100,100), ConwaysRules())
done = False
speed = 0.05
lastUpdate = time.time()

tick = False
paused = False

grid.render(screen)
while not done:
    now = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
            done = True
        if pygame.key.get_pressed()[pygame.K_1]:
            grid = Grid( (100,100), ConwaysRules())
        if pygame.key.get_pressed()[pygame.K_2]:
            grid = Grid( (100,100), ColorfulConway())
        if pygame.key.get_pressed()[pygame.K_3]:
            grid = Grid( (100,100), ForestFire())
        if pygame.key.get_pressed()[pygame.K_4]:
            grid = Grid( (100,100), WindyForestFire())
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            paused = not paused
        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            grid.clear()
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            tick = True
        if pygame.key.get_pressed()[pygame.K_RSHIFT]:
            grid.seed()
        if pygame.mouse.get_pressed()[0]:
            coords = pygame.mouse.get_pos()
            gridLocation = (int((coords[0]-10)/10), int((coords[1]-10)/10))
            grid.getCell(gridLocation).setState(grid.getRule().leftMouseState())
        if pygame.mouse.get_pressed()[2]:
            coords = pygame.mouse.get_pos()
            gridLocation = (int((coords[0]-10)/10), int((coords[1]-10)/10))
            grid.getCell(gridLocation).setState(grid.getRule().rightMouseState())
    
    if now - lastUpdate  > speed and not paused:
        grid.update()
        lastUpdate = time.time()
    if paused and tick:
        grid.update()
        tick = False

    grid.render(screen)
    pygame.display.flip()


pygame.display.quit()
