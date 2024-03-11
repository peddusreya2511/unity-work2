import viz
import vizact
import vizinfo
import vizcam
import vizshape

viz.setMultiSample(4)
viz.fov(60)
viz.go()
viz.mouse(viz.ON)


#INTERACTIVE MODE 1
"""
This script demonstrates how to gather input from the user at startup.
"""
import viz
import vizact
import vizinput

viz.setMultiSample(4)
viz.fov(60)

# Start Vizard with a prompt dialog box
viz.go(viz.PROMPT)

import vizinfo
vizinfo.InfoPanel()

#Retrieve text from the prompt
speed = viz.get(viz.INITMESG)

#Ask user for name
name = vizinput.input('What is your name?')



#INTERACTIVE MODE 2

#=================Programming:(e)Part #3 :Add time counter or add score====================#

import viz
import vizact

viz.setMultiSample(4)
viz.fov(60)
viz.go()

# Define some constants
BALL_SPEED = 5  # The speed of the ball when it is shot (meters/sec)

#Add info panel for displaying score
scorePanel = vizinfo.InfoPanel('Score: 0', icon=False,align=viz.ALIGN_RIGHT_BOTTOM)
scorePanel.score = 0

# Lists that hold the balls and ducks
balls = []

# Beginning duck position
duckBeginPos = [-7, 0, -5]

# Enable physics, but don't use gravity
viz.phys.enable()
viz.phys.setGravity([0, 0, 0])

# Create duck
duck = viz.addAvatar('duck.cfg', pos=duckBeginPos)

# Enable collisions with the duck based on its mesh
duck.collideMesh()
duck.disable(viz.DYNAMICS)

# Create the walk action for the duck
duck_walk_action = vizact.sequence(
    vizact.method.setPosition(duckBeginPos),
    vizact.method.setEuler([-90, 0, 0]),
    vizact.walkTo([-10, 0, 13.5], walkSpeed=1, turnSpeed=0, walkAnim=1)
)

# Start the duck
duck.runAction(duck_walk_action)

# Initialize the ball
ball = viz.addChild('beachball.osgb', pos=(0, 0, -40), flags=viz.CACHE_CLONE)

# Enable collisions with the ball based on a sphere shape
ball.collideSphere()

# We want to be notified of the ball's collisions
ball.enable(viz.COLLIDE_NOTIFY)

# Initialize click count
click_count = 0

# Shoot a ball on double-click
def shootBall(button):
    global click_count  # Use global variable

    if button == viz.MOUSEBUTTON_LEFT:
        # Increment click count on each left mouse button press
        click_count += 1

        # Shoot the ball on double-click
        if click_count == 3:
            # Calculate the vector of the ball based on the mouse position
            line = viz.MainWindow.screenToWorld(viz.mouse.getPosition())
            line.length = BALL_SPEED

            # Set the position of the ball to the calculated position
            ball.setPosition(line.begin)

            # Reset click count
            click_count = 0

            # Reset ball and set velocity
            ball.reset()
            ball.setVelocity(line.dir)

# Assign the shootBall function to handle mouse events for the left mouse button
viz.callback(viz.MOUSEBUTTON_EVENT, shootBall)


# Called when two objects collide in the physics simulator
def oncollide(e):
    if e.obj2 == duck:
        # Play the duck hit animation
        duck.execute(2)
        # Play quack sound
        viz.playSound('quack.wav')
        # Play ball bounce sound
    viz.playSound('bounce.wav')

viz.callback(viz.COLLIDE_BEGIN_EVENT, oncollide)

# Make sure balls maintain constant velocity
def updateVelocity():
    ball.setVelocity(viz.Vector(ball.getVelocity(), length=BALL_SPEED))

vizact.ontimer(0, updateVelocity)

# Move the head position back
viz.MainView.move([0, 0, -7])

# Preload sound files
viz.playSound('gunshot.wav', viz.SOUND_PRELOAD)
viz.playSound('quack.wav', viz.SOUND_PRELOAD)
viz.playSound('bounce.wav', viz.SOUND_PRELOAD)

# Replace the court with your environment model
environment_model = viz.addChild('ground.osgb')

# Enable collisions for the environment model
environment_model.collideMesh()

#INTERACTIVE MODE 3

#Add object that vizinfo GUI objects will modify
wheelbarrow = viz.addChild('wheelbarrow.ive')
wheelbarrow.setPosition([-5,0,0])
wheelbarrow.setAxisAngle([0,1,0, -90])
#Initialize info box with some instructions
info = vizinfo.InfoPanel('Use the slider to spin the wheelbarrow.\nThe radio button changes the color.', align=viz.ALIGN_RIGHT_BOTTOM, icon=False)
info.setTitle( 'Wheelbarrow Spinner' ) #Set title text
info.addSeparator()

#Add slider in info box
slider = info.addLabelItem('Spin Speed', viz.addSlider())
slider.label.color(viz.RED)

#Add radio buttons
red = info.addLabelItem('Red', viz.addRadioButton('color'))
white = info.addLabelItem('White', viz.addRadioButton('color'))
blue = info.addLabelItem('Blue', viz.addRadioButton('color'))

#Set callbacks for changing wheelbarrow color with radio buttons
vizact.onbuttondown( red, wheelbarrow.color, viz.RED )
vizact.onbuttondown( white, wheelbarrow.color, viz.WHITE )
vizact.onbuttondown( blue, wheelbarrow.color, viz.BLUE )

#Keyboard commands that modify the info box
vizact.onkeydown(' ', info.setPanelVisible, viz.TOGGLE)

def changeMessage():
	info.setText( vizinput.input('Enter info text:') ) #Change directions message

vizact.onkeydown('m', changeMessage)

def changeTitle():
	info.setTitle( vizinput.input('Enter title text:') ) #Change title message

vizact.onkeydown('t', changeTitle)


def SetSpinSpeed(pos):
	#Make wheelbarrow spin according to slider position
	wheelbarrow.runAction( vizact.spin(0, -1, 0, 500 * pos) )

vizact.onslider( slider, SetSpinSpeed )

# interaction 4


## translation
"""
This script will demonstrate how to manually animate an object using timers.
"""
import viz
import vizact
import math

viz.setMultiSample(4)
viz.fov(60)
viz.go()

import vizinfo
vizinfo.InfoPanel()

#The speed of the timer.  A value of 0 means the timer function
#Will be called every frame
UPDATE_RATE = 0

#The speed of the translation
SPEED = 50.0

#A variable to hold the angle
angle = 0

#Add a model to rotate
h = viz.addChild('tut_hedra.wrl')

#Place the model in front of the viewer
h.setPosition([2,2,8])

def moveModel():
	global angle

	#Increment the angle based on elapsed time
	angle = angle + (SPEED * viz.elapsed())

	#Set the height of the object to double the sine of the angle
	height = math.sin(viz.radians(angle)) * 2.0

	#Update the models rotation
	h.setEuler([angle,0,0])

	#Translate the object
	h.setPosition([0,height,15])

#setup a timer and specify it's rate and the function to call
vizact.ontimer(UPDATE_RATE, moveModel)


## timer visibikity another case
# timer, visibility
ground=viz.addChild('ground.osgb')
#Make it invisible.
h.visible( viz.OFF )
def onKeyDown(key):
#If the key that was pressed is the
#a key, then make the lab visible.
	if key == 'l':
		h.visible( viz.ON )
#Issue a callback for keyboard events.
#When those events occur, call the
#onKeyDown function.
viz.callback(viz.KEYDOWN_EVENT,onKeyDown)
vizact.onkeydown( 'l', h.visible, viz.ON )
vizact.onkeydown( 'o', h.visible, viz.OFF )
vizact.ontimer2( 1, 0, h.visible, viz.ON )



#INTERACTIVE MODE 4
"""
#=================Programming:(e)Part #8 : Graphical user interface #====================
Graphical user interface
This script demonstrates how to use animation paths
The 4 transparent balls represent the control points
The rest of the animation is done by Vizard
Use the on screen controls to change certain options
Press spacebar to restart the path
"""


#Move the viewpoint back
viz.MainView.move([0,0,0])

#Create the animation path
path = viz.addAnimationPath()

#Add the other colliding object
ball1 = viz.addChild( 'beachball.osgb' )

#Initialize an array of control points
positions = [ [4,0.50,3], [6,0.50,1], [4,0.50,-1], [2,0.50,1] ]

for x,pos in enumerate(positions):
	#Add a ball at each control point and make it
	#semi-transparent, so the user can see where the
	#control points are
	b = viz.addChild('beachball.osgb',flags=viz.CACHE_CLONE)
	b.setPosition(pos)
	b.alpha(0.2)
	#Add the control point to the animation path
	#at the new time
	path.addControlPoint(x+1,pos=pos)

#Set the initial loop mode to circular
path.setLoopMode(viz.CIRCULAR)

#Automatically compute tangent vectors for cubic bezier translations
path.computeTangents()

#Automatically rotate the path
path.setAutoRotate(viz.ON)

#Link the ball to the path
viz.link(path, ball1)

#Play the animation path
path.play()

#Setup path control panel
controlPanel1 = vizinfo.InfoPanel(text=None, title='Settings', align=viz.ALIGN_CENTER_BOTTOM ,icon=False)

slider_speed = controlPanel1.addLabelItem('Speed', viz.addSlider())
slider_speed.set(0.1)

controlPanel1.addSection('Loop Mode')
radio_loop_off = controlPanel1.addLabelItem('Off', viz.addRadioButton('LoopMode'))
radio_loop_on = controlPanel1.addLabelItem('Loop', viz.addRadioButton('LoopMode'))
radio_loop_swing = controlPanel1.addLabelItem('Swing', viz.addRadioButton('LoopMode'))
radio_loop_circular = controlPanel1.addLabelItem('Circular', viz.addRadioButton('LoopMode'))
radio_loop_circular.set(1)

controlPanel1.addSection('Interpolation Mode')
radio_interp_linear = controlPanel1.addLabelItem('Linear', viz.addRadioButton('InterpolationMode'))
radio_interp_cubic = controlPanel1.addLabelItem('Bezier', viz.addRadioButton('InterpolationMode'))
radio_interp_linear.set(1)

def changeSpeed(pos):
	#Adjust the speed of the animation path
	path.setSpeed(pos*10)

#Setup callbacks for slider events
vizact.onslider(slider_speed, changeSpeed)

#Setup button click events
vizact.onbuttondown(radio_loop_off,path.setLoopMode,viz.OFF)
vizact.onbuttondown(radio_loop_on,path.setLoopMode,viz.LOOP)
vizact.onbuttondown(radio_loop_swing,path.setLoopMode,viz.SWING)
vizact.onbuttondown(radio_loop_circular,path.setLoopMode,viz.CIRCULAR)
vizact.onbuttondown(radio_interp_linear,path.setTranslateMode,viz.LINEAR_INTERP)
vizact.onbuttondown(radio_interp_cubic,path.setTranslateMode,viz.CUBIC_BEZIER)

# Reset path
vizact.onkeydown(' ', path.reset)


#=================Programming:(e)Part #2 :ADDING AVATARS ====================#
#ADDING AVATARS
size =[0.8,0.8,0.8]
posX = 10
posY = 0
posZ = -15
avatar1 = viz.addAvatar('vcc_male.cfg',pos=[posX,posY,posZ],euler=[0,0,0],scale= size)
avatar2 = viz.addAvatar('vcc_female.cfg',pos=[posX+2,posY,posZ],euler=[0,0,0],scale= size)
avatar3 = viz.addAvatar('vcc_female.cfg',pos=[posX+4,posY,posZ],euler=[0,0,0],scale= size)
avatar4 = viz.addAvatar('vcc_male.cfg',pos=[posX+6,posY,posZ],euler=[0,0,0],scale= size)
avatar5 = viz.addAvatar('vcc_male.cfg',pos=[posX+8,posY,posZ],euler=[0,0,0],scale= size)
avatar6 = viz.addAvatar('vcc_male.cfg',pos=[posX+10,posY,posZ],euler=[0,0,0],scale= size)	
avatar7 = viz.addAvatar('vcc_female.cfg',pos=[posX,posY,posZ+2],euler=[0,0,0],scale= size)
avatar8 = viz.addAvatar('vcc_female.cfg',pos=[posX,posY,posZ+4],euler=[0,0,0],scale= size)
avatar9 = viz.addAvatar('vcc_female.cfg',pos=[posX,posY,posZ+6],euler=[0,0,0],scale= size)
avatar10 = viz.addAvatar('vcc_female.cfg',pos=[posX,posY,posZ+8],euler=[0,0,0],scale= size)

a1,a2,a3,a4,a5,a6,a7,a8,a9,a10=avatar1,avatar2,avatar3,avatar4,avatar5,avatar6,avatar7,avatar8,avatar9,avatar10
vizact.onkeydown('1', a1.state, 1)
vizact.onkeydown('2', a2.state, 2)
vizact.onkeydown('3', a3.state, 3)
vizact.onkeydown('4', a4.state, 4)
vizact.onkeydown('5', a5.state, 5)
vizact.onkeydown('6', a6.state, 6)
vizact.onkeydown('7', a7.state, 7)
vizact.onkeydown('8', a8.state, 8)
vizact.onkeydown('9', a9.state, 15)
vizact.onkeydown('0', a10.state, 10)
vizact.onkeydown('a', a7.state, 11)
vizact.onkeydown('b', a8.state, 12)
vizact.onkeydown('c', a9.state, 13)
vizact.onkeydown('d', a10.state, 14)
vizact.onkeydown('e', a2.state, 15)
vizact.onkeydown('f', a1.stopAnimation, 2)

#=================Programming:(e)Part #4 :Add multiple windows====================#
import viz

viz.setMultiSample(4)
viz.fov(60)
viz.go()

ground = viz.addChild('ground.osgb')

BirdEyeWindow = viz.addWindow()
BirdEyeWindow.fov(60)
BirdEyeView = viz.addView()
BirdEyeWindow.setView(BirdEyeView)
BirdEyeView.setPosition([7,25,2])
BirdEyeView.setEuler([0,90,0])

RearWindow = viz.addWindow()
RearWindow.fov(60)
RearView = viz.addView()
RearWindow.setView(RearView)
RearWindow.setPosition([0,1])

#Make RearView look behind MainView
viewLink = viz.link(viz.MainView,RearView)
viewLink.preEuler([180, 0, 0]) #spin view backwards

#=================Programming:(e)Part #5 : add a sky with environment map #====================
sky = viz.add(viz.ENVIRONMENT_MAP,'sky.jpg')
skybox = viz.add('skydome.dlc')
skybox.texture(sky)

#-----add ground------#
ground = viz.addChild('ground.osgb')

#-----add greek temple------#
greek = viz.addChild('greektemple.osgb')
greek.setScale([.02,.02,.02])

#-----add assignment------#
lab = viz.addChild('Assignment2-Sreya.osgb')
lab.setScale([.5,.6,.5])

#2 :add and play an audio file====================

citySound = viz.addAudio('bach_air.mid')
citySound.play()
citySound.loop()
vizact.onkeydown( 'p', citySound.play )
vizact.onkeydown( 's', citySound.stop )

#=================Programming:(e)Part #6 : ANIMATING THE VIEW POINT #====================
"""
This script demonstrates how to animate the viewpoint
The keys 1-4 move the viewpoint to a different location
Try changing the rotation mode for interesting effects
"""
import viz
import vizact

viz.setMultiSample(4)
viz.fov(60)
viz.go()

import vizinfo
info = vizinfo.InfoPanel(align=viz.ALIGN_RIGHT_TOP)

# Create info panel for rotate mode
modePanel = vizinfo.InfoPanel('', title='Rotate Mode', align=viz.ALIGN_LEFT_BOTTOM, icon=False)
none = modePanel.addLabelItem('None',viz.addRadioButton('RotateMode'))
pivot = modePanel.addLabelItem('Pivot',viz.addRadioButton('RotateMode'))
blend = modePanel.addLabelItem('Blend',viz.addRadioButton('RotateMode'))
none.set(True)

#Add a ground plane
viz.addChild('ground.osgb')

#Set the background color
viz.clearcolor(viz.SLATE)

#Add the vizard logo
logo = viz.addChild('logo.ive')
logo.setPosition(4,0,-15)

#Set the animation speed and mode
SPEED = 2.5
MODE = viz.SPEED
ROTATE_MODE = viz.NO_ROTATE

def SetRotateMode(mode):
	global ROTATE_MODE
	ROTATE_MODE = mode

def AnimateView(pos):
	action = vizact.goto(pos,SPEED,MODE,pivot=(0,1,0),rotate_mode=ROTATE_MODE)
	viz.MainView.runAction(action)

#Setup keyboard events
vizact.onkeydown('w',AnimateView,[0,1,-3])
vizact.onkeydown('x',AnimateView,[3,0.1,0])
vizact.onkeydown('y',AnimateView,[0,1,3])
vizact.onkeydown('z',AnimateView,[-3,2,0])

#Setup button click events
vizact.onbuttondown(none,SetRotateMode,viz.NO_ROTATE)		#The viewpoint will not rotate while it's  moving
vizact.onbuttondown(pivot,SetRotateMode,viz.PIVOT_ROTATE)	#The viewpoint will look at the pivot point while it's moving
vizact.onbuttondown(blend,SetRotateMode,viz.BLEND_ROTATE)	#The viewpoint will blend to looking at the pivot point

#Start off by moving to the first location
AnimateView([0,1,-3])

#Increase  the  Field  of View
viz.MainWindow.fov(60)
viz.MainView.collision( viz.OFF )
Panel = vizinfo.InfoPanel('', title='Moving  the viewpoint to a different location', align=viz.ALIGN_CENTER_TOP, icon=False)
Panel.setText("Please use Keys: '1' to '9' or 'a','b','c','d' or 'e' to change state of avatar, use 'w','x','y','z' to animate the view point")

#Add 3D text
text3D = viz.addText3D('Our Community',pos=[0,4,4])
text3D.alignment(viz.ALIGN_CENTER_BOTTOM)
text3D.color(viz.GRAY)


import viz
import vizact
import vizinfo

viz.setMultiSample(8)
viz.fov(60)
viz.go()

vizinfo.InfoPanel()

viz.move([0,0,-5])

# Add piazza model 
model = viz.addChild('Assignment2-Sreya.osgb')

# Add piazza animations 
animations = viz.add('banner_animations.osgb')

vizact.onkeydown('1',animations.setAnimationState,viz.PAUSE,node='banner_sequence')
vizact.onkeydown('2',animations.setAnimationState,viz.PLAY,node='banner_sequence')
vizact.onkeydown('3',animations.setAnimationState,viz.PAUSE)
vizact.onkeydown('4',animations.setAnimationState,viz.PLAY)
vizact.onkeydown('5',animations.setAnimationSpeed,3.0,node='walk')

avatar = viz.addAvatar('vcc_male2.cfg')
avatar.setParent(animations,node='walk')
avatar.state(2)





