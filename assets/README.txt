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
			
--------------------------------------------------------------------------------
		
	> Entity:
		~~Description~~
		
		This is the base class for all other classes within SGE. It contains
		member variables to hold size, position, image data, and event handling 
		functions.
		
		~~Data Elements~~
		
		* active : Boolean member variable that indicates whether or not
			the Entity will get updated inside its "update" function.
			
        * visible : Boolean member variable that indicates whether or not
			the Entity will get rendered inside its "render" function.
			
        * solid : Boolean member variable that indicates whether or not
			the Entity can collide with other Entities.
			
        * debug : Boolean member variable that indicates whether or not
			to show the bounding box around the Entities' "rect" and 
			"collideRect" Rects.
			
        * getsInput : Boolean member variable that indicates whether or not
			the Entity will handle input events (keyboard events, mouse 
			events, or joystick events)

        * img : Pygame Surface member variable that holds the image data
        	that will get rendered to a render target inside the Entity's
        	render function.
        	
        * rect : Pygame Rect member variable that hold the size and location
        	of the Entity.
        	
        	!!PITFALL!! Do not manipulate the "x" and "y" values inside the 
        	"rect" variable. These values are automatically assigned inside the 
        	update function from the Entity's "x" and "y" variables.
        	
        * renderMode : Integer member variable that controls how the Entity
        	will be rendered onto a render target.

        * collideRect : Pygame Rect member variable that holds the size and
        	location of the Entity's collision boundaries.
        	
        * collideRadius : Float member variable that holds the radius of the
        	Entity's collision boundaries.
        	
        * collideMode : Booles member variable that controls how the Entity
        	will collide with other Entities.

        * x : Float member variable that denotes the x position of the Entity.
        
        	!!NOTE!! This is a floating point number and it gets assigned to the
        	Integer "x" value inside the Entity's "rect" variable. This is
        	done to allow smooth, sub-pixel movement of Entities.
        	
        * y : Float member variable that denotes the y position of the Entity.
        
        	!!NOTE!! This is a floating point number and it gets assigned to the
        	Integer "y" value inside the Entity's "rect" variable. This is
        	done to allow smooth, sub-pixel movement of Entities.
        	
        * dx : Float member variable that denotes the x velocity of the Entity.
        
        * dy : Float member variable that denotes the y velocity of the Entity.
        
        * ddx : Float member variable that denotes the x acceleration of the 
        	Entity.
        
        * ddy : Float member variable that denotes the y acceleration of the 
        	Entity.
        
        ~~Optional Function References~~
        
        * onTick(target, dt) : Reference to a function that gets called when the 
        	Entity "ticks". A "tick" happens on a fixed interval to sync the 
        	game to a framerate.
        	
        	- "target" is the Entity that gets passed in to the onTick function.
        	
        	- "dt" is the Float that gets passed in to the onTick function and 
        	denotes the time since the last "tick".

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
        	
        * onKeysDown(target, keys) : Reference to a function that gets called 
        	every frame.
        	
        	- "target" is the Entity that gets passed in to the onKeysDown 
        	function.
        	
        	- "keys" is the List that gets passed in to the onKeysDown function
        	and denotes the Pygame Key Values of the keys that are currently 
        	held down.

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
        	
        * onMouseButtonsDown(target, buttons) : Reference to a function that 
        	gets called every frame.
        	
        	- "target" is the Entity that gets passed in to the 
        	onMouseButtonsDown function.
        	
        	- "buttons" is the List that gets passed in to the 
        	onMouseButtonsDown function and denotes the Pygame Key Values of the 
        	keys that are currently held down.

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
        	
        * onJoyButtonsDown : TBD

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

        * onJoyDeviceAdded : TBD
        * onJoyDeviceRemoved : TBD
        
		~~Methods~~
		
		* __init__(x, y, w, h) -> None : Constructor method; Creates a new 
			Entity Object and sets all the initial data values.
			
			- "x" : Float or Integer argument that denotes the Entity's x
				position.
				
			- "y" : Float or Integer argument that denotes the Entity's y
				position.
			
			- "w" : Integer argrument that denotes the width of the Entity.
			
			- "h" : Integer argument that denotes the height of the Entity.
	
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
		
		~~Optional Function References~~
		
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
    
    	* update() -> None : This method calls the parent Entity update method
    		and it calls the update method for every Entity in the State's 
    		"entities" variable.
    	
    	* render(renderTarget) -> None: This method calls the parent Entity 
    		update method and it calls the update method for every Entity in the 
    		State's "entities" variable.
    		
    		- "renderTarget" : Pygame Surface argument that denotes the Surface
    			onto which the State will get rendered.
    	
    	* enter() -> None : This method sets the State's "active", "visible",
    		"solid", and "getInput" variables to True. If the State has a 
    		function in its "onEnter" variable, that function is called.
    	
    	* exit() -> None : This method sets the State's "active", "visible",
    		"solid", and "getInput" variables to False. If the State has a 
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

		* display = Pygame Surface member variable that denotes the 
			window/display that the game will be rendered onto.

        * frameTimer : FLoat member variable that denotes the number of 
        	milliseconds between each frame.
        
        * frameTimeDelta: Float member variable that denotes the running total 
        	milliseonds since the last frame. When this number equals or passes 
        	the "frameTimer" value, it is reset to 0 and starts counting again.
        
        * lastFrameTick : Integer member variable that denotes the Pygame 
        	timestamp of the last frame.

        * keysDown : List member variable that denotes the collection of keys 
        	that are currently pressed down.
        
        * mouseButtonsDown : List member variable that denotes the collection of 
        	mouse buttons that are currently pressed down.
        
        * mousePos : List member variable that denotes the (x, y) position of 
        	the mouse cursor relative to the display.

        * states : List member variable that holds all of the states that the 
        	Game can access.
        
        ~~Optional Function References~~
        
        * onJoyDeviceAdded : TBD
        
        * onJoyDeviceRemoved : TBD
        
        * onStart : TBD
        
        * onQuit : TBD
        
        ~~Methods~~
        
        * __init__(self, title, dispW, dispH, resW, resH, flags) -> None : TBD

    	* __del__(self) -> None : TBD
	
    	* handleEvents(self) -> None : TBD
	
    	* update(self) -> None : TBD
	
    	* render(self, renderTarget) -> None : TBD
	
    	* tick(self) -> None : TBD
	
    	* run(self) -> None : TBD
    	
    	* pushState(self, state) -> None : TBD
    	
    	* popState(self, index) -> None : TBD
