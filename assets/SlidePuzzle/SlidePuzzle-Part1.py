from SimpleGE import *

#Global Settings
REND_SCALE = 3
REND_W = 240
REND_H = 160

def main():
    #Initialize SGE and set up the Display
    dispW = REND_W * REND_SCALE
    dispH = REND_H * REND_SCALE
    dispFlags = 0
    title = "Slide Puzzle"
    
    initSimpleGE(dispW, dispH, dispFlags, title)
    
    #Create a Game object and run it
    gameX = 0
    gameY = 0
    slidePuzzleGame = Game(gameX, gameY, REND_W, REND_H)
    slidePuzzleGame.debug = True
    
    slidePuzzleGame.run()
    
    return
#end main

#Program Entry Point
if __name__ == '__main__':
    main()
#end if