from code.objects import Wind, Bit, Server
import pygame
import sys


FPS = 60

BLACK = (0,   0,   0  )
WHITE = (255, 255, 255)
GREEN = (25,  230, 100)
RED   = (255, 0,   0  )
BLUE  = (45,  75,  245)



def printer():
    # A pygame group for things the user interacts with
    interaction_group = pygame.sprite.Group()
    
    Wind.containers = interaction_group
    
    thing = Wind(0, 0)
    print(thing.count_data())
    
def draw(screen, *groups):
    screen.fill(BLACK)
    for group in groups:
        group.draw(screen)
        
        
def main():
    screen = pygame.display.set_mode((640, 480))
    
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
    
    Wind(200, 200)
    Server(0,0)
    
    clock = pygame.time.Clock()
    
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
        dynamic_group.update()
        for item in server_group:
            if item.timer == 0:
                Bit(item.rect.top, item.rect.left)
                
        for bit in bit_group:
            bit.move(interaction_group)
            
        draw(screen, interaction_group, dynamic_group)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()