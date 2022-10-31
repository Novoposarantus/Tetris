from __future__ import annotations
from enum import Enum
import random
from typing import Tuple
import pygame.color
from codesets.helpers import first
from codesets.colors import *

class PositionChangeType(Enum):
    CLEAR = 1
    CANT = 2
    STOP = 3

class PositionType(Enum):
    BLOCK = 1
    EMPTY = 2

class Position:
    def __init__(self, x: int, y : int, empty: bool = False):
        self.x: int = x
        self.y: int = y
        self.positionType: PositionType = PositionType.EMPTY if empty else PositionType.BLOCK
    
    def plus(self, position: Position) -> Position:
        self.x += position.x
        self.y += position.y
        return self
    
    def clone(self) -> Position:
        empty: bool = True if self.positionType == PositionType.EMPTY else False
        return Position(self.x, self.y, empty)
    
    def equals(self, position: Position):
        return self.x == position.x and self.y == position.y

class RotationType(Enum):
    LEFT = 1
    TOP = 2
    RIGHT = 3
    BOTOM = 4

class Rotation:
    def __init__(self, positions: list[Position], type: RotationType):
        self.positions: list[Position] = positions
        self.type: RotationType = type

    def getMaxWidthPos(self) -> int:
        return max(map(lambda pos: pos.x, self.positions))

    def getMaxHeightPos(self) -> int:
        return max(map(lambda pos: pos.y, self.positions))

    def getPosition(self, x: int, y: int) -> Position:
        return first(self.positions, lambda p: p.equals(Position(x, y)))

class Rotations:
    def __init__(self, left: list[Position], top: list[Position], right: list[Position], bottom: list[Position]):
        self.left: Rotation = Rotation(left, RotationType.LEFT)
        self.top: Rotation = Rotation(top, RotationType.TOP)
        self.right: Rotation = Rotation(right, RotationType.RIGHT)
        self.bottom: Rotation = Rotation(bottom, RotationType.BOTOM)
    
    def getRandomRotation(self):
        rotationNumber = random.randint(1, 4)
        if rotationNumber == RotationType.LEFT.value:
            return self.left
        if rotationNumber == RotationType.RIGHT.value:
            return self.right
        if rotationNumber == RotationType.TOP.value:
            return self.top
        if rotationNumber == RotationType.BOTOM.value:
            return self.bottom
    
    def getRightRotation(self, currentRotation: Rotation) -> Rotation:
        switcher = {
            RotationType.LEFT: self.top,
            RotationType.TOP: self.right,
            RotationType.RIGHT: self.bottom,
            RotationType.BOTOM: self.left,
        }

        return switcher.get(currentRotation.type)
    
    def getLeftRotation(self, currentRotation: Rotation) -> Rotation:
        switcher = {
            RotationType.LEFT: self.bottom,
            RotationType.BOTOM: self.right,
            RotationType.RIGHT: self.top,
            RotationType.TOP: self.left,
        }

        return switcher.get(currentRotation.type)
        

class Color:
    def __init__(self, red: int, green: int, blue: int):
        self.red: int = red
        self.green: int = green
        self.blue: int = blue
    
    def __init__(self, tuple: Tuple):
        self.red: int = tuple[0]
        self.green: int = tuple[1]
        self.blue: int = tuple[2]

    def getPyGameColor(self) -> pygame.color.Color:
        return (self.red, self.green, self.blue)


class Block:
    def __init__(self, color: Color, rotations: Rotations):
        self.color: Color = color
        self.rotations: Rotations = rotations
        self.__rotation: Rotation = None
    
    def getRotation(self) -> Rotation:
        if(self.__rotation == None):
            self.__rotation = self.rotations.getRandomRotation()
        
        return self.__rotation
    
    def getRotateLeft(self) -> Rotation:
        if self.__rotation == None:
            return self.getRotation()
        return self.rotations.getLeftRotation(self.__rotation)

    def rotateLeft(self):
        self.__rotation = self.getRotateLeft()

    def getRotateRight(self) -> Rotation:
        if self.__rotation == None:
            return self.getRotation()
        return self.rotations.getRightRotation(self.__rotation)
    
    def rotateRight(self):
        self.__rotation = self.getRotateRight()
        
    

class Block_LINE(Block):
    def __init__(self):
        color = Color(BLOCK_LINE_COLOR)
        leftRotation = [Position(0, 0), Position(0, 1), Position(0, 2), Position(0, 3)]
        topRotation = [Position(0, 0), Position(1, 0), Position(2, 0), Position(3, 0)]
        rotation = Rotations(leftRotation, topRotation, leftRotation, topRotation)
        super().__init__(color, rotation)

class Block_T(Block):
    def __init__(self):
        color = Color(BLOCK_T_COLOR)
        leftRotation = [Position(0, 0, True), Position(1, 0), Position(0, 1), Position(1, 1), Position(0, 2, True), Position(1, 2)]
        topRotation = [Position(0, 0, True), Position(1, 0), Position(2, 0, True), Position(0, 1), Position(1, 1), Position(2, 1)]
        rightRotation = [Position(0, 0), Position(1, 0, True), Position(0, 1), Position(1, 1), Position(0, 2), Position(1, 2, True)]
        bottomRotation = [Position(0, 0), Position(1, 0), Position(2, 0), Position(0, 1, True), Position(1, 1), Position(2, 1, True)]
        rotation = Rotations(leftRotation, topRotation, rightRotation, bottomRotation)
        super().__init__(color, rotation)

class Block_SQUARE(Block):
    def __init__(self):
        color = Color(BLOCK_SQUARE_COLOR)
        leftRotation = [Position(0, 0), Position(1, 0), Position(0, 1), Position(1, 1)]
        rotation = Rotations(leftRotation, leftRotation, leftRotation, leftRotation)
        super().__init__(color, rotation)

class Block_L(Block):
    def __init__(self):
        color = Color(BLOCK_L_COLOR)
        leftRotation = [Position(0, 0), Position(1, 0, True), Position(0, 1), Position(1, 1, True), Position(0, 2), Position(1, 2)]
        topRotation = [Position(0, 0), Position(1, 0), Position(2, 0), Position(0, 1), Position(1, 1, True), Position(2, 1, True)]
        rightRotation = [Position(0, 0), Position(1, 0), Position(0, 1, True), Position(1, 1), Position(0, 2, True), Position(1, 2)]
        bottomRotation = [Position(0, 0, True), Position(1, 0, True), Position(2, 0), Position(0, 1), Position(1, 1), Position(2, 1)]
        rotation = Rotations(leftRotation, topRotation, rightRotation, bottomRotation)
        super().__init__(color, rotation)

class Block_MIRROR_L(Block):
    def __init__(self):
        color = Color(BLOCK_MIRROR_L_COLOR)
        leftRotation = [Position(0, 0, True), Position(1, 0), Position(0, 1, True), Position(1, 1), Position(0, 2), Position(1, 2)]
        topRotation = [Position(0, 0), Position(1, 0, True), Position(2, 0, True), Position(0, 1), Position(1, 1), Position(2, 1)]
        rightRotation = [Position(0, 0), Position(1, 0), Position(0, 1), Position(1, 1, True), Position(0, 2), Position(1, 2, True)]
        bottomRotation = [Position(0, 0), Position(1, 0), Position(2, 0), Position(0, 1, True), Position(1, 1, True), Position(2, 1)]
        rotation = Rotations(leftRotation, topRotation, rightRotation, bottomRotation)
        super().__init__(color, rotation)

class Block_BACKGROUD(Block):
    def __init__(self):
        color = Color(BLOCK_BACKGROUD)
        leftRotation = [Position(0, 0)]
        rotation = Rotations(leftRotation, leftRotation, leftRotation, leftRotation)
        super().__init__(color, rotation)
