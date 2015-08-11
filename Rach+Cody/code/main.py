from code.objects import Wind, Bit, Server, Menu
from code.calculations import direction
import pygame
import sys


FPS = 60

MENU_WIDTH = 200

DEFAULT_SCREEN_WIDTH  = 800
DEFAULT_SCREEN_HEIGHT = 500

BLACK      = (0,   0,   0  )
WHITE      = (255, 255, 255)
GREEN      = (25,  230, 100)
RED        = (255, 0,   0  )
BLUE       = (45,  75,  245)
FAINT_BLUE = (55, 55, 75)


def draw(screen, *groups):
    screen.fill(BLACK)
    for group in groups:
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
    level(screen)
        
def level(screen):
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
    
    Wind.containers = interaction_group
    Bit.containers = dynamic_group, bit_group
    Server.containers = dynamic_group, server_group
    
    menu = Menu(screen.get_width(), screen.get_height(), {"wind":3, "cats":3})
    
    Server(100,10)
    
    clock = pygame.time.Clock()
    
    
    while True:
        mouse_pos = list(pygame.mouse.get_pos())
        mouse_pos[0] -= game_pos[0]
        mouse_pos[1] -= game_pos[1]
        mouse_pressed = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((max(event.w, DEFAULT_SCREEN_WIDTH), max(event.h, DEFAULT_SCREEN_HEIGHT)), pygame.RESIZABLE)
                #game = pygame.Surface((max(event.w, DEFAULT_SCREEN_WIDTH)-MENU_WIDTH, max(event.h, DEFAULT_SCREEN_HEIGHT)))
                game_pos = ((screen.get_width()-200) / 2 - game.get_width() / 2, screen.get_height() / 2 - game.get_height() / 2)
                menu_surfece = pygame.Surface((MENU_WIDTH, max(event.h, DEFAULT_SCREEN_HEIGHT)))
                menu.update_size(MENU_WIDTH, max(event.h, DEFAULT_SCREEN_HEIGHT))
            if event.type == pygame.KEYDOWN:
                pass
                
                
        dynamic_group.update()
        for item in server_group:
            if item.timer == 0:
                Bit(item.rect.centerx, item.rect.centery)
                
        
        for bit in bit_group:
            bit.move(interaction_group)
                        
        for item in interaction_group:
            #print (direction(item.rect.center, mouse_pos))
            item.carry(mouse_pos[0], mouse_pos[1], mouse_pressed[0])
            item.rect.clamp_ip(game.get_rect())
            
        draw(game, interaction_group, dynamic_group)
        menu_surfece.fill((GREEN))
        update_menu(menu_surfece, menu, screen.get_width())
        new_object = menu.create()
        if new_object != None:
            if new_object == "wind":
                Wind(mouse_pos[0], mouse_pos[1])
            
        background(screen, game_pos)
        screen.blit(menu_surfece, (screen.get_width()-MENU_WIDTH, 0))
        screen.blit(game, game_pos)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()