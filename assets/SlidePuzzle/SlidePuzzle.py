import pygame as pg

#-------------------------------------------------------------------------------
#   Global Variables
#-------------------------------------------------------------------------------

RENDERMODE_NATIVE = 0
RENDERMODE_STRETCH = 1
RENDERMODE_CENTER = 2

COLLIDEMODE_RECT = 0
COLLIDEMODE_RADIUS = 1

COLOR_DEFAULT = (0,0,0)
COLOR_TRANSPARENT = (255,0,255)

DISP_W = 800
DISP_H = 600
DISP_FLAGS = 0

DISPLAY = None
KEYSDOWN = None
MOUSEDOWN = None
JOYDOWN = None

#-------------------------------------------------------------------------------
#   Entity
#-------------------------------------------------------------------------------

class Entity:    
    def __init__(self, x, y, w, h, img):
        #Size and Position
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        #Movement
        
        self.dx = 0
        self.dy = 0
        self.ddx = 0
        self.ddy = 0
        
        #Image data
        
        self.img = img

        if self.img == None:
            self.img = pg.surface.Surface((w,h))
            self.img.fill(COLOR_DEFAULT)
        #end if

        self.img = self.img.convert()
        self.img.set_colorkey(COLOR_TRANSPARENT)
        
        self.renderMode = RENDERMODE_NATIVE
        self.clipRect = pg.Rect(0,0,w,h)

        #Collision Boundaries
        
        self.hitRect = pg.Rect(x,y,w,h)
        self.hitOffsX = 0
        self.hitOffsY = 0
        self.hitR = w

        if self.hitR > h:
            self.hitR = h
        #end if
        
        self.collideMode = COLLIDEMODE_RECT

        #Status
        
        self.getsTick = True
        self.getsInput = True
        self.getsKeyboardInput = True
        self.getsMouseInput = True
        self.getsJoystickInput = True
        self.getsUpdate = True
        self.getsRender = True
        self.getsCollision = True
        self.debug = False
        self.lastTick = 0
        
        #Callback Functions

        self.onTick = None
        self.onUpdate = None
        self.onRender = None
        self.onCollide = None

        self.onKeyPressed = None
        self.onKeyReleased = None

        self.onMousePressed = None
        self.onMouseReleased = None
        self.onMouseMotion = None
        self.onMouseWheel = None
        
        self.onJoyButtonPressed = None
        self.onJoyButtonReleased = None
        self.onJoyAxisMotion = None
        self.onJoyHatMotion = None

        return
    #end __init__

    def tick(self, dt):
        if self.getsTick == True:
            self.lastTick += dt

            if self.onTick != None:
                self.onTick(self, dt)
            #end if
        #end if

        return
    #end tick

    def handleInput(self, event):
        if self.getsInput == True:
            if self.getsKeyboardInput == True:
                if event.type == pg.KEYDOWN:
                    if self.onKeyPressed != None:
                        self.onKeyPressed(self, event.key)
                    #end if
                elif event.type == pg.KEYUP:
                    if self.onKeyReleased != None:
                        self.onKeyReleased(self, event.key)
                    #end if
            #end if
            
            if self.getsMouseInput == True:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.onMousePressed != None:
                        self.onMousePressed(self, event.button)
                    #end if
                elif event.type == pg.MOUSEBUTTONUP:
                    if self.onMouseReleased != None:
                        self.onMouseReleased(self, event.button)
                    #end if
                elif event.type == pg.MOUSEMOTION:
                    if self.onMouseMotion != None:
                        self.onMouseMotion(self, event.pos)
                    #end if
                elif event.type == pg.MOUSEWHEEL:
                    if self.onMouseWheel != None:
                        self.onMouseWheel(self, event.x, event.y)
                    #end if
                #end if
            #end if
                        
            if self.getsJoystickInput == True:
                if event.type == pg.JOYBUTTONDOWN:
                    if self.onJoyButtonPressed != None:
                        self.onJoyButtonPressed(self, event.instance_id, event.button)
                    #end if
                elif event.type == pg.JOYBUTTONUP:
                    if self.onJoyButtonReleased != None:
                        self.onJoyButtonReleased(self, event.instance_id, event.button)
                    #end if
                elif event.type == pg.JOYAXISMOTION:
                    if self.onJoyAxisMotion != None:
                        self.onJoyAxisMotion(self, event.instance_id, event.axis, event.value)
                    #end if
                elif event.type == pg.JOYHATMOTION:
                    if self.onJoyHatMotion != None:
                        self.onJoyHatMotion(self, event.instance_id, event.hat, event.value)
                    #end if
                #endif
            #end if
        #end if

        return
    #end handleInput

    def update(self):
        if self.getsUpdate == True:
            self.dx += self.ddx
            self.dy += self.ddy
            self.x += self.dx
            self.y += self.dy

            self.hitRect.topleft = (
                self.x + self.hitOffsX
                ,self.y + self.hitOffsY
            )
            
            if self.onUpdate != None:
                self.onUpdate(self)
            #end if
        #end if

        return
    #end update

    def render(self, renderTarget):        
        if self.getsRender == True:
            if self.renderMode == RENDERMODE_NATIVE:
                renderTarget.blit(
                    self.img
                    ,(int(self.x), int(self.y))
                    ,self.clipRect
                )
            elif self.renderMode == RENDERMODE_STRETCH:
                pg.transform.scale(
                    self.img
                    ,renderTarget.get_size()
                    ,renderTarget
                )
            #end if
                
            if self.onRender != None:
                self.onRender(self, renderTarget)
            #end if
        #end if
                
        if self.debug == True:
            self.debug(renderTarget)
        #end if

        return
    #end render
    
    def debugRect(self, renderTarget):
        pg.draw.rect(renderTarget, (255,0,0), (self.x,self.y,self.w,self.h), 1)
        pg.draw.rect(renderTarget, (0,0,255), (self.hitX,self.hitY,self.hitW,self.hitH), 1)
        
        return
    #end debugRect

    def collide(self, other):
        if self.getsCollision == True:
            if self.collideMode == COLLIDEMODE_RECT:
                if self.hitRect.colliderect(other.hitRect) == True:
                    if self.onCollide != None:
                        self.onCollide(self, other)
                    #end if
                    
                    return True
                else:
                    return False
                #end if
            elif self.collideMode == COLLIDEMODE_RADIUS:
                xDif = other.hitRect.centerx - self.hitRect.centerx
                yDif = other.hitRect.centery - self.hitRect.centery
                sqrDist = (xDif ** 2) + (yDif ** 2)
                sqrRadiiSum = (other.hitR + self.hitR) ** 2

                if sqrDist <= sqrRadiiSum:
                    if self.onCollide != None:
                        self.onCollide(self,other)
                    #end if
                    
                    return True
                else:
                    return False
                #end if
            #end if
        #end if

        return False
    #end collide
#end Entity

#-------------------------------------------------------------------------------
#   State
#-------------------------------------------------------------------------------

class State(Entity):    
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, None)

        self.renderMode = RENDERMODE_STRETCH

        self.entities = []
        self.exitCode = 0

        self.onEnter = None
        self.onExit = None

        return
    #end __init__

    def tick(self, dt):
        for entity in self.entities:
            entity.tick(dt)
        #end for

        super().tick(dt)

        return
    #end tick

    def handleInput(self, event):
        for entity in self.entities:
            entity.handleInput(event)
        #end for

        super().handleInput(event)
        
        return
    #end handleInput

    def update(self):
        for entity in self.entities:
            entity.update()
        #end for

        super().update()
        
        self.checkCollisions()

        return
    #end update
    
    def checkCollisions(self):
        if self.getsCollision == True:
            for i in range(len(self.entities) - 1):
                for j in range(i + 1, len(self.entities)):
                    self.entities[i].collide(self.entities[j])
                    self.entities[j].collide(self.entities[i])
                #end for
            #end for
        #end if
        
        return
    #end checkCollisions

    def render(self, renderTarget):
        self.img.fill(COLOR_DEFAULT)
        
        for entity in self.entities:
            entity.render(self.img)
        #end for
            
        super().render(renderTarget)

        return
    #end render

    def enter(self):
        self.getsTick = True
        self.getsInput = True
        self.getsKeyboardInput = True
        self.getsMouseInput = True
        self.getsJoystickInput = True
        self.getsUpdate = True
        self.getsRender = True
        self.getsCollision = True
        
        self.exitCode = 0

        if self.onEnter != None:
            self.onEnter(self)
        #end if

        return
    #end enter

    def exit(self):
        self.getsTick = False
        self.getsInput = False
        self.getsKeyboardInput = False
        self.getsMouseInput = False
        self.getsJoystickInput = False
        self.getsUpdate = False
        self.getsRender = False
        self.getsCollision = False
        
        self.exitCode = 0

        if self.onExit != None:
            self.onExit(self)
        #end if

        return
    #end exit
#end State

#-------------------------------------------------------------------------------
#   App
#-------------------------------------------------------------------------------

class Game(Entity):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, None)
        
        self.renderMode = RENDERMODE_STRETCH
        self.states = []

        self.frameTimer = 1000 / 40
        self.frameDt = 0

        self.running = False

        self.onStart = None
        self.onQuit = None
        
        self.onKeysDown = None
        self.onMouseDown = None
        
        self.onJoyDeviceAdded = None
        self.onJoyDeviceRemoved = None
        self.onJoyButtonsDown = None
        

        return
    #end __init__

    def tick(self, dt):
        self.frameDt = pg.time.get_ticks() - self.lastTick
        
        while self.frameDt < self.frameTimer:
            self.frameDt += pg.time.get_ticks() - self.lastTick
        #end while
            
        for state in self.states:
            state.tick(self.frameDt)
        #end for
            
        super().tick(self.frameDt)

        return
    #end tick

    def handleInput(self, event):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

                return
            else:
                for state in self.states:
                    state.handleInput(event)
                #end for

                super().handleInput(event)
            #end if
        #end for
                
        getInputStates()
        
        if self.getsInput == True:
            if self.getsKeyboardInput == True:
                if self.onKeysDown != None:
                    self.onKeysDown(self, KEYSDOWN)
                #end if
            #end if
                    
            if self.getsMouseInput == True:
                if self.onMouseDown != None:
                    self.onMouseDown(self, MOUSEDOWN)
                #end if
            #end if
        #end if
        
        return
    #end handleInput

    def update(self):
        for state in self.states:
            state.update()
        #end for

        super().update()

        return
    #end update

    def render(self, renderTarget):
        self.img.fill(COLOR_DEFAULT)
        
        for state in self.states:
            state.render(self.img)
        #end for

        super().render(renderTarget)
        pg.display.flip()

        return
    #end render

    def run(self):
        self.running = True

        if self.onStart != None:
            self.onStart(self)
        #end if

        while self.running == True:
            self.tick(0)
            self.handleInput(None)
            self.update()
            self.render(DISPLAY)
        #end while

        if self.onQuit != None:
            self.onQuit(self)
        #end if

        pg.quit()

        return
    #end run
    
    def pushState(self, state):
        self.states.append(state)
        
        state.enter()
        
        return
    #end pushState
    
    def popState(self, index):
        self.states[index].exit()
        self.states.pop(index)
        
        return
    #end popState
#end App

#-------------------------------------------------------------------------------
#   Functions
#-------------------------------------------------------------------------------

def initSimpleGE(dispW, dispH, dispFlags, title):
    global DISP_W, DISP_H, DISPLAY, KEYSDOWN, MOUSEDOWN

    pg.init()
    
    DISP_W = dispW
    DISP_H = dispH
    DISP_FLAGS = dispFlags
    
    DISPLAY = pg.display.set_mode((DISP_W, DISP_H), DISP_FLAGS)
    pg.display.set_caption(title)
    
    KEYSDOWN = pg.key.get_pressed()
    MOUSEDOWN = pg.mouse.get_pressed()

    return
#end return

def getInputStates():
    global KEYSDOWN, MOUSEDOWN
    
    KEYSDOWN = pg.key.get_pressed()
    MOUSEDOWN = pg.mouse.get_pressed()
    
    return
#end getInputStates

def main():
    initSimpleGE(800,600,0,"Test")

    entity = Entity(0,0,200,200,None)
    entity.img.fill((255,0,0))
    entity.clipRect.w = 100
    
    state = State(0,0,400,400,[entity])
    state.renderMode = 1
    app = Game(0,0,800,800,[state])
    app.renderMode = 1
    
    app.run()

    return
#end main

if __name__ == '__main__':
    main()
#end if

