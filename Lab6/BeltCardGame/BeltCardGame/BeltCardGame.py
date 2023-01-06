import Mouse
import ScrSwitcher
import pygame

def main():
    """Основний файл програми для гри 'Ремінь' """
    pygame.init()
    pygame.font.init()

    dimensions = (1300, 750)
    scr = pygame.display.set_mode(dimensions)
    background = pygame.image.load('assets/background.png')
    pygame.display.set_caption("Ремінь")

    clock = pygame.time.Clock()

    mouse = Mouse.Mouse()
    scrSwitcher = ScrSwitcher.ScrSwitcher(scr, mouse)

    FPS = 60

    run = True

    while run == True:
    
        scr.blit(background, (0, 0))

        mouse.update()
        scrSwitcher.update()

        pygame.display.update()
        clock.tick(FPS)

        for myEvent in pygame.event.get():
            if myEvent.type == pygame.QUIT:
                pygame.quit()
                run = False

if __name__ == '__main__':
    main()