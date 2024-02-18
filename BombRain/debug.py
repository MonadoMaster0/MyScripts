import pygame

def debug(screen: pygame.Surface, *args):
    pygame.font.init()
    text = pygame.font.Font(pygame.font.get_default_font(), 20)
    debugText = ""
    for i, a in enumerate(args):
        b = "".join([str(s) for s in a])
        debugText = text.render(b,1,(0,0,0),(100,100,100))
        screen.blit(debugText, (10,10+i*20))
    