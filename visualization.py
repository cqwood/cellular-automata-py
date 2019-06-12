import pygame

class Cell:
    def __init__(self, location, rule, cellStart=None):
        self.location = location
        self.coords = (10+location[0]*10, 10+location[1]*10)
        self.surface = pygame.Surface((10,10))
        self.debug = False
        self.rule = rule
        
        self.state = cellStart if cellStart else self.rule.startState()
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
    def __init__(self, size, rule, grid = None):
        self.cells = []
        self.width = size[0]
        self.height = size[1]
        self.rule = rule
        self.surface = pygame.Surface((20+(self.width*10),20+(self.height*10)))
        self.surface.fill((100,100,100))
        self.font = pygame.font.SysFont('helvetica', 30)
        self.counts = {}
        for x in range(0, self.width):
            for y in range(0, self.height):
                possible_state = None
                if grid:
                    possible_state = grid.getCell((x,y)).getState()
                if possible_state in self.rule.states:
                    self.cells.append( Cell( (x, y), rule, possible_state) )
                else:
                    self.cells.append( Cell( (x, y), rule ) )
        self.saveNeighborhood()

    def update(self):
        self.saveNeighborhood()
        self.counts = {}
        for state in self.rule.states:
            self.counts[state] = 0
        for cell in self.cells:
            neighbors = []
            for neighbor in self.getNeighborhood(cell.getLocation()):
                neighbors.append(self.getOldState(neighbor))
            cell.update(neighbors)
            self.counts[cell.getState()] += 1


    def saveNeighborhood(self):
        self.oldStates = []
        for cell in self.cells:
            self.oldStates.append(cell.getState())

    def render(self, screen):
        screen.blit(self.surface, (0,0))
        for cell in self.cells:
            cell.render(screen)
        nameSurface = self.font.render(self.rule.name, True, (255,255,255))
        screen.blit(nameSurface, (1040,40))
        offset = 80
        for state, count in self.counts.items():
            surface = self.font.render(state+' : '+str(count), True, (255,255,255))
            screen.blit(surface, (1040,offset))
            offset += 40

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