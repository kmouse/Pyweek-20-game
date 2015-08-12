from code.objects import Wind, Bit, Server, Computer, Menu, Data_Type, Settings
from code.calculations import direction
from code.static import *
import pygame
import sys



def total_data(objects):
    total = 0
    for object in objects:
        total += object.count_data()
    return total
    
    
def draw(screen, *groups):
    screen.fill(BLACK)
    for group in groups:
        #group.update()
        group.draw(screen)
        
def background(screen, game_pos):
    screen.fill(BLACK)
    rect = pygame.Rect((game_pos[0] - 2, game_pos[1] - 2), (DEFAULT_SCREEN_WIDTH - 200 + 4, DEFAULT_SCREEN_HEIGHT + 4))
    pygame.draw.rect(screen, FAINT_BLUE, rect)
    
        
def update_menu(screen, menu, total_width):
    menu.press(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0], total_width)
    menu.update()
    screen.blit(menu.image, (0, 0))
        
        
def main():
    screen = pygame.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT), pygame.RESIZABLE)
    level(screen, {'interactive':{'wind':2}, 'static':{'server':(10,10), 'computer':(200, 40)}})
        
        
def level(screen, objects):
    game = pygame.Surface((DEFAULT_SCREEN_WIDTH-MENU_WIDTH, DEFAULT_SCREEN_HEIGHT))
    # Where the game is rendered
    # Initially (0, 0) as it is the default screen size
    game_pos = (0,0)
    menu_surfece = pygame.Surface((MENU_WIDTH, DEFAULT_SCREEN_HEIGHT))
    
    # A pygame group for things the user interacts with
    interaction_group = pygame.sprite.Group()
    # Pygame group for dynamic objects that the user can't interact with
    dynamic_group = pygame.sprite.Group()
    # Group for the individual objects
    bit_group = pygame.sprite.Group()
    server_group = pygame.sprite.Group()
    
    settings = Settings(screen.get_width(), [], None)
    
    Wind.containers = interaction_group
    Bit.containers = dynamic_group, bit_group
    Server.containers = dynamic_group, server_group
    Computer.containers = dynamic_group
    
    menu = Menu(screen.get_width(), screen.get_height(), objects['interactive'])
    for object in objects['static']:
        if object == 'server':
            Server(*objects['static'][object])
        elif object == 'computer':
            Computer(*objects['static'][object])
    
    clock = pygame.time.Clock()
    
    
    while True:
        mouse_pos = list(pygame.mouse.get_pos())
        mouse_pos[0] -= game_pos[0]
        mouse_pos[1] -= game_pos[1]
        mouse_pressed = pygame.mouse.get_pressed()
        
        mouse_absolute_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((max(event.w, DEFAULT_SCREEN_WIDTH), max(event.h, DEFAULT_SCREEN_HEIGHT)), pygame.RESIZABLE)
                #game = pygame.Surface((max(event.w, DEFAULT_SCREEN_WIDTH)-MENU_WIDTH, max(event.h, DEFAULT_SCREEN_HEIGHT)))
                game_pos = ((screen.get_width()-200) / 2 - game.get_width() / 2, screen.get_height() / 2 - game.get_height() / 2)
                menu_surfece = pygame.Surface((MENU_WIDTH, max(event.h, DEFAULT_SCREEN_HEIGHT)))
                menu.update_size(MENU_WIDTH, max(event.h, DEFAULT_SCREEN_HEIGHT))
                settings.update_size(screen.get_width())
            if event.type == pygame.KEYDOWN:
                pass
                
                
        dynamic_group.update()
        for item in server_group:
            if item.timer == 0:
                Bit(item.rect.centerx, item.rect.centery)
                
        
        for bit in bit_group:
            bit.move(interaction_group)
                        
        for item in interaction_group:
            item.carry(mouse_pos[0], mouse_pos[1], mouse_pressed[0])
            new_settings = item.right_click(mouse_pos[0], mouse_pos[1], mouse_pressed[2])
            if new_settings != None:
                settings.set_items(new_settings, item)
            item.rect.clamp_ip(game.get_rect())
            
        interaction_group.update()
        draw(game, interaction_group, dynamic_group)
        menu_surfece.fill((GREEN))
        update_menu(menu_surfece, menu, screen.get_width())
        
        if settings.click(mouse_absolute_pos[0], mouse_absolute_pos[1], mouse_pressed[0], screen.get_size()):
            pass
        
        # All data objects (i.e. the things that the user controls) must be created here
        new_object = menu.create()
        if new_object != None:
            if new_object == "wind":
                Wind(mouse_pos[0], mouse_pos[1])
                print (total_data(interaction_group))
            
        background(screen, game_pos)
        screen.blit(menu_surfece, (screen.get_width()-MENU_WIDTH, 0))
        screen.blit(game, game_pos)
        screen.blit(settings.image, (0, screen.get_height() - SETTINGS_HEIGHT))
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()