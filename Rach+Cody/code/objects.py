from code.data import filepath
from code.calculations import *
from code.static import *
from code.side_bars import *
from code.base_types import *
from math import sin, cos, pi, sqrt, degrees
import pygame

pygame.font.init()


def rotate_center(image, angle):
    orig_size = image.get_size()
    new = pygame.transform.rotate(image, angle)
    image.fill((0, 0, 0, 0))
    new_size = new.get_size()
    pos = ((orig_size[0] - new_size[0]) // 2, (orig_size[1] - new_size[1]) // 2)
    image.blit(new, pygame.Rect(pos, orig_size))
    
    
def reflect(velocity, normal, exit_velocity=1):
    angle = compass_lock(-direction(velocity, (0, 0)) + pi)
    magnitude = distance((0, 0), velocity) * exit_velocity
    
    angle = compass_lock(2*normal - angle - pi/2)
    velocity = [magnitude*sin(angle), magnitude*cos(angle)]
    return velocity

    
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

    
class Server(Screen_Object, pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Set up the sprite
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        # Set up the sprite image 
        self.image = pygame.Surface((10, 10))
        self.image.fill(RED)
        self.x, self.y = x, y
        
        # Set up the rect that controls the size and location of the sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.emit_time = 60 # frames
        self.timer = self.emit_time
        
    def update(self):
        self.rect.center = (self.x, self.y)
        self.timer = (self.timer - 1) if self.timer != 0 else self.emit_time
        
        
class Computer(Screen_Object, pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Set up the sprite
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        # Set up the sprite image 
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        
        self.x, self.y = x, y
        
        # Set up the rect that controls the size and location of the sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.emit_time = 60 # frames
        self.timer = self.emit_time
        
    def update(self):
        self.rect.center = (self.x, self.y)
        self.timer = (self.timer - 1) if self.timer != 0 else self.emit_time
        
  
class Bit(Screen_Object, pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Set up the sprite
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        # Set up the sprite image 
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLUE)
        
        self.x, self.y = x, y
        
        self.age = 0
        
        # Set up the rect that controls the size and location of the sprite
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        self.velocity = [0,0]
        
    def update(self):
        self.velocity[1] += GRAVITY
        
        self.velocity[0] *= FRICTION
        self.velocity[1] *= FRICTION
        
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
        self.rect.center = (self.x, self.y)
        
        self.age += 1
        if self.age > MAX_AGE:
            self.kill()
        
    def move_pos(self, user_objects, scene_objects):
        for object in user_objects:
            object.move_bit(self)
        for object in scene_objects:
            object.move_bit(self)
        
    
class Wind(Data_Type, pygame.sprite.Sprite):
    def __init__(self, x, y, magnitude=50, direction=0):
        assert (0 <= magnitude <= 100)
        self.type = "wind"
        
        self.timer = 0
        
        # Set up the sprite
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        # Set up the sprite image 
        self.image = pygame.Surface((100, 100))
        self.image.fill(WHITE)
        
        # Set up the rect that controls the size and location of the sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.x, self.y = x, y
        
        # self.linear_data has points that each cost STATIC_DATA_COST bits
        # self.exponent_data increases for each extra bit you use (i.e. the number 7 costs 3, the number 8 costs 4)
        self.linear_data = {'direction':direction}
        self.exponent_data = {'magnitude':magnitude}
        self.max_values = {'direction':pi*2, 'magnitude':100}
        
        self.update_direction(direction)
        
        # 0 is none pressed
        # 1 is something else pressed
        # 2 is self pressed
        self.carried = 0
            
        
    def move_bit(self, bit):
        nodes_in_space = ((self.nodes[0][0] + self.rect.left, self.nodes[0][1] + self.rect.top),
                          (self.nodes[1][0] + self.rect.left, self.nodes[1][1] + self.rect.top))
        # Get the angle from both nodes
        angles = [direction(nodes_in_space[0], bit.rect.center), direction(nodes_in_space[1], bit.rect.center)]
        angles[0] = compass_lock(angles[0] + self.linear_data['direction'], False)
        angles[1] = compass_lock(angles[1] + self.linear_data['direction'], False)
        #print(angles)
        #print(angles, pi/2, self.nodes[0], bit.rect.topleft)
        if angles[0] > 0 and angles[1] < 0:
            #print ("Yoooooooooo")
            bit.image.fill(RED)
            bit.velocity[0] += self.exponent_data['magnitude'] * cos(self.linear_data['direction']) / 400
            bit.velocity[1] -= self.exponent_data['magnitude'] * sin(self.linear_data['direction']) / 400
        else:
            bit.image.fill(BLUE)
            
    def update_direction(self, direction):
        direction = compass_lock(-direction)
        self.linear_data['direction'] = direction
        
        ## THIS CODE IS LITERALLY HITLER
        # It calculates the nodes (or edges) of the rotated fan
        # They are used in the caculations of whether a bit is in the wind or not
        self.nodes = ([int(self.rect.width//2*cos(-direction-pi/2)+self.rect.width//2), int(self.rect.width//2*sin(-direction-pi/2)+self.rect.width//2)], [int(self.rect.width//2*cos(-direction + pi/2)+self.rect.width//2), int(self.rect.width//2*sin(-direction + pi/2)+self.rect.width//2)])

        
    def update(self):
        self.update_direction(-self.linear_data['direction'])
        #print ("aAA")
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, BLACK, self.nodes[0], 3)
        pygame.draw.circle(self.image, BLACK, self.nodes[1], 3)
        
        center = (self.rect.width//2, self.rect.height//2)
        offset = (self.rect.width//2+self.exponent_data['magnitude']//2*cos(-self.linear_data['direction']), self.rect.height//2+self.exponent_data['magnitude']//2*sin(-self.linear_data['direction']))
        pygame.draw.line(self.image, RED, center, offset, 5)
        
        
class Bounce(Data_Type, pygame.sprite.Sprite):
    def __init__(self, x, y, bounciness=100, direction=-pi/2):
        self.type = "bounce"
        
        self.timer = 0
        
        # Set up the sprite
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        # Set up the sprite image 
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.internal_size = (sqrt(100**2 - WALL_WIDTH**2), WALL_WIDTH)
        self.bounce = pygame.Surface(self.internal_size)
        self.image.fill((0, 0, 0, 0))
        self.bounce.fill(WHITE)
        
        # Set up the rect that controls the size and location of the sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # self.linear_data has points that each cost STATIC_DATA_COST bits
        # self.exponent_data increases for each extra bit you use (i.e. the number 7 costs 3, the number 8 costs 4)
        self.linear_data = {'direction':direction}
        self.exponent_data = {'bounciness':bounciness}
        self.max_values = {'direction':pi, 'bounciness':100}
        
        self.update_direction(direction)
        
        # 0 is none pressed
        # 1 is something else pressed
        # 2 is self pressed
        self.carried = 0
        self.last_direction = self.linear_data['direction']
            
        
    def move_bit(self, bit):
        #print(angles)
        #print(angles, pi/2, self.nodes[0], bit.rect.topleft)
        top = self.rect.top + (self.rect.height - self.internal_size[0]) / 2
        left = self.rect.left + (self.rect.width - self.internal_size[1]) / 2
        bottom = self.rect.top + (self.rect.height + self.internal_size[0]) / 2
        right = self.rect.left + (self.rect.width + self.internal_size[1]) / 2
        #print ( (left, top), (right, bottom))
        if collide_point_square(bit.rect.center, (left, top), (right, bottom), self.linear_data['direction']):
            #print ("Yoooooooooo")
            bit.image.fill(RED)
            
            bit.velocity = reflect(bit.velocity, self.linear_data['direction'], self.exponent_data['bounciness']/100)
            bit.update()
            #bit.velocity[1] = 0
            #= reflect(bit.velocity, self.linear_data['direction'])
        else:
            bit.image.fill(BLUE)
            
    def update_direction(self, direction):
        direction = compass_lock(-direction)
        self.linear_data['direction'] = direction
        
        top = self.rect.height / 2 - self.internal_size[1] / 2
        left = self.rect.width / 2 - self.internal_size[0] / 2
        
        self.image.fill((0, 0, 0, 0))
        self.bounce.fill(WHITE)
        self.image.blit(self.bounce, (left, top))
        rotate_center(self.image, degrees(self.linear_data['direction']) + 90)
        
    def update(self):
        if self.last_direction != self.linear_data['direction']:
            self.update_direction(-self.linear_data['direction'])
        
        self.last_direction = self.linear_data['direction']
        
        
class Conveyor(Data_Type, pygame.sprite.Sprite):
    def __init__(self, x, y, width=100, speed=75):
        self.type = "conveyor"
        
        self.timer = 0
        
        # Set up the sprite
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        # Set up the sprite image 
        self.image = pygame.Surface((width, WALL_WIDTH), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.image.fill(ORANGE)
        
        # Set up the rect that controls the size and location of the sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # self.linear_data has points that each cost STATIC_DATA_COST bits
        # self.exponent_data increases for each extra bit you use (i.e. the number 7 costs 3, the number 8 costs 4)
        self.linear_data = {}
        self.exponent_data = {'width':width, 'speed':speed}
        self.max_values = {'width':100, 'speed':100}
        
        # 0 is none pressed
        # 1 is something else pressed
        # 2 is self pressed
        self.carried = 0
            
        
    def move_bit(self, bit):
        if collide_point_square(bit.rect.center, self.rect.topleft, self.rect.bottomright):
            #print ("Yoooooooooo")
            bit.image.fill(RED)
            
            bit.velocity[0] = (self.exponent_data['speed'] - 50) / 10
            bit.velocity[1] = 0
            #bit.rect.centery = self.rect.top
            #bit.x, bit.y = bit.rect.center
        else:
            bit.image.fill(BLUE)

            
class Wall(Screen_Object, pygame.sprite.Sprite):
    def __init__(self, x, y, orientation, length=100):
        assert (length >= WALL_WIDTH)
        self.type = "wall"
        # Set up the sprite
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        # Set up the sprite image 
        size = (WALL_WIDTH, length) if orientation == 'v' else (length, WALL_WIDTH)
        
        self.normal = 0 if orientation == 'v' else pi/2
        
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill(WHITE)
        
        self.x, self.y = x, y
        
        # Set up the rect that controls the size and location of the sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
            
        
    def move_bit(self, bit):
        if collide_point_square(bit.rect.center, self.rect.topleft, self.rect.bottomright):
            #print ("Yoooooooooo")
            bit.image.fill(RED)
            
            bit.velocity = reflect(bit.velocity, self.normal)
            
            #bit.velocity[1] = 0
            #= reflect(bit.velocity, self.linear_data['direction'])
        else:
            bit.image.fill(BLUE)
            
    def update(self):
        self.rect.center = self.x, self.y