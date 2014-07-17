# http://www.codeskulptor.org/#user36_tDxcAchpmc_4.py

# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [300, 200]
    ball_vel = ["", ""]
    ball_vel[1] = -random.randrange(1, 3)
    if direction == RIGHT:
        ball_vel[0] = -random.randrange(2, 4)
    elif direction == LEFT:
        ball_vel[0] = random.randrange(2, 4)
    pass

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    # Resetting or initializing the scores etc.
    score1 = score2 = 0
    paddle1_pos = paddle2_pos = HEIGHT / 2
    paddle1_vel = paddle2_vel = 0
    
    # Toss to decide the starting direction
    left_or_right = random.randrange(0, 2)
    
    if left_or_right == 0:
        spawn_ball(True)
    elif left_or_right == 1:
        spawn_ball(False)   
    pass

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # Update positions of the paddles and ensure that they stay on canvas
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    
    if paddle1_pos < HALF_PAD_HEIGHT:
        paddle1_pos = HALF_PAD_HEIGHT
    elif paddle1_pos > HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
    
    if paddle2_pos < HALF_PAD_HEIGHT:
        paddle2_pos = HALF_PAD_HEIGHT
    elif paddle2_pos > HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
 
    # draw paddles
    pad1_x_value = HALF_PAD_WIDTH
    pad2_x_value = (WIDTH - HALF_PAD_WIDTH)
    
    canvas.draw_line([pad1_x_value, (paddle1_pos - HALF_PAD_HEIGHT)], \
                [pad1_x_value, (paddle1_pos + HALF_PAD_HEIGHT)], \
                PAD_WIDTH + 1, "White")
    canvas.draw_line([pad2_x_value, (paddle2_pos - HALF_PAD_HEIGHT)], \
                [pad2_x_value, (paddle2_pos + HALF_PAD_HEIGHT)], \
                PAD_WIDTH + 1, "White")

    # update ball and look for reflections
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    if (ball_pos[1] - BALL_RADIUS) == 0:
        ball_vel[1] = -ball_vel[1]
    elif (ball_pos[1] + BALL_RADIUS) == 400:
        ball_vel[1] = -ball_vel[1]
    
    # Checking if the ball hits the paddle 1 or 2
    if ball_pos[1] >= (paddle1_pos - HALF_PAD_HEIGHT) and \
    ball_pos[1] <= (paddle1_pos + HALF_PAD_HEIGHT):
        hit_pad1 = True
    else:
        hit_pad1 = False
        
    if ball_pos[1] >= (paddle2_pos - HALF_PAD_HEIGHT) and \
    ball_pos[1] <= (paddle2_pos + HALF_PAD_HEIGHT):
        hit_pad2 = True
    else:
        hit_pad2 = False 
            
    # Update ball
    if ball_pos[0] <= (PAD_WIDTH + BALL_RADIUS) and hit_pad1 == True:
        ball_vel[0] = (-ball_vel[0] * 1.1)
    elif ball_pos[0] >= (WIDTH - PAD_WIDTH - BALL_RADIUS) and hit_pad2 == True:
        ball_vel[0] = (-ball_vel[0] * 1.1)
    
    # Draw ball and scores
    canvas.draw_text("L : "+str(score1), (WIDTH * 0.4 - 50, HEIGHT * 0.5), 30, "Yellow")
    canvas.draw_text("R : "+str(score2), (WIDTH * 0.6 + 10, HEIGHT * 0.5), 30, "Yellow")
    canvas.draw_circle((ball_pos[0], ball_pos[1]), BALL_RADIUS, 1, "Black", "Red")
    
    # Update scores and reflect the ball
    if ball_pos[0] <= (PAD_WIDTH + BALL_RADIUS) and hit_pad1 == False:
        score2 += 1
        spawn_ball(False)
    elif ball_pos[0] >= (WIDTH - PAD_WIDTH - BALL_RADIUS) and hit_pad2 == False:
        score1 += 1
        spawn_ball(True)
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    # Paddle 1 update
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -10
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 10
    
    # Paddle 2 update
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = -10
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 10
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    # Paddle 1 update
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    
    # Paddle 2 update
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("RESTART", new_game, 100)

# start frame
new_game()
frame.start()
