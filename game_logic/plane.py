import pygame
from codesets.blocks import Position, Color, PositionType, Block
from codesets.cell import Cell, getRandomBlock
from game_logic.matirix import Matrix
from codesets.colors import GAME_PLANE_COLOR

CELL_COUNT_WIDTH = 10
CELL_COUNT_HEIGHT = 22

class Plane:
    def __init__(self, surface : pygame.Surface, surfaceWidth: int, surfaceHeight: int, topMargin: int, bottomMargin: int):
        self.surfaceWidth: int = surfaceWidth
        self.surfaceHeight: int = surfaceHeight
        self.nextBlock = getRandomBlock()

        self.__matrix: Matrix = Matrix(CELL_COUNT_WIDTH, CELL_COUNT_HEIGHT, Color(GAME_PLANE_COLOR))
        self.__surface: pygame.Surface = surface
        self.__topMargin: int = topMargin
        self.__bottomMargin: int = bottomMargin
        self.__leftBorder: int = 0
        self.__cellSize: int = 0
        self.__savedBlock: Block = None
        self.__canSave: bool = True
        self.__setPlaneSize()

    #region Blocks
    def placeBlock(self):
        self.__canSave = True
        self.__matrix.place(self.nextBlock)
        self.nextBlock = getRandomBlock()
        
    def rotateLeft(self):
        self.__matrix.rotateLeft()

    def rotateRight(self):
        self.__matrix.rotateRight()

    def moveRight(self):
        self.__matrix.moveRight()

    def moveLeft(self):
        self.__matrix.moveLeft()

    def moveDown(self):
        if self.__matrix.hasBlock() and self.__matrix.moveDown():
            return True
        
        return False
    
    def checkLine(self) -> int:
        return self.__matrix.checkLine()

    def hasBlock(self) -> bool:
        return self.__matrix.hasBlock()
    
    def saveBlock(self):
        if not self.__canSave:
            return
        current = self.__matrix.currentBlock
        if self.__savedBlock != None:
            self.__matrix.place(self.__savedBlock)
            self.__savedBlock = current
            self.__canSave = False
            return
        
        self.__savedBlock = current
        self.placeBlock()
        self.__canSave = False
    
    #endregion

    #region Render Plane

    def getPlaneLeftPivot(self) -> Position:
        return Position(self.__leftBorder, self.surfaceHeight - self.__cellSize * self.__matrix.height)
    
    def getGameWidth(self) -> int:
        return self.__cellSize * self.__matrix.width

    def render(self):
        self.__renderGamePlane()
        self.__renderNextBlock()
        self.__renderSavedBlock()
        
    def reRenderPlane(self, surfaceWidth: int, surfaceHeight: int):
        self.surfaceWidth = surfaceWidth
        self.surfaceHeight = surfaceHeight
        self.__setPlaneSize()

    def __renderSavedBlock(self):
        if self.__savedBlock == None:
            return
        leftRotation = self.__savedBlock.rotations.left
        for row in range(leftRotation.getMaxHeightPos() + 1):
            for column in range(leftRotation.getMaxWidthPos() + 1):
                position = leftRotation.getPosition(column, row)
                if position.positionType == PositionType.EMPTY:
                    continue
                center = self.getPlaneLeftPivot().x + self.getGameWidth() / 2
                cellsize = 15
                position = Position(column, row)
                x = center - 30 - ((leftRotation.getMaxWidthPos() + 1) * cellsize) + (cellsize * position.x)
                y = 50 + (cellsize * position.y)
                self.__renderCell(Position(x, y), self.__savedBlock.color, cellsize)

    def __renderNextBlock(self):
        leftRotation = self.nextBlock.rotations.left
        for row in range(leftRotation.getMaxHeightPos() + 1):
            for column in range(leftRotation.getMaxWidthPos() + 1):
                position = leftRotation.getPosition(column, row)
                if position.positionType == PositionType.EMPTY:
                    continue
                center = self.getPlaneLeftPivot().x + self.getGameWidth() / 2
                cellsize = 15
                position = Position(column, row)
                x = 30 + center + (cellsize * position.x)
                y = 50 + (cellsize * position.y)
                self.__renderCell(Position(x, y), self.nextBlock.color, cellsize)

    def __renderGamePlane(self):
        for column in range(self.__matrix.width):
            for row in range(self.__matrix.height):
                position = Position(column, row)
                x = self.__leftBorder + (self.__cellSize * position.x)
                y = self.surfaceHeight - self.__bottomMargin - (self.__cellSize * (self.__matrix.height - position.y))
                self.__renderCell(Position(x, y), self.__matrix.get(position).color, self.__cellSize)

    def __renderCell(self, pos: Position, color: Color, cellSize: int):
        pygame.draw.rect(self.__surface, color.getPyGameColor(), pygame.Rect(pos.x, pos.y, cellSize, cellSize))
        # render indexes
        # my_font = pygame.font.SysFont('arial', 15)
        # text_surface = my_font.render(str(cell.position.x) + "," + str(cell.position.y), False, (0, 0, 0))
        # self.__surface.blit(text_surface, (x + 5, y + 5))

    def __setPlaneSize(self):
        planeWidth = self.surfaceWidth
        maxPlaneHeight = self.surfaceHeight - self.__topMargin - self.__bottomMargin
        planeHeight = self.__getPlaneHeight(planeWidth)
        cellSize = self.__getCellSize(planeWidth)
        while ((not planeHeight.is_integer()) or planeHeight > maxPlaneHeight or (not cellSize.is_integer())) and planeWidth > 0:
            planeWidth -=1
            planeHeight = self.__getPlaneHeight(planeWidth)
            cellSize = self.__getCellSize(planeWidth)
        
        self.__leftBorder = (self.surfaceWidth - planeWidth) / 2
        self.__cellSize = cellSize
    
    def __getPlaneHeight(self, planeWidth: int) -> int:
        return (planeWidth * self.__matrix.height) / self.__matrix.width
    
    def __getCellSize(self, planeWidth: int) -> int:
        return planeWidth / self.__matrix.width

    #endregion