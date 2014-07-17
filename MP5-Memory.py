# http://www.codeskulptor.org/#user36_tDxcAchpmc_5.py
# simple state example for Memory

############################### INFO ####################################
# Buttons:																#
#																		#
# NEW GAME -> Start a fresh game [standard]								#
# REVEAL CARDS -> Reveal the set of cards .. cheating :) [extra]		#
# BACK TO GAME -> Get back to game once you saw the cards [extra]		#
#																		#
# Text:																	#
#																		#
# # Turns -> This tracks the number of turns already made [standard]	#
# # Completed -> This tracks the number of pairs found [extra]			#
#																		#
# Implementation stuff:													#
#																		#
# 1. The digits turn green when matching cards are exposed				#
# 2. Congratulatory message appears when all matching cards are found	#	
#########################################################################	

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
#import simplegui
import random

# Global state variables to track attempts, state of game and opened cards
# Initialize all with None to ensure that new_game does proper initliazation
turns = None
state = None
open_card1 = None
open_card2 = None
exposed = [None] * 16
perm_exposed = [None] * 16

# Set card height and width
height = 140
width = 50

# define event handlers

# Initialize the variables for new game
def new_game():
    # Setting up game state and cards
    global state, turns, cardset
    state = 0
    turns = 0
    cardset = range(8)
    cardset.extend(range(8))
    random.shuffle(cardset)
    
    # No exposed and open cards
    global exposed, perm_exposed, exposed_pair
    exposed = [False] * 16
    perm_exposed = [False] * 16
    open_card1 = None
    open_card2 = None
    
    frame.set_draw_handler(draw)
       
def mouse_click(pos):
    global state, turns, open_card1, open_card2
    # Get card from mouse click position
    card = pos[0]//width

    if state == 0:
        open_card1 = card
        exposed[open_card1] = True
        state = 1
        
    elif state == 1:
        # Test to check if clicked card is not already exposed to ignore spurious clicks
        if not exposed[card]:
            open_card2 = card
            exposed[open_card2] = True
            turns += 1
            state = 2
            
            # check if cards match and set the permanent exposed flags
            if cardset[open_card1] == cardset[open_card2]:
                perm_exposed[open_card1] = True
                perm_exposed[open_card2] = True
        
    else:
        # Test to check if clicked card is not already exposed to ignore spurious clicks
        if not exposed[card]:
            # Reset the cards if cards do not match
            if cardset[open_card1] != cardset[open_card2]:
                exposed[open_card1] = False
                exposed[open_card2] = False
                open_card1 = None
                open_card2 = None
                        
            # Reinitialize the last clicked card 
            open_card1 = card
            exposed[open_card1] = True
            state = 1	
                     
def draw(canvas):
    turns_label.set_text("# Turns = " + str(turns))
    perm_exposed_label.set_text("# Completed = " + str(sum(perm_exposed)/2)+"/8")    
    # Draw lines
    [canvas.draw_line([width*(i+1), 0], [width*(i+1), height], 2, "Yellow") for i in range(15)] 
    # Draw exposed cards
    for i in range(16):        
        if exposed[i]:
            canvas.draw_polygon([[width*i, 0], [width*(i+1), 0],[width*(i+1), height],\
                                 [width*i, height]], 2, "Red", "Black")
            canvas.draw_text(str(cardset[i]), [15 + width*i, 0.6*height], 40, "Yellow")
        if perm_exposed[i]:
            canvas.draw_text(str(cardset[i]), [15 + width*i, 0.6*height], 40, "Lime")
    
    # Draw congratulatory message once all matching cards are found
    if sum(perm_exposed) == 16:
        canvas.draw_polygon([[0, 0], [width*16, 0],[width*16, height], [0, height]], 2,\
                            "Red", "Black")
        canvas.draw_text("Good show! Completed in "+str(turns)+" turns!",\
                         [15 + width*2, 0.6*height], 40, "Yellow")

# Additional functions to handle the "reveal cards" feature
def reveal():
    frame.set_draw_handler(draw2)

def back():
    frame.set_draw_handler(draw)
    
def draw2(canvas):  
    # Draw lines
    [canvas.draw_line([width*(i+1), 0], [width*(i+1), height], 2, "Green") for i in range(15)] 
    # Draw all cards as if exposed
    for i in range(16):
        canvas.draw_polygon([[width*i, 0], [width*(i+1), 0],\
                             [width*(i+1), height], [width*i, height]], 2, "Red", "Green")
        canvas.draw_text(str(cardset[i]), [15 + width*i, 0.6*height], 40, "Yellow")
        
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 16*width, height)
frame.set_canvas_background("Teal")
 
# Button to restart the game
frame.add_button("NEW GAME", new_game, 150)

# Text to update # turns and # found cards
turns_label=frame.add_label("")
perm_exposed_label=frame.add_label("")

# Buttons to reveal all the cards [a bit of cheating :)] and back
frame.add_button("REVEAL CARDS", reveal, 150)
frame.add_button("BACK TO GAME", back, 150)

# register event handlers
frame.set_mouseclick_handler(mouse_click)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
