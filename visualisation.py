import pygame, random, sys
from pygame.locals import *
from collections import Counter
import game
import time

class Visualisation:
    def __init__(self, root:game.Block, tile=80):
        self.brd = root
        self.vehicles = root.blocks
        self.tile = tile
        self.width = (root.size) * self.tile
        self.make_colors()

        # initialize pygame and window
        pygame.init()
        self.window = pygame.display.set_mode((self.width, self.width))
        pygame.display.set_caption('Rush Hour')
        self.window.fill((255, 255, 255))
        self.draw_board()
        pygame.display.update()


    def check_input(self):
        """
        checks for input which pauses or quits the visualisation
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                self.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.exit()
                self.pause()

    def make_colors(self):
        self.colors = []

        for i in range(len(self.vehicles)):
            self.colors.append((130 + int(random.random() * 60), int(random.random() * 256), int(random.random() * 256)))

        # recolor the main vehicle
        self.colors[0] = (255, 0, 0)


    @staticmethod
    def exit():
        """
        quit the visualisation
        """
        pygame.quit()
        sys.exit()

    def moveBlock(self, block_num, dx,dy):
        result = self.brd.moveBlock(block_num,dx,dy,force=True)
        if result:
            self.draw_board()
        else:
            print('Ilegal Move ' + str(block_num) + ' dx:' + str(dx) + ' dy:' + str(dy))
            #print(self.brd.toHuman())
            self.draw_board()
            time.sleep(0.3)

            self.window.fill((255, 0, 0))
            pygame.display.update()
            time.sleep(0.1)

            self.brd.moveBlock(block_num, -dx, -dy)
            self.draw_board()

    def draw_board(self):
        """
        draw the current vehicles on the window
        """
        print(self.brd.toHuman())
        self.window.fill((255, 255, 255))
        for v, c in zip(self.vehicles, self.colors):

            # draw horizontally orientated vehicles
            if v is not None:
                if v.horizontal:
                    pygame.draw.rect(self.window, c, (v.x * self.tile, v.y * self.tile, v.length * self.tile, self.tile))
                # draw vertically orientated vehicles
                else:
                    pygame.draw.rect(self.window, c, (v.x * self.tile, v.y * self.tile, self.tile, v.length * self.tile))
        pygame.display.update()