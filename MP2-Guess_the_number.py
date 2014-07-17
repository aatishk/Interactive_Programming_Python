# http://www.codeskulptor.org/#user36_tDxcAchpmc_2.py

# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

""" User comments as docstrings """
# Comments provided in the template 

""" Importing relevant modules """
import random
import simplegui
import math

# initialize global variables used in your code
""" Default range is [0,100) """
num_range = 100

# helper function to start and restart the game
def new_game():
    """Global variables for storing computer guess and count of user guesses """ 
    global computer_guess
    global count_user_guesses
    
    """ Generate computer guess (min is not needed. It's by default 0.) """
    computer_guess = random.randrange(num_range)
    
    """ Generate max guesses allowed. 2^n => max-min+1 """
    count_user_guesses = int(math.ceil(math.log(num_range,2)))

    """ Print Welcome Message and Maximum Guesses Info """
    print "**** New Game ****" 
    print 
    print "Range is from 0 to", num_range
    print "You have to find the number in", count_user_guesses,"guesses"
    print
    
# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    global num_range

    num_range = 100
    new_game()
    
def range1000():
    # button that changes range to range [0,1000) and restarts
    global num_range

    num_range = 1000
    new_game()
    
def input_guess(guess):    
    # main game logic goes here
    global count_user_guesses
    
    """ Convert from string to integer """
    user_guess = int(guess)
    print " ++ You guessed", user_guess,"++"
        
    """ Check for match """
    if (count_user_guesses > 0):      
        
        if (user_guess == computer_guess):
            print "You guessed correctly :) CONGRATS"
            print
            """ Start new game """
            new_game()            
        
        elif (user_guess > computer_guess):
            print "You guessed incorrectly :( Guess LOWER"
            """ Decrement the number of guesses still left """
            count_user_guesses -= 1
            print "Number of remaining guesses is", count_user_guesses   
            print
        
        else:
            print "You guessed incorrectly :( Guess HIGHER"
            """ Decrement the number of guesses still left """
            count_user_guesses -= 1
            print "Number of remaining guesses is", count_user_guesses   
            print
    
    """ No more guesses left. Reveal the computer guess and start new game. """
    if (count_user_guesses == 0):
        print "Sorry :( No more guesses possible"
        print "The number was", computer_guess
        print
        print "Better luck next time!"
        print
        new_game()
    
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements
frame.add_button("Range is [0,100)", range100, 200)
frame.add_button("Range is [0,1000)", range1000, 200)
frame.add_input("Enter a guess (integer)", input_guess, 200)

# call new_game and start frame
new_game()
frame.start()

# always remember to check your completed program against the grading rubric
