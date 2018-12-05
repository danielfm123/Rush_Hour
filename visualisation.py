import pygame, random, sys
import time

class Visualisation:
    def __init__(self, board, tile=80):
        self.brd = board
        self.blocks = board.blocks
        self.tile = tile
        self.width = (board.size) * self.tile
        self.make_colors()

        # initialize pygame and window
        pygame.init()
        self.window = pygame.display.set_mode((self.width, self.width))
        pygame.display.set_caption('Rush Hour')
        self.window.fill((255, 255, 255))
        self.draw_board()

    def new_board(self,board,sleep = 0.05):
        self.brd = board
        self.blocks = board.blocks
        self.window.fill((255, 255, 255))
        self.draw_board()
        time.sleep(sleep)

    def make_colors(self):
        self.colors = []

        for i in range(len(self.blocks)):
            self.colors.append((130 + int(random.random() * 60), int(random.random() * 256), int(random.random() * 256)))

        # recolor the main vehicle
        self.colors[0] = (255, 0, 0)

    def move_block(self, block_num, dx,dy, force):
        result = self.brd.moveBlock(block_num,dx,dy,force=force)
        if result:
            self.draw_board()
            time.sleep(0.1)
        elif force:
            print('Ilegal Move ' + str(block_num) + ' dx:' + str(dx) + ' dy:' + str(dy))
            #print(self.brd.toHuman())
            self.draw_board()
            time.sleep(0.1)

            self.window.fill((255, 0, 0))
            pygame.display.update()
            time.sleep(0.1)

            self.brd.moveBlock(block_num, -dx, -dy,force=True)
            self.draw_board()
        return result

    def draw_board(self):
        """
        draw the current vehicles on the window
        """
        #print(self.brd.toHuman())
        self.window.fill((255, 255, 255))
        for v, c in zip(self.blocks, self.colors):

            # draw horizontally orientated vehicles
            if v is not None:
                if v.horizontal:
                    pygame.draw.rect(self.window, c, (v.x * self.tile, v.y * self.tile, v.length * self.tile, self.tile))
                # draw vertically orientated vehicles
                else:
                    pygame.draw.rect(self.window, c, (v.x * self.tile, v.y * self.tile, self.tile, v.length * self.tile))
        pygame.display.update()