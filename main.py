import pygame
import time
import rules
import visualization

pygame.init()
pygame.display.set_caption("Cellular Awesomeness")
screen = pygame.display.set_mode((1500,1020))
GRID_SIZE = (100,100)

grid = visualization.Grid( GRID_SIZE, rules.Conways())
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
            grid = visualization.Grid( GRID_SIZE, rules.Conways(), grid)
        if pygame.key.get_pressed()[pygame.K_2]:
            grid = visualization.Grid( GRID_SIZE, rules.ColorfulConway(), grid)
        if pygame.key.get_pressed()[pygame.K_3]:
            grid = visualization.Grid( GRID_SIZE, rules.ForestFire(), grid)
        if pygame.key.get_pressed()[pygame.K_4]:
            grid = visualization.Grid( GRID_SIZE, rules.WindyForestFireSouth(), grid)
        if pygame.key.get_pressed()[pygame.K_5]:
            grid = visualization.Grid( GRID_SIZE, rules.WindyForestFireEast(), grid)
        if pygame.key.get_pressed()[pygame.K_6]:
            grid = visualization.Grid( GRID_SIZE, rules.ForestFireAdvanced(), grid)
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

    screen.fill((0,0,0))
    grid.render(screen)
    pygame.display.flip()


pygame.display.quit()
