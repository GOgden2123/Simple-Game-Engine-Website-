from SimpleGE import *

#Global Settings
REND_SCALE = 3
REND_W = 240
REND_H = 160

class IntroState(State):
    def __init__(self):
        super().__init__(0,0,REND_W,REND_H)
        
        self.bg = Entity(0,0,REND_W,REND_H,pg.image.load('gfx/intro.bmp'))
        
        self.entities = [
            self.bg    
        ]
        
        return
    #end __init__
#end IntroState
    
class MenuState(State):
    def __init__(self):
        super().__init__(0,0,REND_W,REND_H)
        
        return
    #end __init__
#end MenuState
    
class PlayState(State):    
    def __init__(self):
        super().__init__(0,0,REND_W,REND_H)
        
        return
    #end __init__
#end PlayState
    
class SlidePuzzleGame(Game):
    def __init__(self):
        super().__init__(0,0,REND_W,REND_H)
        
        self.introState = IntroState()
        self.menuState = MenuState()
        self.playState = PlayState()
        
        self.introState.enter()
        self.menuState.exit()
        self.playState.exit()
        
        self.states = [
            self.introState
            ,self.menuState
            ,self.playState
        ]
        
        return
    #end __init__
#end SlidePuzzleGame

def main():
    #Initialize SGE and set up the Display
    dispW = REND_W * REND_SCALE
    dispH = REND_H * REND_SCALE
    dispFlags = pg.RESIZABLE
    title = "Slide Puzzle"
    
    initSimpleGE(dispW, dispH, dispFlags, title)
    
    #Create a Game object and run it
    slidePuzzleGame = SlidePuzzleGame()
    
    slidePuzzleGame.run()
    
    return
#end main

#Program Entry Point
if __name__ == '__main__':
    main()
#end if
