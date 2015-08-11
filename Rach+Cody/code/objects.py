from code.data import filepath
from code.calculations import direction, compass_lock, collide_point_square
from math import sin, cos, pi
import pygame


# This is how much a linear data item (e.g. position) costs
STATIC_DATA_COST = 4

GRAVITY = 0.05

MENU_WIDTH = 200
MENU_ITEM_HEIGHT = 70

FPS = 60

UNPRESS = 0
HOVER   = 1
PRESS   = 2

BLACK = (0,   0,   0  )
WHITE = (255, 255, 255)
GREEN = (25,  230, 100)
RED   = (255, 0,   0  )
BLUE  = (45,  75,  245)
TRANSPARENT = (0, 0, 0, 30)

pygame.font.init()


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
    
    
def text(string, size):
    font = pygame.font.Font(None, size)
    return font.render(str(string), True, BLACK)
    
    
class Menu_Item:
    def __init__(self, type, quantity):
        self.type = type
        self.quantity = quantity
        self.state = 0
        self.image = pygame.Surface((MENU_WIDTH, MENU_ITEM_HEIGHT), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 30))
        pygame.draw.line(self.image, (0, 0, 0, 60), (0, MENU_ITEM_HEIGHT), (MENU_WIDTH, MENU_ITEM_HEIGHT), 6)
        self.image.blit(text(type, 40), (10,10))
        self.image.blit(text(quantity, 20), (25,50))
        
    def press(self, state):
        self.state = state
        if state == UNPRESS:
            self.image.fill((0, 0, 0, 30))
            pygame.draw.line(self.image, (0, 0, 0, 60), (0, MENU_ITEM_HEIGHT), (MENU_WIDTH, MENU_ITEM_HEIGHT), 6)
            self.image.blit(text(self.type, 40), (10,10))
            self.image.blit(text(self.quantity, 20), (25,50))
        elif state == HOVER:
            self.image.fill((0, 0, 0, 45))
            pygame.draw.line(self.image, (0, 0, 0, 60), (0, MENU_ITEM_HEIGHT), (MENU_WIDTH, MENU_ITEM_HEIGHT), 6)
            self.image.blit(text(self.type, 40), (10,10))
            self.image.blit(text(self.quantity, 20), (25,50))
        elif state == PRESS:
            self.image.fill((0, 0, 0, 75))
            pygame.draw.line(self.image, (0, 0, 0, 100), (0, MENU_ITEM_HEIGHT), (MENU_WIDTH, MENU_ITEM_HEIGHT), 6)
            self.image.blit(text(self.type, 40), (10,10))
            self.image.blit(text(self.quantity, 20), (25,50))
            
    def update(self):
        press(self.state)
    
    
class Menu:
    def __init__(self, width, height, objects={}):
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.scroll = 0
        
        self.menu_items = []
        
        self.pressed = None
        
        for object in objects:
            self.menu_items.append(Menu_Item(object, objects[object]))
            
        self.create_stack = []
        
    def update(self):
        self.image.fill(GREEN)
        for i in range(len(self.menu_items)):
            self.image.blit(self.menu_items[i].image, (0, 20+i*(MENU_ITEM_HEIGHT + 20) - self.scroll))

    def press(self, mouse_pos, mouse_pressed, screen_width):
        ##FIX THESE LINES DAMMIT
        for i in range(len(self.menu_items)):
            if mouse_pressed == False:
                self.pressed = None
            elif self.pressed == None and 20+i*(MENU_ITEM_HEIGHT + 20) - self.scroll <= mouse_pos[1] <= 20+i*(MENU_ITEM_HEIGHT + 20) - self.scroll + MENU_ITEM_HEIGHT and screen_width - mouse_pos[0] < 200:
                self.pressed = i
                if (self.menu_items[i].quantity > 0):
                    self.create_stack.append(self.menu_items[i].type)
                    self.menu_items[i].quantity -= 1
                
            if self.pressed == i:
                self.menu_items[i].press(PRESS)
            elif 20+i*(MENU_ITEM_HEIGHT + 20) - self.scroll <= mouse_pos[1] <= 20+i*(MENU_ITEM_HEIGHT + 20) - self.scroll + MENU_ITEM_HEIGHT and screen_width - mouse_pos[0] < 200 and self.pressed == None:
                self.menu_items[i].press(HOVER)
                #print ("YEHAH")
            else:
                self.menu_items[i].press(UNPRESS)
        
    def update_size(self, width, height):
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        
    def create(self):
        # If there's items to be create
        if len(self.create_stack):
            return self.create_stack.pop(0)
        return None

    
class Server(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Set up the sprite
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        # Set up the sprite image 
        self.image = pygame.Surface((10, 10))
        self.image.fill(RED)
        
        # Set up the rect that controls the size and location of the sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
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
        self.rect.center = (self.x, self.y)
        
        self.velocity = [0,0]
        
    def update(self):
        self.velocity[1] += GRAVITY
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
        self.rect.center = (self.x, self.y)
        
    def move(self, data_objects):
        for object in data_objects:
            if object.type == "wind":
                object.move_bit(self)
        
        
class Data_Type:
    # A class variable to check if there is already a data_type grabbed
    grabbed = False
        
    def carry(self, x, y, pressed):
        if collide_point_square((x, y), self.rect.topleft, self.rect.bottomright):
            if pressed and self.carried == 0 and Data_Type.grabbed == False:
                self.carried = 2
                Data_Type.grabbed = True
        elif (pressed or Data_Type.grabbed == True) and self.carried != 2:
            self.carried = 1
        if not pressed:
            Data_Type.grabbed = False
            self.carried = 0
        
        if self.carried == 2:
            self.rect.center = (x, y)
            
    # self.exponent_data should be a dict with all the counted data
    def count_data(self):
        bits = 0
        for point in self.exponent_data:
            print(point, ":", self.exponent_data[point], "-", get_data_size_int(self.exponent_data[point]))
            bits += get_data_size_int(self.exponent_data[point])
        bits += STATIC_DATA_COST*len(self.linear_data)
        return bits
        

class Wind(Data_Type, pygame.sprite.Sprite):
    def __init__(self, x, y, magnitude=50, direction=0):
        assert (0 <= magnitude <= 100)
        self.type = "wind"
        # Set up the sprite
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        # Set up the sprite image 
        self.image = pygame.Surface((100, 100))
        self.image.fill(WHITE)
        
        # Set up the rect that controls the size and location of the sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # self.linear_data has points that each cost STATIC_DATA_COST bits
        # self.exponent_data increases for each extra bit you use (i.e. the number 7 costs 3, the number 8 costs 4)
        self.linear_data = {'x':x, 'y':y, 'direction':direction}
        self.exponent_data = {'magnitude':magnitude}
        
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
            bit.velocity[0] += self.exponent_data['magnitude'] * cos(self.linear_data['direction']) / 200
            bit.velocity[1] -= self.exponent_data['magnitude'] * sin(self.linear_data['direction']) / 200
        else:
            bit.image.fill(BLUE)
            
    def update_direction(self, direction):
        direction = compass_lock(-direction)
        self.image.fill(WHITE)
        self.linear_data['direction'] = direction
        
        ## THIS CODE IS LITERALLY HITLER
        # It calculates the nodes (or edges) of the rotated fan
        # They are used in the caculations of whether a bit is in the wind or not
        self.nodes = ([int(self.rect.width//2*cos(-direction-pi/2)+self.rect.width//2), int(self.rect.width//2*sin(-direction-pi/2)+self.rect.width//2)], [int(self.rect.width//2*cos(-direction + pi/2)+self.rect.width//2), int(self.rect.width//2*sin(-direction + pi/2)+self.rect.width//2)])
        pygame.draw.circle(self.image, BLACK, self.nodes[0], 3)
        pygame.draw.circle(self.image, BLACK, self.nodes[1], 3)
        #self.nodes[0][0] += self.rect.left
        #self.nodes[1][0] += self.rect.left
        #self.nodes[0][1] += self.rect.top
        #self.nodes[1][1] += self.rect.top