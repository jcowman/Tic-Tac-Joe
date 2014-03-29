#Joe Cowman 2014

import pygame
from pygame.locals import *
from sys import exit
from time import sleep

pygame.init()

PLAYER = "O"

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
        if board[x] == "X":
            draw_cross(sec_list[x],LINE_COLOR)
        elif board[x] == "O":
            draw_circle(sec_list[x],LINE_COLOR)

def check_win():
    
    global game_finished
    
    row_list =[(win_grid[0]+win_grid[1]+win_grid[2]),
               (win_grid[3]+win_grid[4]+win_grid[5]),
               (win_grid[6]+win_grid[7]+win_grid[8]),
               (win_grid[0]+win_grid[3]+win_grid[6]),
               (win_grid[1]+win_grid[4]+win_grid[7]),
               (win_grid[2]+win_grid[5]+win_grid[8]),
               (win_grid[0]+win_grid[4]+win_grid[8]),
               (win_grid[2]+win_grid[4]+win_grid[6])]

    tile_list =[(sec_list[0],sec_list[1],sec_list[2]),
               (sec_list[3],sec_list[4],sec_list[5]),
               (sec_list[6],sec_list[7],sec_list[8]),
               (sec_list[0],sec_list[3],sec_list[6]),
               (sec_list[1],sec_list[4],sec_list[7]),
               (sec_list[2],sec_list[5],sec_list[8]),
               (sec_list[0],sec_list[4],sec_list[8]),
               (sec_list[2],sec_list[4],sec_list[6])]

    for x in xrange(0,len(row_list)):
        if row_list[x] == 3:
            for y in xrange(0,3):
                draw_cross(tile_list[x][y],VICTORY_COLOR)
            game_finished = True
        elif row_list[x] == -3:
            for y in xrange(0,3):
                draw_circle(tile_list[x][y],VICTORY_COLOR)
            game_finished = True

def clear_board():
    for x in board:
        x = None
    for x in win_grid:
        x = 0
    draw_moves()
    pygame.display.update()
    game_finished = False
    active_spot = None
        
board = [None,None,None,None,None,None,None,None,None]
sec_list = [sec1,sec2,sec3,sec4,sec5,sec6,sec7,sec8,sec9]
win_grid = [0,0,0,0,0,0,0,0,0]

active_spot = None
    
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            if game_finished == True:
                exit()
            if active_spot != None:
                if PLAYER == "X":
                    board[active_spot] = "X"
                    win_grid[active_spot] = 1
                    PLAYER = "O"
                elif PLAYER == "O":
                    board[active_spot] = "O"
                    win_grid[active_spot] = -1
                    PLAYER = "X"

    draw_board()

    draw_moves()

    check_win()

    coords = pygame.mouse.get_pos()

    if game_finished == False:
        for x in xrange(0,len(sec_list)):
            if sec_list[x].collidepoint(coords) == 1 and board[x] == None:
                if PLAYER == "X":
                    draw_cross(sec_list[x],UNACTIVE_COLOR)
                    active_spot = x
                elif PLAYER == "O":
                    draw_circle(sec_list[x],UNACTIVE_COLOR)
                    active_spot = x
            elif sec_list[x].collidepoint(coords) == 1 and board[x] != None:
                active_spot = None

    pygame.display.update()
