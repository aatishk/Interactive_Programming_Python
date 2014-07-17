# http://www.codeskulptor.org/#user36_tDxcAchpmc_3.py
# template for "Stopwatch: The Game"

# define global variables
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
#import simplegui

## Initialize all globals to zero ##
(time, pts, tries) = (0, 0, 0)

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D

## Helper function to format the time display ##
def format(t):
    BC  =  t // 1000
    D = (t % 1000) // 100
    A = BC // 60
    BC = BC % 60 
    
    if BC < 10:
        return str(A) + ":" + str(0) + str(BC) + "." + str(D)
    else:
        return str(A) + ":" + str(BC) + "." + str(D)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button_handler():
    timer.start()

def stop_button_handler():
    global time, pts, tries 
    
    if timer.is_running():
        timer.stop()
        ## Test if time is exactly a multiple of second ##
        if time % 1000 == 0:
            pts += 1
        tries += 1

def reset_button_handler():
    global time, pts, tries
    
    ## Reset all globals to zero ##
    (time, pts, tries) = (0, 0, 0)
    
    if timer.is_running():
        timer.stop()

def help_button_handler():
    print "***** Stopwatch Game *****"
    print
    print "Click START to begin the game"
    print
    print "You need to click STOP when it's a whole second"
    print "Whole second is X:01.0, X:02.0, X:03.0, etc."
    print
    print "You get a point if you manage to click STOP correctly"
    print "Points and Tries get updated with each click of STOP"
    print
    print "Click START to restart the game OR"
    print "Click RESET to start from scratch"
    print
    print "Have fun!!"
    print "***** End of help info *****"
    
# define event handler for timer with 0.1 sec interval
def timer_handler():
    global time
    if timer.is_running():
        time += 100 

# define draw handler
def draw_handler(canvas):
    global time, pts, tries
    
    canvas.draw_text(str(format(time)), [80,120], 40, "Yellow")
    canvas.draw_text(("Points/Tries"), [90, 30], 20, "White")
    canvas.draw_text((str(pts)+"/"+str(tries)), [130, 50], 20, "Orange")

# create frame
frame = simplegui.create_frame("StopWatch Game", 200, 150)
frame.set_canvas_background("Purple")

# create timer
timer = simplegui.create_timer(100, timer_handler)

# register event handlers
frame.add_button("START", start_button_handler, 100)
frame.add_button("STOP", stop_button_handler, 100)
frame.add_button("RESET", reset_button_handler, 100)
frame.add_button("HELP", help_button_handler, 100)
frame.set_draw_handler(draw_handler)

# start frame
frame.start()

# Please remember to review the grading rubric
