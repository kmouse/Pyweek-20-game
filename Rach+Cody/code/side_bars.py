from code.static import *
from code.calculations import *
import pygame

def text(string, size, color=BLACK):
    font = pygame.font.Font(None, size)
    return font.render(str(string), True, color)
    
    
class Settings_Item:
    def __init__(self, name, width, value, max_value=100):
        self.name = name
        self.value = value
        self.width = width
        self.max_value = max_value
        self.update_size(self.width)
        self.update()
        
    def update_value(self, value):
        self.value = value
        print(self.value)
        self.update()
        
    def update_size(self, width):
        self.width = width
        self.image = pygame.Surface((self.width, SETTINGS_HEIGHT), pygame.SRCALPHA)
        self.update()
        
    def update(self):
        print ("Updating:", self.image.get_width() * self.value / self.max_value)
        self.image.fill((0, 0, 0, 0))
        self.image.fill((255, 255, 255, 40), pygame.Rect((0,0), (self.image.get_width() * self.value / self.max_value, SETTINGS_HEIGHT)))
        self.image.blit(text(self.name, 25, WHITE), (0, 0))
    
    
class Settings:
    def __init__(self, width, items, current_item):
        self.image = pygame.Surface((1,1), pygame.SRCALPHA)
        self.current_item = current_item
        self.set_items(items, None)
            
        self.update_size(width)
        self.draw_items()
        
        self.size = 10
        
        # 0 is none
        # 1 is not me
        # 2 is me
        self.pressed = 0
        self.pressed_item = -1
        
        
    def update_size(self, width):
        self.image = pygame.Surface((width - MENU_WIDTH, SETTINGS_HEIGHT), pygame.SRCALPHA)
        self.image.fill(DARK_TRANSPARENT)
            
        if len(self.items):
            self.size = self.image.get_width()/(len(self.items) + 1)
            
        for item in self.items:
            item.update_size(self.image.get_width()/(len(self.items)+1))
        self.draw_items()
        
    def set_items(self, items, object):
        self.items = []
        
        if len(items):
            self.size = self.image.get_width()/(len(items) + 1)
            self.items.append(Settings_Item("delete", self.size, 0, 100))
            
        for item in items:
            self.items.append(Settings_Item(item, self.size, items[item], object.max_values[item]))
        self.draw_items()
        
        # Giving settings power to change the values in the object when a setting is changed
        self.controlled_object = object
            
    def click(self, x, y, pressed, screen_size):
        """Figures out if one of the settings items was changed, and then changes the settings item image.
        Returns whether it was changed."""
        #print (x, y)
        if x < screen_size[0] - MENU_WIDTH and y > screen_size[1] - SETTINGS_HEIGHT:
            if pressed and self.pressed != 1:
                self.pressed = 2
            if not pressed:
                self.pressed = 0
        else:
            if not pressed:
                self.pressed = 0
            if pressed and self.pressed == 0:
                self.pressed = 1
        #print (self.pressed)
        
        if self.pressed == 2 and len(self.items):
            i = int(x // self.size)
            if i == self.pressed_item or self.pressed_item == -1:
                self.pressed_item = i
                scroll_value = x - self.size*i
                scroll_value /= self.items[i].image.get_width()
                scroll_value *= self.items[i].max_value
                self.items[i].update_value(scroll_value)
                
                if self.items[i].name in self.controlled_object.linear_data:
                    self.controlled_object.linear_data[self.items[i].name] = self.items[i].value
                elif self.items[i].name in self.controlled_object.exponent_data:
                    self.controlled_object.exponent_data[self.items[i].name] = self.items[i].value
                elif self.items[i].name == 'delete':
                    type = self.controlled_object.type
                    self.draw_items()
                    self.controlled_object.kill()
                    return type
                    
                else:
                    print ("No attribute called:", self.items[i].name)
        
            #print (scroll_value)
            
        else:
            self.pressed_item = -1
        self.draw_items()
        return None
        
    def draw_items(self):
        self.image.fill(DARK_TRANSPARENT)
        i = 0
        for item in self.items:
            #print ( self.image.get_width()/len(self.items)*i)
            self.image.blit(item.image, (self.size*i, 0))
            i += 1
    
    
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
        
    def add(self, type):
        for item in self.menu_items:
            if item.type == type:
                item.quantity += 1