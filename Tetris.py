# -*- coding: utf-8 -*-

'''
Created on Jul 18, 2015

@author: Tim
'''

import pygame
from pygame import *
import random

class Cell:
    color = "#000000"
    filled = False

WIN_WIDTH = 400 #window width
WIN_HEIGHT = 600 # window height
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # in one variable
BACKGROUND_COLOR = "#AAAAAA" #gray background
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 30 #frames per second (pygame thing)
fpsClock = pygame.time.Clock() #clock init. (pygame thing)
grid = [[Cell() for i in range(25)] for j in range(15)] #Basic grid for playing field
fgrid = [[Cell() for i in range(25)] for j in range(15)] #Grid for figure
ftemp = [[Cell() for i in range(25)] for j in range(15)] #Aux. temporary grid for figures turning/moving
f_x = 1 #X location of figure
f_y = 1 #Y location of figure
f_type = ''  #figure type
f_color = '' #figure color (unused)
f_exists = False #does figure exist (if not, create another)
f_down = False  #does figure need to go down
f_left = False  #left
f_right = False #right
f_turn = False #or turn
left = False #is left key pressed
right = False #right
down = False #down
turn = False #space bar for turn
figure_should_lower = False #"time to lower figure" flag
DOWN_SPEED = 1000 #how fast figure goes down. can be changed for higher difficulty 
FIGURES = ["Q", "I", "T", "J", "L", "Z", "S"] #type of figures, randomly selected
    
def empty_grid():
    ''' Emptying the glass.'''
    
    global f_exists
    
    f_exists = False
    print('emptying grid')
    for i in range(0, 10):
        for j in range(0, 20):
            grid[i][j] = False
            fgrid[i][j] = False

def f_can_move_down():
    ''' Checking if figure can move down.'''
    
    #print('f_y= ', f_y)
    for i in range(0, 10):
        for j in range(0, 20):
            if ((fgrid[i][j] == True) and (j > 18)): 
                return False
            if ((fgrid[i][j] == True) and (grid[i][j+1] == True)): 
                return False  
    return True


def f_can_move_right():
    ''' Checking if figure can move right.'''
    
    #print('f_x= ', f_y)
    for i in range(0, 10):
        for j in range(0, 20):
            if ((fgrid[i][j] == True) and (i > 8)):
                return False
            if ((fgrid[i][j] == True) and (grid[i+1][j] == True)): 
                return False
    return True

def f_can_move_left():
    ''' Checking if figure can move left.'''
    
    #print('f_y= ', f_y)
    for i in range(0, 10):
        for j in range(0, 20):
            if ((fgrid[i][j] == True) and (i < 1)):
                return False
            if ((fgrid[i][j] == True) and (grid[i-1][j] == True)): 
                return False
    return True

def f_can_turn_clockwise():
    ''' Checking if we can turn figure (no overlapping with other bricks/walls/etc.'''
    
    if f_type == "Q":
        ''' Squares don't turn.'''
        return True
    
    if f_type == "I":
        ''' Stick has size of four, different from other figures.'''
        ftemp[f_x][f_y] = fgrid[f_x][f_y+3]
        ftemp[f_x+1][f_y] = fgrid[f_x][f_y+2]
        ftemp[f_x+2][f_y] = fgrid[f_x][f_y+1]
        ftemp[f_x+3][f_y] = fgrid[f_x][f_y]
               
        ftemp[f_x][f_y+1] = fgrid[f_x+1][f_y+3]
        ftemp[f_x+1][f_y+1] = fgrid[f_x+1][f_y+2]
        ftemp[f_x+2][f_y+1] = fgrid[f_x+1][f_y+1]
        ftemp[f_x+3][f_y+1] = fgrid[f_x+1][f_y]
               
        ftemp[f_x][f_y+2] = fgrid[f_x+2][f_y+3]
        ftemp[f_x+1][f_y+2] = fgrid[f_x+2][f_y+2]
        ftemp[f_x+2][f_y+2] = fgrid[f_x+2][f_y+1]
        ftemp[f_x+3][f_y+2] = fgrid[f_x+2][f_y]
            
        ftemp[f_x][f_y+3] = fgrid[f_x+3][f_y+3]
        ftemp[f_x+1][f_y+3] = fgrid[f_x+3][f_y+2]
        ftemp[f_x+2][f_y+3] = fgrid[f_x+3][f_y+1]
        ftemp[f_x+3][f_y+3] = fgrid[f_x+3][f_y]
        
        for x in range(0,4):
                for y in range(0,4):
                    if ((ftemp[f_x+x][f_y+y] == True) and (grid[f_x+x][f_y+y] == True)) or ((f_x+x) > 9) or ((f_x+x) < 1) or ((f_y+y)> 19):
                        return False
                        break
                    
    if (f_type != "I") and (f_type != "Q"):
        ''' All other figures (3x3).'''
        ftemp[f_x][f_y] = fgrid[f_x][f_y+2]
        ftemp[f_x+1][f_y] = fgrid[f_x][f_y+1]
        ftemp[f_x+2][f_y] = fgrid[f_x][f_y]
               
        ftemp[f_x][f_y+1] = fgrid[f_x+1][f_y+2]
        ftemp[f_x+1][f_y+1] = fgrid[f_x+1][f_y+1]
        ftemp[f_x+2][f_y+1] = fgrid[f_x+1][f_y]
               
        ftemp[f_x][f_y+2] = fgrid[f_x+2][f_y+2]
        ftemp[f_x+1][f_y+2] = fgrid[f_x+2][f_y+1]
        ftemp[f_x+2][f_y+2] = fgrid[f_x+2][f_y]
        
        for x in range(0,3):
                for y in range(0,3):
                    if ((ftemp[f_x+x][f_y+y] == True) and (grid[f_x+x][f_y+y] == True)) or ((f_x+x) > 9) or ((f_x+x) < 0) or ((f_y+y)> 19):
                        return False
                        break
                     
     
    return True

def move():
    ''' Moving figure (left, right, down or turning clockwise).'''
    
    global left
    global right
    global down
    global turn
    global f_x
    global f_y
    global f_type
    
    can = f_can_move_down()
    if (down) and (can):
        print('Figure Goes Down')#DEBUG LINE
        
        for i in range(0, 10):
            for j in range(0, 20):
                ftemp[i][j] = fgrid[i][j]
        
        for i in range(0, 10):
            for j in range(0, 20):
                fgrid[i][j] = False
        
        for i in range(0, 10):
            for j in range(0, 20):
                if ftemp[i][j] == True:
                    fgrid[i][j+1] = True
            
        f_y += 1
        
    can = f_can_move_right()
    if (right) and (can):
        print('Figure Goes Right')
        
        for i in range(0, 10):
            for j in range(0, 20):
                ftemp[i][j] = fgrid[i][j]
        
        for i in range(0, 10):
            for j in range(0, 20):
                fgrid[i][j] = False
        
        for i in range(0, 10):
            for j in range(0, 20):
                if ftemp[i][j] == True:
                    fgrid[i+1][j] = True
                 
        f_x += 1
        
    can = f_can_move_left()
    if (left) and (can):
        print('Figure Goes Left')
        
        for i in range(0, 10):
            for j in range(0, 20):
                ftemp[i][j] = fgrid[i][j]
        
        for i in range(0, 10):
            for j in range(0, 20):
                fgrid[i][j] = False
        
        for i in range(0, 10):
            for j in range(0, 20):
                if ftemp[i][j] == True:
                    fgrid[i-1][j] = True
               
        
        f_x -= 1    

    can = f_can_turn_clockwise()
    if (turn) and (can):
        
        if f_type == "Q":
            pass
        
        if f_type == "I":
            
            for x in range(0,10):
                for y in range(0,20):
                    ftemp[x][y] = False
            
            for y in range(0,4):
                    print(fgrid[f_x][f_y+y],fgrid[f_x+1][f_y+y],fgrid[f_x+2][f_y+y],fgrid[f_x+3][f_y+y])
                        
            print('Turning stick!')#DEBUG LINE
                             
            ftemp[f_x][f_y] = fgrid[f_x][f_y+3]
            ftemp[f_x+1][f_y] = fgrid[f_x][f_y+2]
            ftemp[f_x+2][f_y] = fgrid[f_x][f_y+1]
            ftemp[f_x+3][f_y] = fgrid[f_x][f_y]
                
            ftemp[f_x][f_y+1] = fgrid[f_x+1][f_y+3]
            ftemp[f_x+1][f_y+1] = fgrid[f_x+1][f_y+2]
            ftemp[f_x+2][f_y+1] = fgrid[f_x+1][f_y+1]
            ftemp[f_x+3][f_y+1] = fgrid[f_x+1][f_y]
                
            ftemp[f_x][f_y+2] = fgrid[f_x+2][f_y+3]
            ftemp[f_x+1][f_y+2] = fgrid[f_x+2][f_y+2]
            ftemp[f_x+2][f_y+2] = fgrid[f_x+2][f_y+1]
            ftemp[f_x+3][f_y+2] = fgrid[f_x+2][f_y]
            
            ftemp[f_x][f_y+3] = fgrid[f_x+3][f_y+3]
            ftemp[f_x+1][f_y+3] = fgrid[f_x+3][f_y+2]
            ftemp[f_x+2][f_y+3] = fgrid[f_x+3][f_y+1]
            ftemp[f_x+3][f_y+3] = fgrid[f_x+3][f_y]
            
                
            for x in range(0,10):
                for y in range(0,20):
                    fgrid[x][y] = False
            
            for x in range(0,4):
                for y in range(0,4):
                    fgrid[f_x+x][f_y+y] = ftemp[f_x+x][f_y+y]
        
        if (f_type != "I") and (f_type != "Q"):
            
            for x in range(0,10):
                for y in range(0,20):
                    ftemp[x][y] = False
            
            for y in range(0,3):
                    print(fgrid[f_x][f_y+y],fgrid[f_x+1][f_y+y],fgrid[f_x+2][f_y+y],fgrid[f_x+3][f_y+y])
                        
            print('Turning other figures (neither stick, nor square)!')#DEBUG LINE
                             
            ftemp[f_x][f_y] = fgrid[f_x][f_y+2]
            ftemp[f_x+1][f_y] = fgrid[f_x][f_y+1]
            ftemp[f_x+2][f_y] = fgrid[f_x][f_y]
                
            ftemp[f_x][f_y+1] = fgrid[f_x+1][f_y+2]
            ftemp[f_x+1][f_y+1] = fgrid[f_x+1][f_y+1]
            ftemp[f_x+2][f_y+1] = fgrid[f_x+1][f_y]
                
            ftemp[f_x][f_y+2] = fgrid[f_x+2][f_y+2]
            ftemp[f_x+1][f_y+2] = fgrid[f_x+2][f_y+1]
            ftemp[f_x+2][f_y+2] = fgrid[f_x+2][f_y]
            
                
            for x in range(0,10):
                for y in range(0,20):
                    fgrid[x][y] = False
            
            for x in range(0,3):
                for y in range(0,3):
                    fgrid[f_x+x][f_y+y] = ftemp[f_x+x][f_y+y]
        
    return True

    
def draw_grid(screen, grid):
    ''' Drawing playing field on screen '''     
    
    for i in range(0, 10):
        for j in range(0, 20):
            if grid[i][j] == True: 
                pygame.draw.rect(screen, WHITE, (i * 25, j * 25, 25, 25))
            if fgrid[i][j] == True: 
                pygame.draw.rect(screen, RED, (i * 25, j * 25, 25, 25))
            if (grid[i][j] == False) and (fgrid[i][j] == False):
                pygame.draw.rect(screen, BLACK, (i * 25, j * 25, 25, 25))

def figure_disappear():
    ''' When figure needs to disappear we do this flush '''    
    
    global f_exists
    
    for i in range(0, 10):
        for j in range(0, 20):
            if fgrid[i][j] == True: 
                grid[i][j] = True
                fgrid[i][j] = False
    f_exists = False
    


            
def create_figure():
    ''' Randombly creating figure '''
    
    global f_x
    global f_y
    global f_exists
    global f_type
        
    f_type = random.choice(FIGURES)
    print('figure = ', f_type) #DEBUG LINE
    
    if (f_type == 'Q'):
        f_exists = True
        f_x = 4
        f_y = 0
    
        fgrid[f_x][f_y] = True
        fgrid[f_x+1][f_y] = True
        fgrid[f_x][f_y+1] = True
        fgrid[f_x+1][f_y+1] = True
    
    if (f_type == 'I'):
        f_exists = True
        f_x = 4
        f_y = 0
    
        fgrid[f_x+1][f_y] = True
        fgrid[f_x+1][f_y+1] = True
        fgrid[f_x+1][f_y+2] = True
        fgrid[f_x+1][f_y+3] = True
    
    if (f_type == 'T'):
        f_exists = True
        f_x = 4
        f_y = 0
    
        fgrid[f_x][f_y] = True
        fgrid[f_x+1][f_y] = True
        fgrid[f_x+2][f_y] = True
        fgrid[f_x+1][f_y+1] = True
        
    if (f_type == 'J'):
        f_exists = True
        f_x = 4
        f_y = 0
    
        fgrid[f_x+1][f_y] = True
        fgrid[f_x+1][f_y+1] = True
        fgrid[f_x+1][f_y+2] = True
        fgrid[f_x][f_y+2] = True

    if (f_type == 'L'):
        f_exists = True
        f_x = 4
        f_y = 0
    
        fgrid[f_x][f_y] = True
        fgrid[f_x][f_y+1] = True
        fgrid[f_x][f_y+2] = True
        fgrid[f_x+1][f_y+2] = True
        
    if (f_type == 'Z'):
        f_exists = True
        f_x = 4
        f_y = 0
    
        fgrid[f_x][f_y] = True
        fgrid[f_x+1][f_y] = True
        fgrid[f_x+1][f_y+1] = True
        fgrid[f_x+2][f_y+1] = True
        
    if (f_type == 'S'):
        f_exists = True
        f_x = 4
        f_y = 0
    
        fgrid[f_x][f_y+1] = True
        fgrid[f_x+1][f_y] = True
        fgrid[f_x+1][f_y+1] = True
        fgrid[f_x+2][f_y] = True
        
    return True
    

def lines_disappear():
    ''' Checking if we have full row and if we do - it disappears '''
    
    for j in range(0, 20):
        for i in range(0, 10):
            
            Line_Filled = True
            
            if (grid[i][j] == False):
                Line_Filled = False
                break
        
        if (Line_Filled == True):
            print('We are removing the line!')
            for k in range(0,j):
                for l in range(0,10):
                    print('we are copying cell', j-k-1, l, grid[l][j-k-1], ' into cell ', j-k, l, grid[l][j-k])
                    grid[l][j-k] = grid[l][j-k-1]         
               
            
            

    
def figure_lowers():
    ''' Figure goes down by itself (on a timer ticks) '''
    
    global f_x
    global f_y
    
    can = f_can_move_down()
    
    if can:    
        
        for i in range(0, 10):
            for j in range(0, 20):
                ftemp[i][j] = fgrid[i][j]
        
        for i in range(0, 10):
            for j in range(0, 20):
                fgrid[i][j] = False
        
        for i in range(0, 10):
            for j in range(0, 20):
                if ftemp[i][j] == True:
                    fgrid[i][j+1] = True
            
        f_y += 1
        return True
    elif (not can):
        print('reached bottom')
        figure_disappear()
        lines_disappear()
            
    
    
    
def main():
    ''' Main game '''
    
    global left
    global right
    global down
    global turn
    global figure_should_lower
    global f_type
    
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption(("Test"))
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Creating view field
    bg.fill(Color(BACKGROUND_COLOR))     # Making it gray
    figure_fall_event = pygame.USEREVENT + 1
    move_ticker = 0
    pygame.time.set_timer(figure_fall_event, DOWN_SPEED)
    empty_grid()

    
    while True: # Main iteration cycle
       # fpsClock.tick(20)
        for e in pygame.event.get(): # Events
            if e.type == QUIT:
                raise SystemExit("QUIT")
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                turn = True
               
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_SPACE:
                turn = False
            if e.type == figure_fall_event:
                figure_lowers()
          
         
        if (not f_exists):
            print('figure not exist, creating...')
            create_figure()
        
        can = f_can_move_down() 
        
        if ((f_y == 0) and (can == False)):
            raise SystemExit("GAME OVER")    
                    
        move_ticker += 1
        if ((left or right or down or turn) and (move_ticker > 3)):
            print('Type issss', f_type)
            print('calling move')
            move()
            move_ticker = 0            
                            
        screen.blit(bg, (0,0))      # Redrawing screen each iteration
        draw_grid(screen, grid)
        pygame.display.update()     # Updating screen
        fpsClock.tick(FPS)    


if __name__ == '__main__':
    main()
