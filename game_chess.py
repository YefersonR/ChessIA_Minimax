import pygame
import os.path
import random
from copy import deepcopy
from define import *
from pieces import *
from tools import *
from AI import *


class Board():
    def __init__(self, screen):
        self.screen = screen
        self.color = BLUE      
        
    def draw_board(self, C):
        for y in range(8):
            for x in range(8):
                if (x + y) % 2 == 0:
                    self.color = WHITE_BOARD
                else:
                    self.color = BLUE_BOARD
                pygame.draw.rect(
                    self.screen, self.color,
                    (PIECE_SIZE*(x), PIECE_SIZE*(y), PIECE_SIZE, PIECE_SIZE))


class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Chess game')
        icon = pygame.image.load('./img/chessicono.ico')
        pygame.display.set_icon(icon)
        board = Board(self.screen)
        pieces = Pieces(self.screen)
        cmate = -1
        cmate = self.Game_player_vs_AI_Minimax(board, pieces)
        self.Game_Over(board, pieces, cmate)
                
        pygame.quit()


    def Game_player_vs_AI_Minimax(self, board, pieces):

        cplayer = ['w', 'b']
        player, cl, st, cmate = 0, -1, [], -1
        last_pos = ()
        AI = AI_Minimax(pieces.ar, pieces)
        running = True
        
        print("Te toca!!!!!!!!!!!")
        while running:

            pos_clicked = ()
           
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == MOUSEBUTTONDOWN:
                    if player == 0 and pygame.mouse.get_pressed()[0]:
                        pos_clicked = rev_rect(pygame.mouse.get_pos())
                        pos_clicked = (pos_clicked[0]+1,pos_clicked[1]+1)
                        cl += 1
                        if not pieces.precond(pos_clicked, player) and cl == 0:
                            cl -= 1
                            continue
            if player == 0:
                if pos_clicked != () and not check_valid(pos_clicked[0]-1, pos_clicked[1]-1):
                    cl -= 1
                    continue
                if pos_clicked != () and cl == 0:
                    pieces.selecting(pos_clicked)
                    st.append(pos_clicked)
                    
                if pos_clicked != () and cl == 1:
                    if eq(st[0], pos_clicked):
                        cl -= 1
                        continue
                    if pieces.switch_piece(st[0], pos_clicked):
                        cl, st = -1, []
                        clean_selected(pieces.ar)
                        continue
                    if not pieces.move(pieces.ar, st[0], pos_clicked):
                        cl -= 1
                        continue
                    last_pos = (st[0], pos_clicked)
                    player, cl, st = 1 - player, -1, []
                    if pieces.is_checked(pieces.ar, cplayer[player]): 
                        if pieces.is_checkmate(pieces.ar, cplayer[player]):
                            cmate = 1-player
                            running = False
            else: 
                print("Esperando respuesta de la IA")
                pos = AI.minimax(pieces.ar,pieces,'b',-1000000000,1000000000,3,None,pieces.prev_move)
                if pos[1] == None:
                    pieces.move(pieces.ar, p_random[0], p_random[1])
                else:
                    pieces.selecting(pos[1])
                    pieces.move(pieces.ar, pos[1], pos[2])
                    
                    print_ar(pieces.ar)
                    
                    last_pos = (pos[1], pos[2])
                    player = 1 - player

                    if pieces.is_checked(pieces.ar, cplayer[player]):
                        if pieces.is_checkmate(pieces.ar, cplayer[player]):
                            cmate = 1-player
                            running = False

            board.draw_board(player)
            pieces.draw_pieces_upgrade(last_pos)

            pygame.display.flip()
            self.clock.tick(20)
            
     

        return cmate

    def Game_Over(self, board, pieces, cmate):
        if cmate == -1:
            txt = ""
        if cmate == 2:
            txt = "Empate ♟♟"
        else:
            if cmate == 0:
                txt = "Has ganado!🎊🎊🎊"       
            else:
                txt = "La IA ha ganado! 😂👉" 
                
        print(txt)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            pieces.draw_pieces()

            pygame.display.flip()
            self.clock.tick(20)



if __name__ == '__main__':
    t = Game()
