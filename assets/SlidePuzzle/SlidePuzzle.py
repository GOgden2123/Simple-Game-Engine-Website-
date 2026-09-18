import pygame as pg

COLLIDEMODE_RECT = 0
COLLIDEMODE_RADIUS = 1

RENDERMODE_NATIVE = 0
RENDERMODE_STRETCH = 1
RENDERMODE_CENTER = 2

class Entity:
    def __init__(self, x, y, w, h):
        self.active = True
        self.visible = True
        self.solid = True
        self.debug = False
        self.getsInput = True

        self.img = pg.surface.Surface((w,h))
        self.rect = pg.Rect(x,y,w,h)
        self.renderMode = RENDERMODE_NATIVE

        self.collideRect = pg.Rect(x,y,w,h)
        self.collideRadius = min(w,h)
        self.collideMode = COLLIDEMODE_RECT
        
        self.x = float(x)
        self.y = float(y)
        self.dx = 0.0
        self.dy = 0.0
        self.ddx = 0.0
        self.ddy = 0.0
        
        self.onTick = None

        self.onKeyPressed = None 
        self.onKeyReleased = None
        self.onKeysDown = None

        self.onMouseButtonPressed = None
        self.onMouseButtonReleased = None
        self.onMouseButtonsDown = None

        self.onMouseMotion = None
        self.onMouseWheel = None

        self.onJoyButtonPressed = None
        self.onJoyButtonReleased = None
        self.onJoyButtonsDown = None

        self.onJoyAxisMotion = None
#         self.onJoyBallMotion = None
        self.onJoyHatMotion = None

        return
    #end __init__

    def handleEvent(self, event):
        if event.type == pg.QUIT:
            self.active = False
        elif self.getsInput == True:
            if event.type == pg.KEYDOWN:
                if self.onKeyPressed != None:
                    self.onKeyPressed(self, event.key)
                #end if
            elif event.type == pg.KEYUP:
                if self.onKeyReleased != None:
                    self.onKeyReleased(self, event.key)
                #end if
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.onMouseButtonPressed != None:
                    self.onMouseButtonPressed(self, event.button)
                #end if
            elif event.type == pg.MOUSEBUTTONUP:
                if self.onMouseButtonReleased != None:
                    self.onMouseButtonReleased(self, event.button)
                #end if
            elif event.type == pg.MOUSEMOTION:
                if self.onMouseMotion != None:
                    self.onMouseMotion(self, event.pos)
                #end if
            elif event.type == pg.MOUSEWHEEL:
                if self.onMouseWheel != None:
                    self.onMouseWheel(self, (event.x, event.y))
                #end if
            elif event.type == pg.JOYBUTTONDOWN:
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
            #end if
        #end if

        return
    #end handleEvent

    def update(self):
        if self.active == True:
            self.dx += self.ddx
            self.dy += self.ddy
            self.x += self.dx
            self.y += self.dy
            self.rect.left = int(self.x)
            self.rect.top = int(self.y)
            self.collideRect.center = self.rect.center
        #end if

        return
    #end update

    def render(self, renderTarget):
        if self.visible == True:            
            if self.renderMode == RENDERMODE_NATIVE:
                renderTarget.blit(self.img,self.rect)
            elif self.renderMode == RENDERMODE_STRETCH:
                pg.transform.scale(
                    self.img
                    ,renderTarget.get_size()
                    ,renderTarget
                )
            elif self.renderMode == RENDERMODE_CENTER:
                renderTarget.blit(
                    self.img
                    ,self.rect.move(
                        int((renderTarget.get_width()-self.img.get_width())/2)
                        ,int((renderTarget.get_height()-self.img.get_height())/2)
                    )
                )
            #end if
        #end if

        return
    #end render
    
    def debugRect(self, renderTarget):
        pg.draw.rect(renderTarget, (255,0,0), self.rect, 1)
        pg.draw.rect(renderTarget, (0,0,255), self.collideRect, 1)
        
        return
    #end debugRect

    def collide(self, other):
        if self.solid == True:
            if isinstance(other,Entity):
                if self.collideMode == COLLIDEMODE_RECT:
                    return self.collideRect.colliderect(other.collideRect)
                elif self.collideMode == COLLIDEMODE_RADIUS:
                    dx = other.collideRect.center[0] - self.collideRect.center[0]
                    dy = other.collideRect.center[1] - self.collideRect.center[1]
                    d = (dx * dx) + (dy * dy)
                    r = other.collideRadius + self.collideRadius
                    r = r * r
                    return d < r
                #end if
            else:
                return False
            #end if
        else:
            return False
        #end if
    #end collide
#end Entity

class State(Entity):
    def __init__(self,x,y,w,h):
        super().__init__(x,y,w,h)
        self.entities = []
        self.exitCode = 0

        self.onEnter = None
        self.onExit = None

        return
    #end __init__
    
    def update(self):        
        if self.active == True:
            for entity in self.entities:
                entity.update()
            #end for
            
            super().update()
        #end if
        
        return
    #end update
    
    def render(self, renderTarget):
        self.img.fill((0,0,0))
        
        if self.visible == True:
            for entity in self.entities:
                entity.render(self.img)
            #end for
                
            super().render(renderTarget)
        #end if
        
        return
    #end render
    
    def enter(self):
        self.active = True
        self.visible = True
        self.solid = True
        self.getsInput = True
        
        if self.onEnter != None:
            self.onEnter(self)
        #end if
        
        return
    #end enter
    
    def exit(self):
        self.active = False
        self.visible = False
        self.solid = False
        self.getsInput = False
        
        if self.onExit != None:
            self.onExit(self)
        #end if
        
        return
    #end exit
#end State

class Game(Entity):
    def __init__(self, title, dispW, dispH, resW, resH, flags):
        pg.init()
        super().__init__(0,0,resW,resH)

        self.display = pg.display.set_mode((dispW,dispH),flags)
        pg.display.set_caption(title)

        self.frameTimer = int(1000 / 40)
        self.frameTimeDelta = 0
        self.lastFrameTick = 0

        self.keysDown = pg.key.get_pressed()
        self.mouseButtonsDown = pg.mouse.get_pressed()
        self.mousePos = pg.mouse.get_pos()

        self.states = []
        
        self.onJoyDeviceAdded = None
        self.onJoyDeviceRemoved = None
        
        self.onStart = None
        self.onQuit = None

        return
    #end __init__

    def __del__(self):
        pg.quit()

        return
    #end __del__

    def handleEvents(self):
        for event in pg.event.get():
            self.handleEvent(event)

            for state in self.states:
                state.handleEvent(event)

                for Entity in state.entities:
                    Entity.handleEvent(event)
                #end for
            #end for
        #end for

        self.keysDown = pg.key.get_pressed()
        self.mouseButtonsDown = pg.mouse.get_pressed()
        self.mousePos = pg.mouse.get_pos()

        if self.onKeysDown != None and self.getsInput == True:
            self.onKeysDown(self, self.keysDown)
        #end if

        if self.onMouseButtonsDown != None and self.getsInput == True:
            self.onMouseButtonsDown(self, self.mouseButtonsDown)
        #end if

        for state in self.states:
            if state.getsInput == True:
                if state.onKeysDown != None:
                    state.onKeysDown(state, self.keysDown)
                #end if

                if state.onMouseButtonsDown != None:
                    state.onMouseButtonsDown(state, self.mouseButtonsDown)
                #end if
                    
                for entity in state.entities:
                    if entity.onKeysDown != None and entity.getsInput == True:
                        entity.onKeysDown(entity, self.keysDown)
                    #end if

                    if entity.onMouseButtonsDown != None and entity.getsInput == True:
                        entity.onMouseButtonsDown(entity, self.mouseButtonsDown)
                    #end if
                #end for
            #end if
        #end for
        
        return
    #end handleEvents

    def update(self):
        if self.active == True:
            for state in self.states:
                state.update()
            #end for
            
            super().update()
        #end if

        return
    #end update

    def render(self, renderTarget):
        self.display.fill((0,0,0))
        self.img.fill((0,0,0))
        
        if self.visible == True:
            for state in self.states:
                state.render(self.img)
            #end for
            
            super().render(renderTarget)
        #end if
            
        pg.display.flip()

        return
    #end render

    def tick(self):
        self.frameTimeDelta = pg.time.get_ticks() - self.lastFrameTick

        while self.frameTimeDelta < self.frameTimer:
            self.frameTimeDelta = pg.time.get_ticks() - self.lastFrameTick
        #end while

        self.lastFrameTick = pg.time.get_ticks()

        if self.onTick != None:
            self.onTick(self, self.frameTimeDelta)
        #end if
            
        for state in self.states:
            if state.onTick != None:
                state.onTick(state, self.frameTimeDelta)
            #end if
                
            for entity in state.entities:
                if entity.onTick != None:
                    entity.onTick(entity, self.frameTimeDelta)
                #end if
            #end for
        #end for

        return
    #end tick

    def run(self):
        try:
            if self.onStart != None:
                self.onStart()
            #end if
            
            while self.active == True:
                self.tick()
                self.handleEvents()
                self.update()
                self.render(self.display)
            #end while
                
            if self.onQuit() != None:
                self.onQuit()
            #end if
        except Exception as e:
            print(e)
        #end try

        return
    #end run
    
    def pushState(self, state):
        self.states.append(state)
        
        self.states[-1].enter()
        
        if state.onEnter != None:
            state.onEnter(state)
        #end if
        
        return
    #end pushState
    
    def popState(self, index):
        state = self.states.pop(index)
        state.exit()
        
        if state.onExit != None:
            state.onExit(state)
        #end if
        
        return
    #end popState
#end Game
