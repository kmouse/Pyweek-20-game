from code.data import filepath
from code.calculations import direction, compass_lock
from math import sin, cos, pi
import pygame


# This is how much a linear data item (e.g. position) costs
STATIC_DATA_COST = 4

GRAVITY = 0.05

FPS = 60

BLACK = (0,   0,   0  )
WHITE = (255, 255, 255)
GREEN = (25,  230, 100)
RED   = (255, 0,   0  )
BLUE  = (45,  75,  245)


# Load an image for pygame
def loadIm(name):
    file = data.filepath(name)
    try:
        image = pygame.image.load(file)
        return image.convert_alpha()
    except:
        name = 'error.png'
        print ('Could not load:', file)
        file = data.filepath(name)
        image = pygame.image.load(file)
        return image.convert_alpha()
        
        
def get_data_size_int(point):
    i = 1
    while point > 1:
        point //= 2
        i += 1
        
    return (i)
    
    
class Menu:
    def __init__(self, screen):
        pass

    
class Server(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Set up the sprite
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        # Set up the sprite image 
        self.image = pygame.Surface((10, 10))
        self.image.fill(RED)
        
        # Set up the rect that controls the size and location of the sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.emit_time = 60 # frames
        self.timer = self.emit_time
        
    def update(self):
        self.timer = (self.timer - 1) if self.timer != 0 else self.emit_time
  
  
class Bit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Set up the sprite
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        # Set up the sprite image 
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLUE)
        
        self.x, self.y = x, y
        
        # Set up the rect that controls the size and location of the sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        
        self.velocity = [0,0]
        
    def update(self):
        self.velocity[1] += GRAVITY
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
        self.rect.topleft = (self.x, self.y)
        
    def move(self, data_objects):
        for object in data_objects:
            if object.type == "wind":
                object.move_bit(self)
        
        
class Data_Type:
    # self.exponent_data should be a dict with all the counted data
    def count_data(self):
        bits = 0
        for point in self.exponent_data:
            print(point, ":", self.exponent_data[point], "-", get_data_size_int(self.exponent_data[point]))
            bits += get_data_size_int(self.exponent_data[point])
        bits += STATIC_DATA_COST*len(self.linear_data)
        return bits
        

class Wind(Data_Type, pygame.sprite.Sprite):
    def __init__(self, x, y, magnitude=100, direction=0.7):
        assert (0 <= magnitude <= 100)
        self.type = "wind"
        # Set up the sprite
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        # Set up the sprite image 
        self.image = pygame.Surface((100, 100))
        self.image.fill(WHITE)
        
        # Set up the rect that controls the size and location of the sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # self.linear_data has points that each cost STATIC_DATA_COST bits
        # self.exponent_data increases for each extra bit you use (i.e. the number 7 costs 3, the number 8 costs 4)
        self.linear_data = {'x':x, 'y':y, 'direction':direction}
        self.exponent_data = {'magnitude':magnitude}
        
        ## THIS CODE IS LITERALLY HITLER
        # It calculates the nodes (or edges) of the rotated fan
        # They are used in the caculations of whether a bit is in the wind or not
        self.nodes = ([int(self.rect.width//2*cos(-direction-pi/2)+self.rect.width//2), int(self.rect.width//2*sin(-direction-pi/2)+self.rect.width//2)], [int(self.rect.width//2*cos(-direction + pi/2)+self.rect.width//2), int(self.rect.width//2*sin(-direction + pi/2)+self.rect.width//2)])
        pygame.draw.circle(self.image, BLACK, self.nodes[0], 3)
        pygame.draw.circle(self.image, BLACK, self.nodes[1], 3)
        self.nodes[0][0] += self.rect.left
        self.nodes[1][0] += self.rect.left
        self.nodes[0][1] += self.rect.top
        self.nodes[1][1] += self.rect.top
        
        
    def move_bit(self, bit):
        # Get the angle from both nodes
        angles = [direction(self.nodes[0], bit.rect.center), direction(self.nodes[1], bit.rect.center)]
        #angles = [direction((0,1), (0,0)), direction((0,0), (-1,0))]
        angles[0] = compass_lock(angles[0] + self.linear_data['direction'], False)
        angles[1] = compass_lock(angles[1] + self.linear_data['direction'], False)
        #print(angles, pi/2, self.nodes[0], bit.rect.topleft)
        if angles[0] > 0 and angles[1] < 0:
            #print ("Yoooooooooo")
            bit.velocity[0] += self.exponent_data['magnitude'] * cos(self.linear_data['direction']) / 200
            bit.velocity[1] -= self.exponent_data['magnitude'] * sin(self.linear_data['direction']) / 200
            
    def update_direction(self, direction):
        self.image.fill(WHITE)
        self.linear_data['direction'] = direction
        self.nodes = ([int(self.rect.width//2*cos(-direction-pi/2)+self.rect.width//2), int(self.rect.width//2*sin(-direction-pi/2)+self.rect.width//2)], [int(self.rect.width//2*cos(-direction + pi/2)+self.rect.width//2), int(self.rect.width//2*sin(-direction + pi/2)+self.rect.width//2)])
        pygame.draw.circle(self.image, BLACK, self.nodes[0], 3)
        pygame.draw.circle(self.image, BLACK, self.nodes[1], 3)
        self.nodes[0][0] += self.rect.left
        self.nodes[1][0] += self.rect.left
        self.nodes[0][1] += self.rect.top
        self.nodes[1][1] += self.rect.top