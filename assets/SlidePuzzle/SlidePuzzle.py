from SimpleGE import *
from random import randint, choice

DISP_W: int = 800
DISP_H: int = 800
RENDER_W: int = 800
RENDER_H: int = 800
TILESIZE: int = 160

class MenuState(State):
    def __init__(self) -> None:
        super().__init__(0,0,RENDER_W,RENDER_H)
        
        self.font: pg.font.Font = pg.font.Font(None, size=100)
        
        tempTextSurf: pg.surface.Surface = self.font.render('Slide Puzzle',False,(255,255,255))
        self.textSlidePuzzle: Entity = Entity(0,0,tempTextSurf.get_width(), tempTextSurf.get_height())
        self.textSlidePuzzle.img.blit(tempTextSurf,(0,0))
        self.textSlidePuzzle.rect.midtop = self.rect.midtop
        
        tempTextSurf: pg.surface.Surface = self.font.render('3 x 3',False,(255,255,255))
        self.text3x3: Entity = Entity(0,100,tempTextSurf.get_width(), tempTextSurf.get_height())
        self.text3x3.img.blit(tempTextSurf,(0,0))
        
        tempTextSurf: pg.surface.Surface = self.font.render('4 x 4',False,(255,255,255))
        self.text4x4: Entity = Entity(0,200,tempTextSurf.get_width(), tempTextSurf.get_height())
        self.text4x4.img.blit(tempTextSurf,(0,0))
        
        tempTextSurf: pg.surface.Surface = self.font.render('5 x 5',False,(255,255,255))
        self.text5x5: Entity = Entity(0,300,tempTextSurf.get_width(), tempTextSurf.get_height())
        self.text5x5.img.blit(tempTextSurf,(0,0))
        
        self.entities = [
            self.textSlidePuzzle
            ,self.text3x3
            ,self.text4x4
            ,self.text5x5
        ]
        
        return
    #end __init__
#end MenuState
    
class Tile(Entity):
    def __init__(self, x: int, y: int, w: int, h:int, img: pg.surface.Surface, id: int) -> None:
        super().__init__(x,y,w,h)
        self.img = img
        self.id = id
        
        return
    #end __init__
    
    def __repr__(self) -> None:
        return str(self.id)
    
    def __str__(self) -> None:
        return self.__repr__()
#end Tile

class PlayState(State):
    def __init__(self, size: int) -> None:        
        self.size: int = size
        super().__init__(0,0,TILESIZE*self.size,TILESIZE*self.size)
        self.scale: float = self.img.get_width() / RENDER_W
        self.renderMode = RENDERMODE_STRETCH
        self.mousePos: list = [0,0]
        
        self.tileSet: pg.surface.Surface = pg.image.load('gfx/tiles.bmp')
        self.tileSet.set_colorkey((255,0,255))
        
        self.tileGrid: list = [
            pg.Rect(x, y, TILESIZE, TILESIZE)
            for y in range(0, self.img.get_height(), TILESIZE)
            for x in range(0, self.img.get_width(), TILESIZE)
        ]
        
        self.tileImgs: list = [
            self.tileSet.subsurface((x, y, TILESIZE, TILESIZE))
            for y in range(0, self.tileSet.get_height(), TILESIZE)
            for x in range(0, self.tileSet.get_width(), TILESIZE)
        ]
            
        self.onEnter = PlayState.onEnter
        self.onMouseMotion = PlayState.getMousePos
        self.onMouseButtonPressed = PlayState.onClick
        
        self.setupGrid()
        
        return
    #end __init__
    
    def update(self) -> None:
        if self.active == True:
            for i in range(len(self.entities)):
                self.entities[i].rect.center = self.tileGrid[i].center
            #end for
        #end if
        
        return
    #end update
    
    def shuffleTiles(self) -> None:        
        for i in range(100):
            lastLoc: int = [x.id for x in self.entities].index(0)
            x: int = lastLoc % self.size
            y: int = int(lastLoc / self.size)
            neighbors: list = []
            
            if y == 0:
                if x == 0:
                    neighbors = [
                        ((y + 0) * self.size + (x + 1))
                        ,((y + 1) * self.size + (x + 0))
                    ]
                elif x > 0 and x < self.size - 1:
                    neighbors = [
                        ((y + 0) * self.size + (x - 1))
                        ,((y + 0) * self.size + (x + 1))
                        ,((y + 1) * self.size + (x + 0))
                    ]
                elif x == self.size - 1:
                    neighbors = [
                        ((y + 0) * self.size + (x - 1))
                        ,((y + 1) * self.size + (x + 0))
                    ]
                #end if
            elif y > 0 and y < self.size - 1:
                if x == 0:
                    neighbors = [
                        ((y + 0) * self.size + (x + 1))
                        ,((y - 1) * self.size + (x + 0))
                        ,((y + 1) * self.size + (x + 0))
                    ]
                elif x > 0 and x < self.size - 1:
                    neighbors = [
                        ((y + 0) * self.size + (x - 1))
                        ,((y + 0) * self.size + (x + 1))
                        ,((y - 1) * self.size + (x + 0))
                        ,((y + 1) * self.size + (x + 0))
                    ]
                elif x == self.size - 1:
                    neighbors = [
                        ((y + 0) * self.size + (x - 1))
                        ,((y - 1) * self.size + (x + 0))
                        ,((y + 1) * self.size + (x + 0))
                    ]
                #end if
            elif y == self.size - 1:
                if x == 0:
                    neighbors = [
                        ((y + 0) * self.size + (x + 1))
                        ,((y - 1) * self.size + (x + 0))
                    ]
                elif x > 0 and x < self.size - 1:
                    neighbors = [
                        ((y + 0) * self.size + (x - 1))
                        ,((y + 0) * self.size + (x + 1))
                        ,((y - 1) * self.size + (x + 0))
                    ]
                elif x == self.size - 1:
                    neighbors = [
                        ((y + 0) * self.size + (x - 1))
                        ,((y - 1) * self.size + (x + 0))
                    ]
                #end if
            #end if
            
            self.swapTiles(choice(neighbors))
        #end for
        
        return
    #end shuffleTiles
    
    def setupGrid(self) -> None:
        self.entities = [
            Tile(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE, self.tileImgs[y * self.size + x], y * self.size + x)
            for y in range(self.size)
            for x in range(self.size)
        ]
        
        self.shuffleTiles()
                
        return
    #end setupGrid
    
    def swapTiles(self, i: int) -> None:
        x: int = i % self.size
        y: int = int(i / self.size)
        i2: int = 0
        temp: Entity = None
        
        if x > 0:
            i2 = (y + 0) * self.size + (x + -1)
            
            if self.entities[i2].id == 0:
#                 print('swapping tile #%d with #%d' % (i, i2))
                temp = self.entities[i]
                self.entities[i] = self.entities[i2]
                self.entities[i2] = temp
#                 print(self.entities)
                return
            #end if
        #end if
                
        if x < self.size - 1:
            i2 = (y + 0) * self.size + (x + 1)
            
            if self.entities[i2].id == 0:
#                 print('swapping tile #%d with #%d' % (i, i2))
                temp = self.entities[i]
                self.entities[i] = self.entities[i2]
                self.entities[i2] = temp
#                 print(self.entities)
                return
            #end if
        #end if
            
        if y > 0:
            i2 = (y + -1) * self.size + (x + 0)
            
            if self.entities[i2].id == 0:
#                 print('swapping tile #%d with #%d' % (i, i2))
                temp = self.entities[i]
                self.entities[i] = self.entities[i2]
                self.entities[i2] = temp
#                 print(self.entities)
                return
            #end if
        #end if
            
        if y < self.size - 1:
            i2 = (y + 1) * self.size + (x + 0)
            
            if self.entities[i2].id == 0:
#                 print('swapping tile #%d with #%d' % (i, i2))
                temp = self.entities[i]
                self.entities[i] = self.entities[i2]
                self.entities[i2] = temp
#                 print(self.entities)
                return
            #end if
        #end if
        
        return
    #end swapTiles
    
    @staticmethod
    def onEnter(self) -> None:
        self.setupGrid()
        
        return
    #end onEnter
    
    @staticmethod
    def getMousePos(self, pos: list) -> None:
        self.mousePos[0] = round(pos[0] * self.scale)
        self.mousePos[1] = round(pos[1] * self.scale)
        
        return
    #end getMousePos
    
    @staticmethod
    def onClick(self, button: int) -> None:
        for i in range(len(self.entities)):
            if self.entities[i].rect.collidepoint(self.mousePos):
                self.swapTiles(i)
                break
            #end if
        #end for
        
        return
    #end swapTiles
#end PlayState

class SlidePuzzleGame(Game):
    def __init__(self) -> None:
        super().__init__('Slide Puzzle', DISP_W, DISP_H, RENDER_W, RENDER_H, 0)
        
        self.menuState: MenuState = MenuState()
        self.menuState.exit()
        self.playState3x3: PlayState = PlayState(3)
        self.playState3x3.exit()
        self.playState4x4: PlayState = PlayState(4)
        self.playState4x4.exit()
        self.playState5x5: PlayState = PlayState(5)
        self.playState5x5.exit()
        
        self.states = [
            self.menuState
            ,self.playState3x3
            ,self.playState4x4
            ,self.playState5x5
        ]
        
#         self.menuState.enter()
        self.playState3x3.enter()
        
        return
    #end __init__
#end SlidePuzzleGame

def main() -> None:
    slidePuzzle: SlidePuzzleGame = SlidePuzzleGame()
    slidePuzzle.run()
    
    return
#end main

if __name__ == '__main__':
    main()
#end main
