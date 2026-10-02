--------------------------------------------------------------------------------
	Simple Game Engine (SGE)
--------------------------------------------------------------------------------

	Simple Game Engine (SGE) is a lightweight and robust framework that allows 
	the user to quickly, and easily make games using the Pygame 2.6 Library. 
	Since SGE is more of a framework than a game engine, the user must be
	familiar with at least basic knowledge of how to use Pygame. This document
	does not cover any material regarding Pygame or its interworkings.
	
	SGE has also been ported to several other languages with different API's
	for general inputs and outputs. The C version of SGE uses the SDL2 library
	as a base, and the Javascript version of SGE has no base and uses pure 
	Javascript.
	
	This document is intended to inform the user of everything included in SGE,
	define data, go over assumptions and pitfalls, and offer a tutorial on how
	to use SGE.

--------------------------------------------------------------------------------
	Contents
--------------------------------------------------------------------------------

	Simple Game Engine has 3 user-defined classes: Entity, State, and Game.
	Entity is the base class for both State and Game and contains general data
	and methods related to graphics, movement, and inputs. Below is the full
	list of contents inside SGE and descriptions of each.
	
	> Global Constants:
		* COLLIDEMODE_RECT : Assigned to Entities' "collideMode" variable; 
			Indicates that collisions between Entities will be calculated
			from the Entities' "collideRec"t variable.
			
		* COLLIDEMODE_RADIUS : Assigned to Entities' "collideMode" variable; 
			Indicates that collisions between Entities will be calculated
			from the Entities' "collideRadius" variable.
			
		* RENDERMODE_NATIVE : Assigned to Entities' "renderMode" variable; 
			Indicates that Entities will be drawn onto a render target at
			the size and position denoted by their "rect" variable.
			
		* RENDERMODE_STRETCH : Assigned to Entities' "renderMode" variable; 
			Indicates that Entities will be drawn onto a render target and
			scaled to fill the entire render target.
			
		* RENDERMODE_CENTER : Assigned to Entities' "renderMode" variable; 
			Indicates that Entities will be drawn onto the center of a 
			render target and retain the width and height of the
			Entities' "rect" variable.

		* COLOR_DEFAULT : Global configurable setting that determines the
			color that will fill the display when clearing the screen
			before each Game and State render. It is usually set to
			(0,0,0)
			
		* COLOR_TRANSPARENT : Gloabl configurable setting that determines
			which color will be fully transparent by default when loading
			images. It is usually set to (255,0,255)

		* DISP_W : Gloabl configurable setting that determines the width of
			the display window (or display Surface if you use full screen
			mode). It is set to 800 by default, but will get updated to
			whichever value is passed to the initSimpleGE function.
			
		* DISP_H : Gloabl configurable setting that determines the height of
			the display window (or display Surface if you use full screen
			mode). It is set to 600 by default, but will get updated to
			whichever value is passed to the initSimpleGE function.
			
		* DISP_FLAGS : Gloabl configurable setting that determines the flags
			the display window (or display Surface if you use full screen
			mode). It is set to 0 by default, but will get updated to
			whichever value is passed to the initSimpleGE function.
		
		* DISPLAY Global setting that should only be set once by the initSimpleGE
			function. Set to None by default and initialized to a Pygame Display
			with the DISP_W, DISP_H, and DISP_FLAGS values passed to initSimpleGE.
			
		* KEYSDOWN = Global setting that represents a list of the state of every
			keyboard key (False means not held down and True means held down).
			This variable is refreshed every frame by the Game object after
			polling and handling every Event in the event queue.
		
		* MOUSEDOWN = Global setting that represents a list of the state of every
			mouse button (False means not held down and True means held down).
			This variable is refreshed every frame by the Game object after
			polling and handling every Event in the event queue.
			
	> Global Functions
		
		* initSimpleGE(dispW, dispH, dispFlags, title) -> None : This global
			function initializes all Pygame systems and sets up the DISPLAY,
			DISP_W, DISP_H, DISP_FLAGS, KEYSDOWN, MOUSEDOWN, and JOYDOWN 
			variables.
			
			!NOTE! This function must be called before any SimpleGE objects are
			created. This ensures that all img data uses the same format and that
			Pygame is initialized.
			
			- "dispW" : Integer argument that determines the width of the display.
			
			- "dispH" : Integer argument that determines the height of the display.
			
			- "dispFlags" : Integer argument that holds the Pygame Display Flags
				for the display. Common flags would be FULLSCREEN and RESIZEABLE
			
			- "title" : String argument that sets the caption on the display
				window.
		
		* getInputStates() -> None : This function populates the KEYDOWN, MOUSEDOWN,
			and JOYDOWN variables with the current values of their respective
			inputs. This gets called once per frame by a Game object.
			
--------------------------------------------------------------------------------
		
	> Entity:
		~~Description~~
		
		This is the base class for all other classes within SGE. It contains
		member variables to hold size, position, image data, and event handling 
		functions.
		
		~~Data Elements~~
		
		//Position and Size
		
		* x : Float member variable that denotes the x position of the Entity.
        	
        * y : Float member variable that denotes the y position of the Entity.
        
        * w : Float member variable that denotes the width of the Entity.
        	
        * h : Float member variable that denotes the height of the Entity.
        
        //Movement
        
        * dx : Float member variable that denotes the x velocity of the Entity.
        
        * dy : Float member variable that denotes the y velocity of the Entity.
        
        * ddx : Float member variable that denotes the x acceleration of the 
        	Entity.
        
        * ddy : Float member variable that denotes the y acceleration of the 
        	Entity.
        	
        //Image Data
        
        * img : Pygame Surface member variable that holds the image data
        	that will get rendered to a render target inside the Entity's
        	render function.
        	
        * renderMode : Integer member variable that controls how the Entity
        	will be rendered onto a render target.
        	
        * clipRect : Pygame Rect member variable that holds the size and
        	location of the Entity's image clipping area. This is the portion
        	of the img data that will get rendered.
        	
        //Collision Boundaries
        
        * hitRect : Pygame Rect member variable that holds the size and
        	location of the Entity's collision boundaries.
        	
        * hitOffsX : Float member variable that determines the hitRect x offset
        	relative to the Entity's position. This determines the top left corner
        	of hitRect and gets updated each frame.
        
        * hitOffsY : Float member variable that determines the hitRect y offset
        	relative to the Entity's position. This determines the top left corner
        	of hitRect and gets updated each frame.
        	
        * hitR : Float member variable that holds the radius of the
        	Entity's collision boundaries.
        	
        * collideMode : Booles member variable that controls how the Entity
        	will collide with other Entities.
        	
        //Status
        
        * getsTick : Boolean member variable that indicates whether or not
			the Entity will try to call its onTick Callback Function each
			frame.
		
		* getsInput : Boolean member variable that indicates whether or not
			the Entity will handle input events (keyboard events, mouse 
			events, or joystick events)
		
		* getsKeyboardInput : Boolean member variable that indicates whether or not
			the Entity will receive and handle keyboard inputs.
        
        * getsMouseInput : Boolean member variable that indicates whether or not
			the Entity will receive and handle mouse inputs.
        
        * getsJoystickInput : Boolean member variable that indicates whether or not
			the Entity will receive and handle joystick inputs.
		
		* getsUpdate : Boolean member variable that indicates whether or not
			the Entity will get updated inside its "update" function.
			
        * getsRender : Boolean member variable that indicates whether or not
			the Entity will get rendered inside its "render" function.
			
        * getsCollision : Boolean member variable that indicates whether or not
			the Entity can collide with other Entities.
			
        * debug : Boolean member variable that indicates whether or not
			to show the bounding box around the Entities' "rect" and 
			"collideRect" Rects.
			
		* lastTick : Int member variable that indicates the timestamp of the last
			tick.
        
        ~~Callback Functions~~
        
        * onTick(target, dt) : Reference to a function that gets called when the 
        	Entity "ticks". A "tick" happens on a fixed interval to sync the 
        	game to a framerate.
        	
        	- "target" is the Entity that gets passed in to the onTick function.
        	
        	- "dt" is the Float that gets passed in to the onTick function and 
        	denotes the time since the last "tick".
        	
        * onUpdate(target) : Reference to a function that gets called when the 
        	Entity's "update" function is called.
        	
        	- "target" is the Entity that gets passed in to the onUpdate function.
        	
        * onRender(target, renderTarget) : Reference to a function that gets called when the 
        	Entity's "render" function is called.
        	
        	- "target" is the Entity that gets passed in to the onRender function.
        	
        	- "renderTarget" : Pygame Surface argument that denotes the Surface
    			onto which the Entity will get rendered.
    			
    	* onCollide(target, other) : Reference to a function that gets called when the
    		Entity's "collide" function is called.
    		
    		- "target" is the Entity that gets passed in to the onCollide function.
    		
    		- "other" is the Entity that gets passed in to the onCollide function.

        * onKeyPressed(target, key) : Reference to a function that gets called 
        	when a Pygame KEYDOWN Event is posted.
        	
        	- "target" is the Entity that gets passed in to the onKeyPressed 
        	function.
        	
        	- "key" is the Integer that gets passed in to the onKeyPressed 
        	function and denotes the Pygame Key Value of the key that was 
        	pressed this frame.
        	
        * onKeyReleased(target, key) : Reference to a function that gets called 
        	when a Pygame KEYUP Event is posted.
        	
        	- "target" is the Entity that gets passed in to the onKeyReleased 
        	function.
        	
        	- "key" is the Integer that gets passed in to the onKeyReleased 
        	function and denotes the Pygame Key Value of the key that was 
        	released this frame.

        * onMouseButtonPressed(target, button) : Reference to a function that 
        	gets called when a Pygame MOUSEDOWN Event is posted.
        	
        	- "target" is the Entity that gets passed in to the 
        	onMouseButtonPressed function.
        	
        	- "button" is the Integer that gets passed in to the 
        	onMouseButtonPressed function and denotes the Pygame Mouse Button 
        	Value of the key that was pressed this frame.
        	
        * onMouseButtonReleased(target, button) : Reference to a function that 
        	gets called when a Pygame MOUSEUP Event is posted.
        	
        	- "target" is the Entity that gets passed in to the 
        	onMouseButtonReleased function.
        	
        	- "button" is the Integer that gets passed in to the 
        	onMouseButtonReleased function and denotes the Pygame Mouse Button 
        	Value of the key that was released this frame.

        * onMouseMotion(target, (x, y)) : Reference to a function that gets 
        	called when a Pygame MOUSEMOTION Event is posted.
        	
        	- "target" is the Entity that gets passed in to the onMouseMotion 
        	function.
        	
        	- "x" is the Integer that gets passed in to the onMouseMotion 
        	function and denotes the new x position of the mouse cursor relative 
        	to the display.
        	
        	- "y" is the Integer that gets passed in to the onMouseMotion 
        	function and denotes the new y position of the mouse cursor relative 
        	to the display.
        	
        * onMouseWheel(target, (x, y)) : Reference to a function that gets 
        	called when a Pygame MOUSEWHEEL Event is posted.
        	
        	- "target" is the Entity that gets passed in to the onMouseWheel 
        	function.
        	
        	- "x" is the Integer that gets passed in to the onMouseWheel 
        	function and denotes the new x displacement of the mouse wheel 
        	(usually it's 0).
        	
        	- "y" is the Integer that gets passed in to the onMouseWheel 
        	function and denotes the new y displacement of the mouse wheel.

        * onJoyButtonPressed(target, joystickID, button) : Reference to a 
        	function that gets called when a Pygame JOYBUTTONDOWN Event is 
        	posted.
        	
        	- "target" is the Entity that gets passed in to the 
        	onJoyButtonPressed function.
        	
        	- "joystickID" is the Integer that gets passed in to the 
        	onJoyButtonPressed function and denotes the Pygame JoyStick ID that 
        	posted the event.
        	
        	- "button" is the Integer that gets passed in to the 
        	onJoyButtonPressed function and denotes the Pygame Joy Button Value 
        	of the button that was pressed this frame.
        	
        * onJoyButtonReleased(target, joystickID, button) : Reference to a 
        	function that gets called when a Pygame JOYBUTTONUP Event is posted.
        	
        	- "target" is the Entity that gets passed in to the 
        	onJoyButtonReleased function.
        	
        	- "joystickID" is the Integer that gets passed in to the 
        	onJoyButtonReleased function and denotes the Pygame JoyStick ID that 
        	posted the event.
        	
        	- "button" is the Integer that gets passed in to the 
        	onJoyButtonReleased function and denotes the Pygame Joy Button Value 
        	of the button that was released this frame.

        * onJoyAxisMotion(target, joystickID, axis, value) : Reference to a 
        	function that gets called when a Pygame JOYAXISMOTION Event is 
        	posted.
        	
        	- "target" is the Entity that gets passed in to the onJoyAxisMotion 
        	function.
        	
        	- "joystickID" is the Integer that gets passed in to the 
        	onJoyAxisMotion function and denotes the Pygame JoyStick ID that 
        	posted the event.
        	
        	- "axis" is the Integer that gets passed in to the onJoyAxisMotion 
        	function and denotes the ID of the axis that was moved.
        	
        	- "value" is the Float that gets passed in to the onJoyAxisMotion 
        	function and denotes the value of the axis that was moved.
        	
        * onJoyHatMotion(target, joystickID, hat, value) : Reference to a 
        	function that gets called when a Pygame onJoyHatMotion Event is 
        	posted.
        	
        	- "target" is the Entity that gets passed in to the onJoyHatMotion 
        	function.
        	
        	- "joystickID" is the Integer that gets passed in to the 
        	onJoyonJoyHatMotionAxisMotion function and denotes the Pygame 
        	JoyStick ID that posted the event.
        	
        	- "hat" is the Integer that gets passed in to the onJoyHatMotion 
        	function and denotes the ID of the hat that was moved.
        	
        	- "value" is the List that gets passed in to the onJoyHatMotion 
        	function and denotes the (x, y) value of the hat that was moved.
        
		~~Methods~~
		
		* __init__(x, y, w, h, img) -> None : Constructor method; Creates a new 
			Entity Object and sets all the initial data values.
			
			- "x" : Float or Integer argument that denotes the Entity's x
				position.
				
			- "y" : Float or Integer argument that denotes the Entity's y
				position.
			
			- "w" : Integer argrument that denotes the width of the Entity.
			
			- "h" : Integer argument that denotes the height of the Entity.
			
			- "img" : Pygame Surface argument (or None) that holds the img
				data.
				
		* tick(dt) -> None : This method gets called at the start of every frame
			and calls the Entity's "onTick" callback function. This is useful
			for code that needs to be run at given time intervals and before
			inputs are handled and the Entity updates.
			
			- "dt" : Integer argument that denotes the time in milliseconds since
				the last tick.
	
    	* handleEvent(event) -> None : Handles the Events that Pygame posts to 
    		the event queue. Specifically, this method handles keyboard, mouse, 
    		joystick, and quitting events
    		
    		- "event" : Pygame Event argument that gets passed to the 
    			handleEvent method by a Game object.
	
    	* update() -> None : This method updates the Entity's position and 
    		collision boundaries.
	
    	* render(renderTarget) -> None : This method renders the Entity's "img" 
    		variable to a render target according to the render mode denoted in 
    		the "renderMode" variable.
    		
    		- "renderTarget" : Pygame Surface argument that denotes the Surface
    			onto which the Entity will get rendered.
    	
    	* debugRect(renderTarget) -> None : This method draws rectangles around 
    		the Entity's image Rect and collision boundaries.
    		
    		- "renderTarget" : Pygame Surface argument that denotes the Surface
    			onto which the debug boundaries will get rendered.
	
    	* collide(other) -> bool : This method returns a boolean value that 
    		denotes if this Entity is colliding with an other Entity according 
    		to the collide mode denoted in the "collideMode" variable.
    		
    		- "other" : Entity argument that denotes the Entity that this Entity
    			is checking collision with.

--------------------------------------------------------------------------------
		
	> State:
	
		~~Description~~
		
		This class extends the Entity class. It adds optional function pointers 
		to handle when the State is entered and exited. It also adds a list of
		Entities that will get updated and rendered automatically by the State.
		
		~~Data~~
		
		* entities : List member variable that holds a collection of Entities 
		that will get automatically updated and rendered by this State object.
		
		* exitCode: Int member variable that is intended to signal to a Game
		object that this State should exit and denote an ID for a new State that
		the Game should enter.
		
		~~Callback Functions~~
		
		* onEnter(target) : Reference to a function that gets called when the 
        	State gets entered
        	
        	- "target" is the State that gets passed in to the onEnter 
        		function.

		* onExit(target) : Reference to a function that gets called when the 
        	State gets exited
        	
        	- "target" is the State that gets passed in to the onExit 
        		function.
        		
        ~~Methods~~
		
		* __init__(x,y,w,h) -> None : Constructor method; Creates a new 
			State Object and sets all the initial data values. The parent
			Entity constructor is also called with these same arguments.
			
			- "x" : Float or Integer argument that denotes the State's x
				position.
				
			- "y" : Float or Integer argument that denotes the State's y
				position.
			
			- "w" : Integer argrument that denotes the width of the State.
			
			- "h" : Integer argument that denotes the height of the State.
			
		* tick(dt) -> None :  This method calls the parent Entity tick method
    		and it calls the tick method for every Entity in the State's 
    		"entities" variable.
    		
    		- "dt" : Integer argument that denotes the time in milliseconds since
				the last tick.
				
		* handleInput(event) -> None :  This method calls the parent Entity 
			handleInput method and it calls the handleInput method for every 
			Entity in the State's "entities" variable.
    		
    		- "event" : Pygame Event argument that gets passed to the 
    			handleInput method by a Game object.
    
    	* update() -> None : This method calls the parent Entity update method
    		and it calls the update method for every Entity in the State's 
    		"entities" variable.
    		
    	* checkCollisions() -> None : This method calls the "collide" method
    		for every pair of Entities in the State's "entities" variable.
    	
    	* render(renderTarget) -> None : This method calls the parent Entity 
    		update method and it calls the update method for every Entity in the 
    		State's "entities" variable.
    		
    		- "renderTarget" : Pygame Surface argument that denotes the Surface
    			onto which the State will get rendered.
    	
    	* enter() -> None : This method sets the State's status variables ("getsTick", 
    		"getsInput", "getsKeyboardInput", "getsMouseInput", "getsJoystickInput", 
    		"getsUpdate", "getsRender", "getsCollision") to True. If the State has a 
    		function in its "onEnter" variable, that function is called.
    	
    	* exit() -> None : This method sets the State's status variables ("getsTick", 
    		"getsInput", "getsKeyboardInput", "getsMouseInput", "getsJoystickInput", 
    		"getsUpdate", "getsRender", "getsCollision") to False. If the State has a 
    		function in its "onExit" variable, that function is called.

--------------------------------------------------------------------------------
		
	> Game:

		~~Description~~
		
		This class extends the Entity class. It adds optional function pointers 
		to handle when the Game is started and quit. It also adds a list of
		States that will get updated and rendered automatically by the Game. The 
		Game will initialize the Pygame library, set up a display, hold keyboard 
		and mouse data, and manage which states need to be entered and exited.
		
		~~Data~~

        * frameTimer : FLoat member variable that denotes the number of 
        	milliseconds between each frame.
        
        * frameDt: Float member variable that denotes the running total 
        	milliseonds since the last frame. When this number equals or passes 
        	the "frameTimer" value, it is reset to 0 and starts counting again.

        * states : List member variable that holds all of the states that the 
        	Game can access.
        	
        * running : Boolean member variable that denotes whether or not the Game
        	is running.
        
        ~~Callback Functions~~
        
        * onKeysDown(target, keys) : Reference to a function that gets called 
        	every frame. The KEYSDOWN variable is passed in automatically.
        	
        	- "target" is the Game that gets passed in to the onKeysDown 
        	function.
        	
        	- "keys" is the List that gets passed in to the onKeysDown function
        	and denotes the Pygame Key Values of the keys that are currently 
        	held down.
        	
        * onMouseButtonsDown(target, buttons) : Reference to a function that 
        	gets called every frame. The MOUSEDOWN variable is passed in 
        	automatically.
        	
        	- "target" is the Game that gets passed in to the 
        	onMouseButtonsDown function.
        	
        	- "buttons" is the List that gets passed in to the 
        	onMouseButtonsDown function and denotes the Pygame Button Values of the 
        	mouse buttons that are currently held down.
        	
        * onJoyDeviceAdded(target) : Reference to a function that gets called when
        	a Pygame Joystick device is plugged into the machine.
        	
        	- "target" is the Game that gets passed in to the 
        	onJoyDeviceAdded function.
        
        * onJoyDeviceRemoved(target) : Reference to a function that gets called when
        	a Pygame Joystick device is unplugged from the machine.
        	
        	- "target" is the Game that gets passed in to the 
        	onJoyDeviceRemoved function.
        	
        * onJoyButtonsDown(target, joystickID, buttons) : Reference to a function that 
        	gets called every frame. The JOYDOWN variable is passed in 
        	automatically.
        	
        	- "target" is the Game that gets passed in to the 
        	onJoyButtonsDown function.
        	
        	- "joystickID" : Integer argument that denotes the ID of the Joystick
        	
        	- "buttons" is the List that gets passed in to the 
        	onJoyButtonDown function and denotes the joystick Button Values of the 
        	joystick buttons that are currently held down.
        
        * onStart(target) : Reference to a function that gets called once when the Game's
        	"run" method gets called.
        	
        	- "target" is the Game that gets passed in to the onKeysDown 
        	function.
        
        * onQuit(target) : Reference to a function that gets called once when the Game's
        	"run" method exits (AKA when the "running" variable gets set to False).
        	
        	- "target" is the Game that gets passed in to the onKeysDown 
        	function.
        
        ~~Methods~~
        
        * __init__(x, y, w, h) -> None : Constructor method; Creates a new 
			Game Object and sets all the initial data values. The parent
			Entity constructor is also called with these same arguments.
			
			- "x" : Float or Integer argument that denotes the State's x
				position.
				
			- "y" : Float or Integer argument that denotes the State's y
				position.
			
			- "w" : Integer argrument that denotes the width of the State.
			
			- "h" : Integer argument that denotes the height of the State.
    	
    	* tick(dt) -> None :  This method calls the parent Entity tick method
    		and it calls the tick method for every State in the Game's 
    		"states" variable.
    		
    		- "dt" : Integer argument that denotes the time in milliseconds since
				the last tick.
	
    	* handleInput(event) -> None :  This method calls the parent Entity 
			handleInput method and it calls the handleInput method for every 
			State in the Games's "states" variable.
    		
    		- "event" : Pygame Event argument that gets passed to the 
    			handleInput method by a Game object.
	
    	* update() -> None : This method calls the parent Entity update method
    		and it calls the update method for every State in the Game's 
    		"states" variable.
	
    	* render(renderTarget) -> None : This method calls the parent Entity 
    		render method and it calls the update method for every State in the 
    		Games's "states" variable.
    		
    		- "renderTarget" : Pygame Surface argument that denotes the Surface
    			onto which the Game will get rendered.
	
    	* run() -> None : TBD
    	
    	* pushState(state) -> None : This method pushes a State object onto the Game's
    		"states" list and calls the "enter" function of that state.
    		
    		- "state" : State argument that references the state to be added
    	
    	* popState(index) -> None : This method pops a State object off of the Game's
    		"states" list and calls the "exit" function of that state.
    		
    		- "state" : Interger argument that denotes the index of the state 
    			to be removed
