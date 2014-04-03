#Tic-Tac-Joe v2.06
#Joe Cowman 2014

import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

PLAYER = 1       #1:X, -1:0
OPPONENT = None    #Same layout as above, set variable as None for a two player game.

START_TURN = 2   #1: Player goes first, 2: Opponent goes first

#Set Colors    R   G   B
BACK_COLOR = (127,127,255)
LINE_COLOR = (255,255,255)
UNACTIVE_COLOR = (200,200,255)
VICTORY_COLOR = (255,0,0)
NOWIN_COLOR = (0,0,0)

LINE_WIDTH = 1
SHAPE_WIDTH = 30

SCREENX = 600
SCREENY = 600

REKT_DIM = (SCREENX/3,SCREENY/3)

#Rect objects for each square of the board
sec1 = Rect((0,0),REKT_DIM)
sec2 = Rect((SCREENX/3,0),REKT_DIM)
sec3 = Rect((SCREENX-(SCREENX/3),0),REKT_DIM)
sec4 = Rect((0,SCREENY/3),REKT_DIM)
sec5 = Rect((SCREENX/3,SCREENY/3),REKT_DIM)
sec6 = Rect((SCREENX-(SCREENX/3),SCREENY/3),REKT_DIM)
sec7 = Rect((0,SCREENY-(SCREENY/3)),REKT_DIM)
sec8 = Rect((SCREENX/3,SCREENY-(SCREENY/3)),REKT_DIM)
sec9 = Rect((SCREENX-(SCREENX/3),SCREENY-(SCREENY/3)),REKT_DIM)

SCREEN = pygame.display.set_mode((SCREENX,SCREENY),0,32)

game_finished = False

#Variables for keeping track of wins
x_wins = 0
o_wins = 0
ties = 0
victor = 0

def draw_board():
    pygame.display.set_caption("Tic-Tac-Joe! Number of X Victories: %i Number of O Victories: %i Number of Ties: %i" % (x_wins,o_wins,ties))
    
    SCREEN.fill(BACK_COLOR)
    
    pygame.draw.line(SCREEN,LINE_COLOR,(SCREENX/3,0),(SCREENX/3,SCREENY),LINE_WIDTH)
    pygame.draw.line(SCREEN,LINE_COLOR,(SCREENX-(SCREENX/3),0),(SCREENX-(SCREENX/3),SCREENY),LINE_WIDTH)
    pygame.draw.line(SCREEN,LINE_COLOR,(0,SCREENY/3),(SCREENX,SCREENY/3),LINE_WIDTH)
    pygame.draw.line(SCREEN,LINE_COLOR,(0,SCREENY-(SCREENY/3)),(SCREENX,SCREENY-(SCREENY/3)),LINE_WIDTH)
    
def draw_cross(section,color,width=SHAPE_WIDTH):
    pygame.draw.line(SCREEN,color,(section[0]+(width/2),section[1]+LINE_WIDTH),(section[0]+((SCREENX/3)-(width/2))-LINE_WIDTH,section[1]+(SCREENY/3)-LINE_WIDTH),width)
    pygame.draw.line(SCREEN,color,(section[0]+((SCREENX/3)-(width/2))-LINE_WIDTH,section[1]+LINE_WIDTH),(section[0]+(width/2),section[1]+(SCREENY/3)-LINE_WIDTH),width)

def draw_circle(section,color,width=SHAPE_WIDTH):
    pygame.draw.circle(SCREEN,color,(section[0]+(section[2]/2),section[1]+(section[3]/2)),(section[2]/2)-LINE_WIDTH)
    pygame.draw.circle(SCREEN,BACK_COLOR,(section[0]+(section[2]/2),section[1]+(section[3]/2)),(section[2]/2)-width) #Draws a smaller circle inside the first

def draw_moves():
    
    for x in xrange(0,len(board)):
        
        if board[x] == 1:
            draw_cross(sec_list[x],LINE_COLOR)
            
        elif board[x] == -1:
            draw_circle(sec_list[x],LINE_COLOR)

def check_win():
    
    global game_finished
    global victor

    for x in xrange(0,len(row_list)):
        
        test_var = board[row_list[x][0]] + board[row_list[x][1]] + board[row_list[x][2]] #used to determine the amount of placed pieces in each row

        if test_var == 3: #X Victory
            
            for y in xrange(0,3):
                draw_cross(sec_list[row_list[x][y]],VICTORY_COLOR)
                game_finished = True
                victor = 1
                
            return
                
        elif test_var == -3: #O Victory
            
            for y in xrange(0,3):
                draw_circle(sec_list[row_list[x][y]],VICTORY_COLOR)
                game_finished = True
                victor = -1
                
            return

    nowin_check = 0

    for x in board:
        
        if x != 0:
            nowin_check += 1

    if nowin_check == 9:    #If every tile in the board is filled and no one has won, it is a tie

        for x in xrange(0,len(sec_list)):

            if board[x] == 1:
                draw_cross(sec_list[x],NOWIN_COLOR)
                
            elif board[x] == -1:
                draw_circle(sec_list[x],NOWIN_COLOR)

        game_finished = True

class AI(object): #The AI will eventually use reasoning to pick a tile, but for now it just selects a random available spot.

    def __init__(self,piece):
        
        self.piece = piece

    def move(self,board):

        piece_chosen = False

        while True: #For now, piece is just placed in a random available tile

            x = randint(0,8)

            if board[x] == 0:
                return x

    def ghost(self,board,row_list):
        pass #TODO: Place a "ghost tile" to determine which moves would cause victory

        ghost_tiles = []

        for x in board:

            if x == 0:

                board[x] = self.piece
                ghost_tiles.append(x)

                for y in row_list:

                    if y[0]+y[1]+y[2] == 3 or y[0]+y[1]+y[2] == -3:

                        move = ghost_tiles[-1]

                        for z in ghost_tiles:

                            board[z] = 0
                            
                            return move

        self.move(board)

if OPPONENT != None: #Set opponent as an AI

    OPPONENT = AI(OPPONENT)

sec_list = [sec1,sec2,sec3,sec4,sec5,sec6,sec7,sec8,sec9]
board = [0,0,0,0,0,0,0,0,0] #Spaces occupied by X will be marked as 1, O will be -1.
row_list = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)] #Each possible winning row/column/diagonal

active_spot = None #Space moused over by player

turn = START_TURN
    
while True:

    for event in pygame.event.get():
        
        if event.type == QUIT:
            exit()

        if event.type == MOUSEBUTTONDOWN:
            
            if game_finished == True: #Reset board
                
                for x in xrange(0,len(board)):
                    board[x] = 0
                    
                game_finished = False
                active_spot = None
                turn = START_TURN

                if victor == 1:
                    x_wins += 1

                elif victor == -1:
                    o_wins += 1

                elif victor == 0:
                    ties += 1

                victor = 0
                
            if active_spot != None and turn == 1: #If player has clicked on an available tile, place the piece
                
                if PLAYER == 1:
                    
                    board[active_spot] = 1
                    turn = 2

                    if OPPONENT == None:
                        PLAYER = -1
                    
                elif PLAYER == -1:
                    
                    board[active_spot] = -1
                    turn = 2

                    if OPPONENT == None:
                        PLAYER = 1


    draw_board()

    draw_moves()

    check_win()

    if OPPONENT != None and turn == 2 and game_finished == False: #If it's the opponent's turn, play a move
        board[OPPONENT.move(board)] = OPPONENT.piece
        
    turn = 1

    coords = pygame.mouse.get_pos()

    if game_finished == False:
        
        for x in xrange(0,len(sec_list)):
            
            if sec_list[x].collidepoint(coords) == 1 and board[x] == 0: #If the player's cursor is over an available tile, draw a shadow of the piece
                
                if PLAYER == 1:
                    draw_cross(sec_list[x],UNACTIVE_COLOR)
                    active_spot = x
                    
                elif PLAYER == -1:
                    draw_circle(sec_list[x],UNACTIVE_COLOR)
                    active_spot = x
                    
            elif sec_list[x].collidepoint(coords) == 1 and board[x] != 0:
                active_spot = None

    pygame.display.update()
