from code.objects import Wind, Bit, Server, Menu
from code.calculations import direction
import pygame
import sys


FPS = 60

MENU_WIDTH = 200

DEFAULT_SCREEN_WIDTH  = 700
DEFAULT_SCREEN_HEIGHT = 500

BLACK = (0,   0,   0  )
WHITE = (255, 255, 255)
GREEN = (25,  230, 100)
RED   = (255, 0,   0  )
BLUE  = (45,  75,  245)


def draw(screen, *groups):
    screen.fill(BLACK)
    for group in groups:
        group.draw(screen)
        
        
def update_menu(screen, menu):
    menu.update()
    screen.blit(menu.image, (0, 0))
        
        
def main():
    screen = pygame.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT), pygame.RESIZABLE)
    game = pygame.Surface((DEFAULT_SCREEN_WIDTH-MENU_WIDTH, DEFAULT_SCREEN_HEIGHT))
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
    
    menu = Menu(screen.get_width(), screen.get_height(), {"dogs":3, "cats":3})
    
    Wind(100, 100, magnitude=50)
    Server(0,0)
    
    clock = pygame.time.Clock()
    
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((max(event.w, DEFAULT_SCREEN_WIDTH), max(event.h, DEFAULT_SCREEN_HEIGHT)), pygame.RESIZABLE)
                game = pygame.Surface((max(event.w, DEFAULT_SCREEN_WIDTH)-MENU_WIDTH, max(event.h, DEFAULT_SCREEN_HEIGHT)))
                menu_surfece = pygame.Surface((MENU_WIDTH, max(event.h, DEFAULT_SCREEN_HEIGHT)))
                menu.update_size(MENU_WIDTH, max(event.h, DEFAULT_SCREEN_HEIGHT))
                print(dir(event))
               
        dynamic_group.update()
        for item in server_group:
            if item.timer == 0:
                Bit(item.rect.top, item.rect.left)
                
        mouse = pygame.mouse.get_pos()
        for item in interaction_group:
            item.update_direction(-direction(item.rect.center, mouse))
        for bit in bit_group:
            bit.move(interaction_group)
            
        draw(game, interaction_group, dynamic_group)
        menu_surfece.fill((GREEN))
        update_menu(menu_surfece, menu)
        screen.blit(menu_surfece, (screen.get_width()-MENU_WIDTH, 0))
        screen.blit(game, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()