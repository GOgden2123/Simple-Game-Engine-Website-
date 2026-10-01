from SimpleGE import *
from random import choice

REND_SCALE = 3
REND_W = 240
REND_H = 160

# DISP_W = 240 * REND_SCALE
# DISP_H = 160 * REND_SCALE

STATE_INTRO = 1
STATE_MENU = 2
STATE_PLAY_3 = 3
STATE_PLAY_4 = 4
STATE_PLAY_5 = 5

class IntroState(State):
    def __init__(self):
        super().__init__(0,0,REND_W,REND_H)
        
        self.renderMode = RENDERMODE_STRETCH
        
        self.entities = [Entity(0,0,REND_W,REND_H,pg.image.load('gfx/intro.bmp'))]
        
        self.introDuration = 5000
        
        self.onTick = IntroState.tickIntro
        self.onEnter = IntroState.reset
        self.onExit = IntroState.reset
        
        return
    #end __init__
    
    @staticmethod
    def reset(target):
        target.introDuration = 5000
        
        return
    #end enter
    
    @staticmethod
    def tickIntro(target, dt):
        target.introDuration -= dt
        
        if target.introDuration <= 0:
            target.exitCode = STATE_MENU
        #end if
        
        return
    #end tickIntro
#end IntroState
    
class MenuState(State):
    def __init__(self):
        super().__init__(0,0,REND_W,REND_H)
        
        self.renderMode = RENDERMODE_STRETCH
        
        self.entities = [Entity(0,0,REND_W,REND_H,pg.image.load('gfx/menu.bmp'))]
        
        self.selectorPoints = [
            (11,105)
            ,(86,105)
            ,(162,105)
        ]
        self.selectorInd = 0
        
        self.entities.append(Entity(0,0,64,32,pg.image.load('gfx/selector.bmp')))
        self.entities[-1].x = self.selectorPoints[self.selectorInd][0]
        self.entities[-1].y = self.selectorPoints[self.selectorInd][1]
        
        self.selectorSFX = pg.mixer.Sound('sfx/slide.wav')
        self.selectSFX = pg.mixer.Sound('sfx/select.wav')
        
        self.onKeyPressed = MenuState.moveSelector
        
        return
    #end __init__
    
    @staticmethod
    def moveSelector(target, key):        
        if key == pg.K_RIGHT:
            target.selectorSFX.play()
            
            target.selectorInd += 1
            
            if target.selectorInd >= len(target.selectorPoints):
                target.selectorInd = 0
            #end if
                
            target.entities[-1].x = target.selectorPoints[target.selectorInd][0]
            target.entities[-1].y = target.selectorPoints[target.selectorInd][1]
        elif key == pg.K_LEFT:
            target.selectorSFX.play()
            
            target.selectorInd -= 1
            
            if target.selectorInd < 0:
                target.selectorInd = len(target.selectorPoints) - 1
            #end if
                
            target.entities[-1].x = target.selectorPoints[target.selectorInd][0]
            target.entities[-1].y = target.selectorPoints[target.selectorInd][1]
        elif key == pg.K_RETURN:            
            target.selectSFX.play()
            
            if target.selectorInd == 0:
                target.exitCode = STATE_PLAY_3
            elif target.selectorInd == 1:
                target.exitCode = STATE_PLAY_4
            elif target.selectorInd == 2:
                target.exitCode = STATE_PLAY_5
            #end if
        #end if
        
        return
    #end moveSelector
#end MenuState
    
class Tile(Entity):
    def __init__(self, i):
        super().__init__(0,0,32,32,pg.image.load('gfx/tiles.bmp'))
        self.id = i
        self.clipRect.x = (i % 5) * 32
        self.clipRect.y = int(i / 5) * 32
        
        return
    #end __init__
#end Tile
    
class TileBoard(Entity):
    def __init__(self, size):
        super().__init__(0,0,size * 32, size * 32, None)
        self.size = size
        self.x = int((REND_W - self.w) / 2)
        self.y = int((REND_H - self.h) / 2)
        self.img.fill((255,0,0))
        self.slideSFX = pg.mixer.Sound('sfx/slide.wav')
        self.solved = False
        self.muted = True
        
        self.tilePositions = [(x * 32, y * 32) for y in range(self.size) for x in range(self.size)]
        
        self.tiles = [
            Tile(i)
            for i in range(self.size ** 2)
        ]
        
        for i in range(self.size ** 2):
            self.tiles[i].x = self.tilePositions[i][0]
            self.tiles[i].y = self.tilePositions[i][1]
        #end for
        
        self.hide()
        
        self.onKeyPressed = TileBoard.moveTile
        
        return
    #end __init__
    
    def update(self):
        for i in range(self.size ** 2):
            self.tiles[i].x = self.tilePositions[i][0]
            self.tiles[i].y = self.tilePositions[i][1]
        #end for
            
        self.checkIfSolved()
        
        return
    #end update
    
    def render(self, renderTarget):
        self.img.fill((0,0,0))
        
        for i in range(self.size ** 2):
            self.tiles[i].render(self.img)
        #end if
        
        super().render(renderTarget)
        
        return
    #end render
    
    def hide(self):
        self.getsTick = False
        self.getsInput = False
        self.getsKeyboardInput = False
        self.getsMouseInput = False
        self.getsJoystickInput = False
        self.getsUpdate = False
        self.getsRender = False
        self.getsCollision = False
        
        self.solved = False
        self.muted = True
        
        return
    #end hide
    
    def show(self):
        self.getsTick = True
        self.getsInput = True
        self.getsKeyboardInput = True
        self.getsMouseInput = True
        self.getsJoystickInput = True
        self.getsUpdate = True
        self.getsRender = True
        self.getsCollision = True
        
        self.solved = False
        
        self.reset()
        self.scramble()
        self.muted = False
        
        return
    #end show
    
    def reset(self):
        self.tiles = [
            Tile(i)
            for i in range(self.size ** 2)
        ]
        
        for i in range(self.size ** 2):
            self.tiles[i].x = self.tilePositions[i][0]
            self.tiles[i].y = self.tilePositions[i][1]
        #end for
        
        return
    #end reset
    
    def scramble(self):
        for i in range(1000):
            TileBoard.moveTile(self, choice((pg.K_UP,pg.K_DOWN,pg.K_LEFT,pg.K_RIGHT)))
        #end for
        
        return
    #end scramble
    
    def checkIfSolved(self):
        self.solved = True
        
        for i in range(self.size ** 2):
            if self.tiles[i].id != i:
                self.solved = False
                break
            #end if
        #end for
        
        return
    #end checkIfSolved
    
    @staticmethod
    def moveTile(self, key):
        freeSpaceIndex = 0
        
        for i in range(self.size ** 2):
            if self.tiles[i].id == 0:
                freeSpaceIndex = i
                break
            #end if
        #end for
                
        northTile = freeSpaceIndex - self.size
        southTile = freeSpaceIndex + self.size
        westTile = freeSpaceIndex - 1
        eastTile = freeSpaceIndex + 1
        
        if key == pg.K_UP and northTile >= 0 and northTile < self.size ** 2 and int(northTile / self.size) < int(freeSpaceIndex / self.size):
            temp = self.tiles[freeSpaceIndex]
            self.tiles[freeSpaceIndex] = self.tiles[northTile]
            self.tiles[northTile] = temp
            
            if self.muted == False:
                self.slideSFX.play()
            #end if
        elif key == pg.K_DOWN and southTile >= 0 and southTile < self.size ** 2 and int(southTile / self.size) > int(freeSpaceIndex / self.size):
            temp = self.tiles[freeSpaceIndex]
            self.tiles[freeSpaceIndex] = self.tiles[southTile]
            self.tiles[southTile] = temp
            
            if self.muted == False:
                self.slideSFX.play()
            #end if
        elif key == pg.K_LEFT and westTile >= 0 and westTile < self.size ** 2 and int(westTile % self.size) < int(freeSpaceIndex % self.size):
            temp = self.tiles[freeSpaceIndex]
            self.tiles[freeSpaceIndex] = self.tiles[westTile]
            self.tiles[westTile] = temp
            
            if self.muted == False:
                self.slideSFX.play()
            #end if
        elif key == pg.K_RIGHT and eastTile >= 0 and eastTile < self.size ** 2 and int(eastTile % self.size) > int(freeSpaceIndex % self.size):
            temp = self.tiles[freeSpaceIndex]
            self.tiles[freeSpaceIndex] = self.tiles[eastTile]
            self.tiles[eastTile] = temp
            
            if self.muted == False:
                self.slideSFX.play()
            #end if
        #end if
        
        return
    #end moveTile
#end TileBoard
    
class PlayState(State):    
    def __init__(self):
        super().__init__(0,0,REND_W,REND_H)
        
        self.renderMode = RENDERMODE_STRETCH
        self.boardSize = 3
        
        self.board3 = TileBoard(3)
        self.board4 = TileBoard(4)
        self.board5 = TileBoard(5)
        
        self.entities = [
            self.board3
            ,self.board4
            ,self.board5
        ]
        
        self.onEnter = PlayState.setUpBoard
        
        PlayState.setUpBoard(self)
        
        return
    #end __init__
    
    def update(self):
        super().update()
        
        if self.boardSize == 3 and self.board3.solved == True:
            self.exitCode = STATE_MENU
        elif self.boardSize == 4 and self.board4.solved == True:
            self.exitCode = STATE_MENU
        elif self.boardSize == 5 and self.board5.solved == True:
            self.exitCode = STATE_MENU
        #end if
        
        return
    #end update
    
    @staticmethod
    def setUpBoard(self):
        if self.boardSize == 4:
            self.board3.hide()
            self.board4.show()
            self.board5.hide()
        elif self.boardSize == 5:
            self.board3.hide()
            self.board4.hide()
            self.board5.show()
        else:
            self.board3.show()
            self.board4.hide()
            self.board5.hide()
        #end if
        
        return
    #end setUpBoard
#end PlayState

class SlidePuzzleGame(Game):
    def __init__(self):
        super().__init__(0,0,REND_W,REND_H)
        
        self.renderMode = RENDERMODE_STRETCH
        
        self.introState = IntroState()
        self.introState.exit()
        self.menuState = MenuState()
        self.menuState.exit()
        self.playState = PlayState()
        self.playState.exit()
        
        self.activeState = STATE_INTRO
        
        self.introState.enter()
        
        self.states = [
            self.introState
            ,self.menuState
            ,self.playState
        ]
        
        self.onTick = SlidePuzzleGame.tickSlidePuzzle
        self.onKeyPressed = SlidePuzzleGame.reset
        
        return
    #end __init__
    
    @staticmethod
    def tickSlidePuzzle(target, dt):
        for state in target.states:
            if state.exitCode > 0:
                if state.exitCode == STATE_INTRO:
                    target.activeState = STATE_INTRO
                    target.introState.enter()
                elif state.exitCode == STATE_MENU:
                    target.activeState = STATE_MENU
                    target.menuState.enter()
                elif state.exitCode == STATE_PLAY_3:
                    target.activeState = STATE_PLAY_3
                    target.playState.boardSize = 3
                    target.playState.enter()
                elif state.exitCode == STATE_PLAY_4:
                    target.activeState = STATE_PLAY_4
                    target.playState.boardSize = 4
                    target.playState.enter()
                elif state.exitCode == STATE_PLAY_5:
                    target.activeState = STATE_PLAY_5
                    target.playState.boardSize = 5
                    target.playState.enter()
                #end if
                
                state.exit()
            #end if
        #end for
        
        return
    #end tickSlidePuzzle
    
    @staticmethod
    def reset(target, key):
        if key == pg.K_ESCAPE:
            if target.activeState in (STATE_PLAY_3, STATE_PLAY_4, STATE_PLAY_5):
                target.playState.exitCode = STATE_MENU
            #end if
        #end if
        
        return
    #end reset
#end SlidePuzzleGame

def main():
    initSimpleGE(REND_W * REND_SCALE,REND_H * REND_SCALE,0,"Slide Puzzle")
    
    slidePuzzleGame = SlidePuzzleGame()
    slidePuzzleGame.run()
    
    return
#end main

if __name__ == '__main__':
    main()
#end if

