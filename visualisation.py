import pygame, random, sys
from pygame.locals import *
from collections import Counter
import game

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

        # pause visualisation (wait for input)
        self.pause()

        # start visualisation
        self.run()

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

    def pause(self):
        """
        pause the visualisation, wait for input
        """
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.exit()
                    return False

    def run(self):
        """
        start the visualisation, which will pause after completing
        """

        # iterate over the moves in the solution
        while len(self.solution) > 0:
            self.check_input()
            self.window.fill((255, 255, 255))
            self.update_vehicles(self.solution.pop(0))
            self.draw_board()
            pygame.display.update()
            pygame.time.wait(150)

        # wait for input to quit
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or event.type == KEYDOWN:
                    self.exit()

    def update_vehicles(self, block_num, dx,dy):

        self.brd.moveBlock(block_num,dx,dy)

    def draw_board(self):
        """
        draw the current vehicles on the window
        """
        print(self.brd.toHuman())

        for v, c in zip(self.vehicles, self.colors):

            # draw horizontally orientated vehicles
            if v is not None:
                if v.horizontal:
                    pygame.draw.rect(self.window, c, (v.x * self.tile, v.y * self.tile, v.length * self.tile, self.tile))
                # draw vertically orientated vehicles
                else:
                    pygame.draw.rect(self.window, c, (v.x * self.tile, v.y * self.tile, self.tile, v.length * self.tile))
