from enum import Enum
from pyclbr import Function
import random
import codesets.blocks

class CellType(Enum):
    BACKGROUD = 1
    LINE = 2
    T = 3
    SQUARE = 4
    L = 5
    MIRROR_L = 6

class Cell:
    def __init__(self, color: codesets.blocks.Color, position: codesets.blocks.Position, type: codesets.blocks.PositionType = codesets.blocks.PositionType.EMPTY):
        self.color: codesets.blocks.Color = color
        self.type: codesets.blocks.PositionType = type
        self.position:codesets.blocks.Position = position

def getBlock(cell: CellType) -> codesets.blocks.Block:
    switcher = {
        CellType.BACKGROUD: codesets.blocks.Block_BACKGROUD(),
        CellType.LINE: codesets.blocks.Block_LINE(),
        CellType.T: codesets.blocks.Block_T(),
        CellType.SQUARE: codesets.blocks.Block_SQUARE(),
        CellType.L: codesets.blocks.Block_L(),
        CellType.MIRROR_L: codesets.blocks.Block_MIRROR_L(),
    }

    return switcher.get(cell)

def getRandomBlock() -> codesets.blocks.Block:
    randomBlockNumber = random.randint(2, 6)
    return getBlock(CellType(randomBlockNumber))