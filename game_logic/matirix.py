import random
from numpy import empty
from codesets.blocks import Block, Color, Position, PositionType, Rotation
from codesets.cell import Cell
from codesets.helpers import first
import copy

class Matrix:
    def __init__(self, width: int, height: int, defaultColor: Color):
        self.width: int = width
        self.height: int = height
        self.__matrix: list[list[Cell]] = [[Cell(defaultColor, Position(x, y)) for x in range(width)] for y in range(height)]
        self.currentBlock: Block = None
        self.__currentBlockPositions: list[Position] = []
        self.__defaultColor: Color = defaultColor
    
    def place(self, block: Block):
        self.currentBlock = block
        
        rotation = self.currentBlock.getRotation()
        maxWidthPos = rotation.getMaxWidthPos()
        xPosition = random.randint(0, self.width - 1 - maxWidthPos)
        self.__setBlock(Position(xPosition, 0))

    def get(self, pos: Position) -> Cell:
        # render pivot
        # if self.__getCurrentPosition().equals(pos):
        #     return Cell(Color(0,0,0), pos)
        
        return self.__matrix[pos.y][pos.x]
    
    def moveLeft(self):
        self.__move(Position(-1, 0))
    
    def moveRight(self):
        self.__move(Position(1, 0))

    def moveDown(self):
        if self.__move(Position(0, 1)):
            return True
        self.__unsetBlock()
        return False
    
    def checkLine(self) -> int:
        if self.hasBlock():
            return 0
        
        rowsToDelete = self.__getRowsToDelete()
        if len(rowsToDelete) == 0:
            return 0
        for row in rowsToDelete:
            self.__removeRow(row)
        
        points = self.width * len(rowsToDelete)
        if len(rowsToDelete) == 4:
            points = pow(points, 2)
        return points

    def rotateLeft(self):
        if self.currentBlock == None:
            return
        newRotation = self.currentBlock.getRotateLeft()
        if not self.__checkRotation(newRotation):
            return

        self.currentBlock.rotateLeft()
        self.__setBlock(self.__getCurrentPosition())
    
    def rotateRight(self):
        if self.currentBlock == None:
            return
        newRotation = self.currentBlock.getRotateRight()
        if not self.__checkRotation(newRotation):
            return
        
        self.currentBlock.rotateRight()
        self.__setBlock(self.__getCurrentPosition())
    
    def hasBlock(self):
        return self.currentBlock != None

    def __getRowsToDelete(self) -> list[int]:
        rowsToDelete = []
        for row in range(self.height):
            emptyBlock = first(self.__matrix[row], lambda el: el.type == PositionType.EMPTY)
            if emptyBlock == None:
                rowsToDelete.append(row)
        return rowsToDelete

    def __removeRow(self, rowIndex: int):
        for column in range(self.width):
            self.__set(Position(column, rowIndex), self.__defaultColor, PositionType.EMPTY)
        if rowIndex == 0:
            return
        
        for row in range(rowIndex - 1, -1, -1):
            self.__moveDownRow(row)
    
    def __moveDownRow(self, rowIndex: int):
        for column in range(self.width):
            position = Position(column, rowIndex)
            cell = self.get(position)
            self.__set(position.clone().plus(Position(0, 1)), cell.color, cell.type)

    def __move(self, position: Position) -> bool:
        if self.currentBlock == None:
            return
        nextPosition = self.__getCurrentPosition().clone().plus(position)
        if not self.__checkPosition(nextPosition):
            return False
        self.__setBlock(nextPosition)
        return self.__checkPosition(nextPosition)

    def __set(self, pos: Position, color: Color, type: PositionType = PositionType.EMPTY):
        self.__matrix[pos.y][pos.x] = Cell(color, pos, type)

    def __clear(self):
        for pos in self.__currentBlockPositions:
            self.__set(Position(pos.x, pos.y), self.__defaultColor)
        self.__currentBlockPositions = []

    def __checkRotation(self, rotation: Rotation) -> bool:
        for position in rotation.positions:
            isBlock = self.get(position).type == PositionType.BLOCK
            isCurrenctBlock = first(self.__currentBlockPositions, lambda pos: pos.equals(position)) != None
            if isBlock and not isCurrenctBlock:
                return False
        
        return True

    def __checkPosition(self, newPos: Position) -> bool:
        for pos in self.currentBlock.getRotation().positions:
            if pos.positionType == PositionType.BLOCK:
                blockPosition = pos.clone().plus(newPos)
                if blockPosition.x < 0 or blockPosition.x >= self.width or blockPosition.y >= self.height:
                    return False

                isBlock = self.get(blockPosition).type == PositionType.BLOCK
                isCurrenctBlock = first(self.__currentBlockPositions, lambda pos: pos.equals(blockPosition)) != None
                if isBlock and not isCurrenctBlock:
                    return False
        return True

    def __getCurrentPosition(self) -> Position:
        if len(self.__currentBlockPositions) == 0:
            return Position(0, 0)
        
        currentPositions = copy.deepcopy(self.__currentBlockPositions)
        currentPositions.sort(key = lambda pos: pos.x)
        x = currentPositions[0].x
        currentPositions.sort(key = lambda pos: pos.y)
        y = currentPositions[0].y
        return Position(x, y)

    def __getCurrentPosition(self) -> Position:
        if len(self.__currentBlockPositions) == 0:
            return Position(0, 0)
        
        return Position(self.__minX(), self.__minY())

    def __maxX(self) -> int:
        currentPositions = copy.deepcopy(self.__currentBlockPositions)
        currentPositions.sort(reverse = True, key = lambda pos: pos.x)
        return currentPositions[0].x

    def __maxY(self) -> int:
            currentPositions = copy.deepcopy(self.__currentBlockPositions)
            currentPositions.sort(reverse = True, key = lambda pos: pos.y)
            return currentPositions[0].y

    def __minX(self) -> int:
        currentPositions = copy.deepcopy(self.__currentBlockPositions)
        currentPositions.sort(key = lambda pos: pos.x)
        return currentPositions[0].x

    def __minY(self) -> int:
            currentPositions = copy.deepcopy(self.__currentBlockPositions)
            currentPositions.sort(key = lambda pos: pos.y)
            return currentPositions[0].y

    def __setBlock(self, position: Position):
        self.__clear()
        positionCopy = position.clone()
        rotation = self.currentBlock.getRotation()
        while rotation.getMaxWidthPos() + positionCopy.x >= self.width:
            positionCopy.x -= 1

        for pos in rotation.positions:
            if pos.positionType == PositionType.BLOCK:
                blockPosition = positionCopy.clone().plus(pos)
                self.__set(blockPosition, self.currentBlock.color, PositionType.BLOCK)
                self.__currentBlockPositions.append(blockPosition)
    
    def __unsetBlock(self):
        self.currentBlock = None
        self.__currentBlockPositions = []