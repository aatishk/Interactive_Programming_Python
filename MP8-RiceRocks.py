# http://www.codeskulptor.org/#user36_tDxcAchpmc_12.py

# implementation of Spaceship - program template for RiceRocks
import simplegui
import math
import random

################ R E A D M E ##########################
# 
# a. Help - At the bottom of start screen, player is provided information regarding the keys and their
#           functionality. Images of spacebar and arrow keys are also displayed for visual aid.
#        
# b. Lives - Depicted by three mini-ships. If a ship dies, the thrust turns off.
#            Number of ships with thrust indicates number of lives left.
#
# c. Score - The score of current game is generated via a tiled image of the digits.
#            (https://dl.dropboxusercontent.com/u/14495702/rice_rocks/red-digits-matrix-display-5391579.jpg)
#            Hopefully it makes the score nicer to look at :)
#
# d. Games - This keeps a count of the number of games played by the player once the game is launched.
#
# e. Highest - This displays the highest score by the player in the games played since the launch.
#
# f. Missiles - Thee kind of missiles are drawn (shot1, shot2 and shot3). When a missile is to be launched, 
#               one of three types is chosen using random.randrange function.
#
# g. Rocks - Three kinds of rocks are drawn (asteroid_blue, asteroid_brown and asteroid_blend). When a rock
#            is to be spawned, one of three types is chosen using random.randrange function. I found the rocks
#            to be large for the game canvas, so, they are displayed at 75% of the size, making the game roomier.
#
# h. Ship - The ship on the other hand seemed to be small at 100%. So, it's drawn at 125%.
#
# i. Collisions - Two kinds of collisions: 
#                 A. Ship-rock: Rock gets removed from canvas. Ship gets animated and flickers for 0.5 sec. It also
#                    stops moving.
#				  B. Missile-rock: There are three kind of rocks. Each kind of rock has its own corresponding 
#                    animation for explosion. 
#
####################### That's it.. Enjoy the game! #################

# 
# globals for user interface
WIDTH = 800
HEIGHT = 600
time = 0

score = 0
highest = 0
games = 0

coll_flag = False
show_ship_flag = True

def init_game():
    global lives, started, my_ship, rock_group, missile_group, explosion_group, show_ship_flag
    lives = 0
    started = False
    
    ship_info = ImageInfo([45, 45], [90, 90], 35)
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    rock_group = set()
    missile_group = set()
    explosion_group = set()
    
    if timer_rock_spawner.is_running:
        timer_rock_spawner.stop()

    if timer_ship_animate.is_running:
        timer_ship_animate.stop()
    
    soundtrack.pause()
    show_ship_flag = True

def start_game():
    global lives, score
    lives = 3
    score = 0    
    
    timer_rock_spawner.start()
    soundtrack.rewind()
    soundtrack.play()

# ImageInfo class
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated 

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# Digits image
digits_image = simplegui.load_image("https://dl.dropboxusercontent.com/u/14495702/rice_rocks/red-digits-matrix-display-5391579.jpg")

# keys image
space_image = simplegui.load_image("https://dl.dropboxusercontent.com/u/14495702/rice_rocks/space.png")
arrows_image = simplegui.load_image("https://dl.dropboxusercontent.com/u/14495702/rice_rocks/arrows.png")

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_images = []
missile_images.append(simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png"))
missile_images.append(simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png"))
missile_images.append(simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot3.png"))

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_images = []
asteroid_images.append(simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png"))
asteroid_images.append(simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_brown.png"))
asteroid_images.append(simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png"))

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_images = []
explosion_images.append(simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue.png"))
explosion_images.append(simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png"))
explosion_images.append(simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png"))

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .ogg by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.ogg")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.ogg")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.ogg")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.ogg")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)   

# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image_index = None
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, [self.image_size[0]*1.1, self.image_size[1]*1.1], self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, [self.image_size[0]*1.1, self.image_size[1]*1.1], self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        
        missile_image_index = random.randrange(len(missile_images))
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image_index,\
                                 missile_images[missile_image_index], missile_info, missile_sound))
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius   
    
    def get_image_index(self):
        return self.image_index
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image_index, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.image_index = image_index
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + self.age*self.image_size[0], self.image_center[1]],\
                              self.image_size, self.pos, [self.image_size[0]*0.75, self.image_size[1]*0.75], self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos,\
                              [self.image_size[0]*0.75, self.image_size[1]*0.75], self.angle)
            
    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH 
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # update age
        self.age += 1
        
        if self.age < self.lifespan:
            return False
        else:
            return True
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius

    def get_image_index(self):
        return self.image_index
    
    def collide(self, other_object):
        if dist(self.get_position(), other_object.get_position()) < (self.get_radius() + other_object.get_radius()):
            return True
        else:
            return False
        
# group_collide helper function
def group_collide(group, other_object):
    global explosion_group
    
    for element in set(group):
        if element.collide(other_object):
            group.remove(element)
            explosion_image_index = other_object.get_image_index()
            
            # use image for explosion if missile collides with rock
            if explosion_image_index != None:
                explosion_group.add(Sprite(element.get_position(), [0, 0], 0, 0, explosion_image_index,\
                                     explosion_images[explosion_image_index], explosion_info, explosion_sound))
            return True    
    
    return False

# group_group_collide helper function
def group_group_collide(first_group, second_group):
    collide_count = 0
    for element in set(first_group):
        if group_collide(second_group, element):
            collide_count += 1
            first_group.remove(element)
    return collide_count

# processing of sprite group (update, remove and draw)
def process_sprite_group (sprite_group, canvas):        
    for a_sprite in set(sprite_group):
        if a_sprite.update():
            sprite_group.remove(a_sprite)
        else:
            a_sprite.draw(canvas)

# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    
    vel_penalty = 0.005*score
    if(len(rock_group) < 12):
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        if dist(rock_pos, my_ship.get_position()) > 3.0*my_ship.get_radius():
            rock_vel_x = random.random() * .6 - .3
            rock_vel_y = random.random() * .6 - .3
            if rock_vel_x > 0.0:
                rock_vel_x += vel_penalty
            else:
                rock_vel_x -= vel_penalty
            
            if rock_vel_y > 0.0:
                rock_vel_y += vel_penalty
            else:
                rock_vel_y -= vel_penalty
                
            rock_vel = [rock_vel_x, rock_vel_y]
            rock_avel = random.random() * .2 - .1
            rock_image_index = random.randrange(len(asteroid_images))
            rock_group.add(Sprite(rock_pos, rock_vel, 0, rock_avel, rock_image_index,\
                                  asteroid_images[rock_image_index], asteroid_info))
            
# ship animate
def ship_animate():
    global show_ship_flag
    show_ship_flag = not show_ship_flag

# key handlers to control ship   
def keydown(key):
    if started:
        if key == simplegui.KEY_MAP['left']:
            my_ship.decrement_angle_vel()
        elif key == simplegui.KEY_MAP['right']:
            my_ship.increment_angle_vel()
        elif key == simplegui.KEY_MAP['up']:
            my_ship.set_thrust(True)
        elif key == simplegui.KEY_MAP['space']:
            my_ship.shoot()
        else:
            pass
        
def keyup(key):
    if started:
        if key == simplegui.KEY_MAP['left']:
            my_ship.increment_angle_vel()
        elif key == simplegui.KEY_MAP['right']:
            my_ship.decrement_angle_vel()
        elif key == simplegui.KEY_MAP['up']:
            my_ship.set_thrust(False)
        else:
            pass
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score
    
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    
    if (not started) and inwidth and inheight:
        started = True
        start_game()

# draw handler
def draw(canvas):
    global time, started, lives, score, rock_group, missile_group, explosion_group, my_ship
    global highest, games
    global coll_flag, collision_time, show_ship_flag, timer_ship_animate
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text("LIVES", [42, 20], 25, "Lime", "monospace")
    canvas.draw_text("SCORE", [695, 20], 25, "Yellow", "monospace")
    canvas.draw_text("Games", [250, 20], 25, "White", "monospace")
    canvas.draw_text("Highest", [500, 20], 25, "White", "monospace")
    canvas.draw_text(str(games), [250, 50], 25, "White", "sans-serif")
    canvas.draw_text(str(highest), [500, 50], 25, "White", "sans-serif")
    
    # draw the digits
    score_digits = [0] * 3   
    score_digits[0] = score / 100
    score_digits[1] = (score - score_digits[0] *100) / 10
    score_digits[2] = score % 10
    
    indices = []
    for digit in score_digits:
        if digit == 0:
            indices.append([4,1])
        elif digit > 5:
            indices.append([digit % 6, 1])
        else:
            indices.append([digit-1, 0])       
            
    for ctr in range(len(indices)):
        i = indices[ctr][0]
        j = indices[ctr][1]
        canvas.draw_image(digits_image, [12 + 24*i, 18 + 37*j], [24, 37], [710 + 24*ctr, 45], [24, 37])
        
    # Draw three images without thrust
    for i in range(3):
        canvas.draw_image(ship_image, [45, 45], [90, 90], [40*(i+1), 50], [50,50], -math.pi/2)
        
    # Now draw images with thrust for lives left 
    for i in range(lives):
        canvas.draw_image(ship_image, [135, 45], [90, 90], [40*(i+1), 50], [50,50], -math.pi/2)  
   
   
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        # draw the keyboard help
        scale = 1.25
        canvas.draw_polygon([(40, 510), (260, 510), (260, 590), (40, 590)], 1, 'Black', 'Black')
        
        canvas.draw_image(space_image, [156, 35], [313, 71], [150,560], [156*scale, 35*scale])
        canvas.draw_text("Launch missiles (Spacebar)", [48, 530], 13, "Orange", "monospace")
        
        canvas.draw_polygon([(280, 510), (780, 510), (780, 590), (280, 590)], 1, 'Black', 'Black')
        
        canvas.draw_image(arrows_image, [94, 35], [189, 71], [550,560], [94*scale, 35*scale])
        canvas.draw_text("Thrust ship (Up arrow)", [460, 530], 13, "Orange", "monospace")
        
        canvas.draw_text("Rotate ship anti-", [310, 560], 15, "Orange", "monospace")
        canvas.draw_text("clockwise (Left arrow)", [310, 580], 13, "Orange", "monospace")
        
        canvas.draw_text("Rotate ship clock-", [620, 560], 13, "Orange", "monospace")
        canvas.draw_text("wise (Right arrow)", [620, 580], 13, "Orange", "monospace")
        
    else:
        # check for collision of ship with rocks
        if group_collide(rock_group, my_ship):
            lives -= 1
            collision_time = time
            coll_flag = True
            timer_ship_animate.start()
            my_ship.vel[0] = 0; my_ship.vel[1] = 0
                
        if coll_flag:
            if time - collision_time == 30:
                timer_ship_animate.stop() 
                show_ship_flag = True
                coll_flag = False
                
        if show_ship_flag:
            # draw and update ship
            my_ship.draw(canvas); my_ship.update()
        
        # check for collisions between rocks and missiles
        score += group_group_collide(rock_group, missile_group)
        
        # draw and update sprites
        process_sprite_group(rock_group, canvas)
        process_sprite_group(missile_group, canvas)
        process_sprite_group(explosion_group, canvas)
        
        # restart if no lives left
        if lives == 0:
            init_game()
            my_ship.set_thrust(False)
            games += 1
            if score > highest:
                highest = score    
                 
# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer_rock_spawner = simplegui.create_timer(1000.0, rock_spawner)
timer_ship_animate = simplegui.create_timer(1.0, ship_animate)

# get things rolling
init_game()
frame.start()
