from typing import Sequence
import pygame
from pygame.locals import *
from pygame.event import Event
from codesets.colors import SCORE_BLOCK_COLOR
from game_logic.plane import Plane

START_WIDTH = 330
START_HEIGHT = 600
TOP_MARGIN = 100
BOTTOM_MARGIN = 10
START_TICK_DOWN = 1.0
DOWN_PRESSED_TICK_DOWN = 0.05
MAX_CLICK_EVENT_TIME = 0.5

def WIDOW_HEIGHT():
    return START_HEIGHT + TOP_MARGIN + BOTTOM_MARGIN

class Game:
    def __init__(self):
        pygame.init()
        self.__surface : pygame.Surface = pygame.display.set_mode((START_WIDTH, WIDOW_HEIGHT()), RESIZABLE)
        self.__plane: Plane = Plane(self.__surface, START_WIDTH, WIDOW_HEIGHT(), TOP_MARGIN, BOTTOM_MARGIN)
        self.__runnung: bool = False
        self.__tickDown: float = START_TICK_DOWN
        self.__timeLastEvent: float = 0.0
        self.__lastClick: float = 0
        self.__downPressed = False

        self.points = 0

    def run(self):
        self.__runnung: bool = True

        getTicksLastFrame: int = 0
        while self.__runnung:
            ticks: int = pygame.time.get_ticks()
            deltaTime: float = (ticks - getTicksLastFrame) / 1000.0
            getTicksLastFrame = ticks
            self.__timeLastEvent += deltaTime
            self.__lastClick += deltaTime
            for event in pygame.event.get():
                self.__stop(event)
                self.__resize(event)
                self.__keypress(event)
            
            self.__update(deltaTime)
            self.__checkEvent()
            # self.__keyPressed(pygame.key.get_pressed())

    def __getTickDown(self):
        return DOWN_PRESSED_TICK_DOWN if self.__downPressed else self.__tickDown

    def __checkEvent(self):
        if self.__timeLastEvent < self.__getTickDown() or self.__lastClick < MAX_CLICK_EVENT_TIME:
            return
        self.__timeLastEvent = 0
        self.__onEvent()
    
    def __onEvent(self):
        self.__timeLastEvent = 0
        if self.__plane.hasBlock():
            self.__moveDown()
            return

        if self.__downPressed:
            return
        self.__plane.placeBlock()
    
    def __moveDown(self):
        if not self.__plane.moveDown():
            self.points += self.__plane.checkLine()
            self.__onEvent()

    def __stop(self, event: Event):
        if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
            self.__runnung = False

    def __keypress(self, event: Event):
        if event.type == KEYDOWN:
            if event.key == K_LSHIFT:
                self.__plane.rotateLeft()
            if event.key == K_LEFT:
                self.__lastClick = 0
                self.__plane.moveLeft()
            if event.key == K_RIGHT:
                self.__lastClick = 0
                self.__plane.moveRight()
            if event.key == K_DOWN:
                self.__downPressed = True
                self.__moveDown()
            if event.key == K_UP:
                self.__plane.saveBlock()
        if event.type == KEYUP:
            if event.key == K_DOWN:
                self.__downPressed = False
    
    def __update(self, deltaTime: float):
        self.__surface.fill((255, 255, 255))
        self.__plane.render()
        self.__renderScore()
        pygame.display.flip()
    
    def __renderScore(self):
        my_font = pygame.font.SysFont('arial', 20, bold = True)
        text = str(self.points)
        text_surface = my_font.render(text, False, (0, 0, 0))
        text_width, text_height = my_font.size(text)
        leftPivot = self.__plane.getPlaneLeftPivot()
        gamePlaneWidth = self.__plane.getGameWidth()
        pygame.draw.rect(self.__surface, SCORE_BLOCK_COLOR, pygame.Rect(leftPivot.x, 0, gamePlaneWidth, text_height + 6))
        self.__surface.blit(text_surface, (leftPivot.x + gamePlaneWidth / 2 - text_width / 2, 3))

    def _renderNext(self):
        next = self.__plane.nextBlock
        pass

    def __resize(self, event: Event):
        if event.type != VIDEORESIZE:
            return
        width = event.w
        height = event.h
        if width < START_WIDTH:
            width = START_WIDTH
        if height < WIDOW_HEIGHT():
            height = WIDOW_HEIGHT()
        
        self.__surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.__plane.reRenderPlane(width, height)