from code.data import filepath
import pygame


# This is how much a linear data item (e.g. position) costs
STATIC_DATA_COST = 4

GRAVITY = 10

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

    
class Server(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Set up the sprite
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        # Set up the sprite image 
        self.image = pygame.Surface((100, 100))
        self.image.fill(RED)
        
        # Set up the rect that controls the size and location of the sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.emit_time = 30 # frames
        self.timer = self.emit_time
        
    def update(self):
        self.timer = (self.timer - 1) if self.timer != 0 else self.emit_time
  
  
class Bit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Set up the sprite
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        # Set up the sprite image 
        self.image = pygame.Surface((100, 100))
        self.image.fill(BLUE)
        
        # Set up the rect that controls the size and location of the sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
    def update(self):
        self.rect.top += GRAVITY
        
        
class Data:
    # self.exponent_data should be a dict with all the counted data
    def count_data(self):
        bits = 0
        for point in self.exponent_data:
            print(point, ":", self.exponent_data[point], "-", get_data_size_int(self.exponent_data[point]))
            bits += get_data_size_int(self.exponent_data[point])
        bits += STATIC_DATA_COST*len(self.linear_data)
        return bits
        

class Wind(Data, pygame.sprite.Sprite):
    def __init__(self, x, y, magnitude=1, direction=0):
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
        
    #def count_data(self):
    #    pass