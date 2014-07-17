# http://www.codeskulptor.org/#user36_tDxcAchpmc_10.py

# program template for Spaceship

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

################################
# constants for spaceship
friction_coeff = 0.02
acc_coeff = 0.1
del_angle_vel = 0.05
missile_vel_coeff = 5

# constants for rock
vel = 3
angle_vel = 0.1
###################################

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
##################
ship_thrust_info = ImageInfo([135, 45], [90, 90], 35)
##################
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, angle_vel, image, info, info_thrust):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = angle_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        ##################
        self.image_thrust_center = info_thrust.get_center()
    
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        if self.thrust:
            canvas.draw_image(self.image, self.image_thrust_center, self.image_size, self.pos, self.image_size, self.angle)
            ship_thrust_sound.play()
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
            ship_thrust_sound.rewind()
        
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        self.angle += self.angle_vel
        forward = angle_to_vector(self.angle)
        
        if self.thrust:
            self.vel[0] += acc_coeff*forward[0]
            self.vel[1] += acc_coeff*forward[1]     
                
        self.vel[0] *= (1 - friction_coeff)
        self.vel[1] *= (1 - friction_coeff)
        
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
    
    def angle_vel_update(self, del_angle_vel):
        self.angle_vel += del_angle_vel
    
    def shoot(self):
        forward = angle_to_vector(self.angle)
        
        missile_pos = [self.pos[0] + forward[0] * (self.radius+9), self.pos[1] + forward[1] * (self.radius+9)]
        missile_vel = [self.vel[0] + missile_vel_coeff*forward[0], self.vel[1] + missile_vel_coeff*forward[1]]
        
        return Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound) 
    ######################################
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
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
        if sound:
            sound.rewind()
            sound.play()
   #######################################
    def draw(self, canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)      
        
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        self.angle += self.angle_vel
        
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
    #######################################
           
def draw(canvas):
    global time
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
    
    ############################
    # draw lives etc
    canvas.draw_text('**A S T E R O I D S**', (250, 50), 30, 'White')
    canvas.draw_text('Lives: '+ str(lives), (50, 50), 30, 'Lime', "monospace")
    canvas.draw_text('Score: '+ str(score), (600, 50), 30, 'Yellow', "monospace")
    #############################
##################################    
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    
    rock_pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
    
    # Use http://www.codeskulptor.org/docs.html#random-random to generate random velocities etc.
    rock_vel = [random.random()*2*vel - vel, random.random()*2*vel - vel]
    rock_angle_vel = random.random()*2*angle_vel - angle_vel
    a_rock = Sprite(rock_pos, rock_vel, 0, rock_angle_vel, asteroid_image, asteroid_info)

# handler for keydown
def keydown(key):
    global a_missile
    
    if key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel_update(del_angle_vel)
    elif key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel_update(-1.0*del_angle_vel)
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrust = True
    elif key == simplegui.KEY_MAP['space']:
        a_missile = my_ship.shoot()
    else:
        pass

# handler for keyup
def keyup(key):
    if key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel_update(-1.0*del_angle_vel)
    elif key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel_update(del_angle_vel)
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrust = False
    else:
        pass
######################################        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, 0, ship_image, ship_info, ship_thrust_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
