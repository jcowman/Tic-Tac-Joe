#Joe Cowman 2014

import pygame
from pygame.locals import *
from sys import exit

pygame.init()

PLAYER = "X"

BACK_COLOR = (127,127,255)
LINE_COLOR = (255,255,255)
UNACTIVE_COLOR = (200,200,255)
VICTORY_COLOR = (255,0,0)

SCREENX = 600
SCREENY = 600
LINE_WIDTH = 1
SHAPE_WIDTH = 30

REKT_DIM = (SCREENX/3,SCREENY/3)

sec1 = pygame.Rect((0,0),REKT_DIM)
sec2 = pygame.Rect((SCREENX/3,0),REKT_DIM)
sec3 = pygame.Rect((SCREENX-(SCREENX/3),0),REKT_DIM)
sec4 = pygame.Rect((0,SCREENY/3),REKT_DIM)
sec5 = pygame.Rect((SCREENX/3,SCREENY/3),REKT_DIM)
sec6 = pygame.Rect((SCREENX-(SCREENX/3),SCREENY/3),REKT_DIM)
sec7 = pygame.Rect((0,SCREENY-(SCREENY/3)),REKT_DIM)
sec8 = pygame.Rect((SCREENX/3,SCREENY-(SCREENY/3)),REKT_DIM)
sec9 = pygame.Rect((SCREENX-(SCREENX/3),SCREENY-(SCREENY/3)),REKT_DIM)

SCREEN = pygame.display.set_mode((SCREENX,SCREENY),0,32)

game_finished = False

def draw_board():
    SCREEN.fill(BACK_COLOR)
    
    pygame.draw.line(SCREEN,(LINE_COLOR),(SCREENX/3,0),(SCREENX/3,SCREENY),LINE_WIDTH)
    pygame.draw.line(SCREEN,(LINE_COLOR),(SCREENX-(SCREENX/3),0),(SCREENX-(SCREENX/3),SCREENY),LINE_WIDTH)
    pygame.draw.line(SCREEN,(LINE_COLOR),(0,SCREENY/3),(SCREENX,SCREENY/3),LINE_WIDTH)
    pygame.draw.line(SCREEN,(LINE_COLOR),(0,SCREENY-(SCREENY/3)),(SCREENX,SCREENY-(SCREENY/3)),LINE_WIDTH)
    

def draw_cross(section,color,width=SHAPE_WIDTH):
    pygame.draw.line(SCREEN,color,(section[0]+(width/2),section[1]),(section[0]+((SCREENX/3)-(width/2)),section[1]+(SCREENY/3)),width)
    pygame.draw.line(SCREEN,color,(section[0]+((SCREENX/3)-(width/2)),section[1]),(section[0]+(width/2),section[1]+(SCREENY/3)),width)

def draw_circle(section,color,width=SHAPE_WIDTH):
    pygame.draw.circle(SCREEN,color,(section[0]+(section[2]/2),section[1]+(section[3]/2)),section[2]/2)
    pygame.draw.circle(SCREEN,BACK_COLOR,(section[0]+(section[2]/2),section[1]+(section[3]/2)),(section[2]/2)-width)

def draw_moves():
    
    for x in xrange(0,len(board)):
        
        if board[x] == 1:
            draw_cross(sec_list[x],LINE_COLOR)
            
        elif board[x] == -1:
            draw_circle(sec_list[x],LINE_COLOR)

def check_win():
    
    global game_finished

    row_list = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

    for x in xrange(0,len(row_list)):
        
        test_var = board[row_list[x][0]] + board[row_list[x][1]] + board[row_list[x][2]]

        if test_var == 3:
            
            for y in xrange(0,3):
                draw_cross(sec_list[row_list[x][y]],VICTORY_COLOR)
                game_finished = True
                
        elif test_var == -3:
            
            for y in xrange(0,3):
                draw_circle(sec_list[row_list[x][y]],VICTORY_COLOR)
                game_finished = True

sec_list = [sec1,sec2,sec3,sec4,sec5,sec6,sec7,sec8,sec9]
board = [0,0,0,0,0,0,0,0,0]

active_spot = None
    
while True:

    for event in pygame.event.get():
        
        if event.type == QUIT:
            exit()

        if event.type == MOUSEBUTTONDOWN:
            
            if game_finished == True:
                
                for x in xrange(0,len(board)):
                    board[x] = 0
                    
                game_finished = False
                active_spot = None
                
            if active_spot != None:
                
                if PLAYER == "X":
                    board[active_spot] = 1
                    PLAYER = "O"
                    
                elif PLAYER == "O":
                    board[active_spot] = -1
                    PLAYER = "X"

    draw_board()

    draw_moves()

    check_win()

    coords = pygame.mouse.get_pos()

    if game_finished == False:
        
        for x in xrange(0,len(sec_list)):
            
            if sec_list[x].collidepoint(coords) == 1 and board[x] == 0:
                
                if PLAYER == "X":
                    draw_cross(sec_list[x],UNACTIVE_COLOR)
                    active_spot = x
                    
                elif PLAYER == "O":
                    draw_circle(sec_list[x],UNACTIVE_COLOR)
                    active_spot = x
                    
            elif sec_list[x].collidepoint(coords) == 1 and board[x] != 0:
                active_spot = None

    pygame.display.update()
