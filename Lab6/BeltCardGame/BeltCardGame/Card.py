import pygame

class Card(object):
    """Карта, її значення, розташування, зображення тощо"""
    def __init__(self, scr, imgName):
        self.scr = scr
        self.coords = [0, 0]
        #Card.size:
        #0 - in deck
        #1 - everywhere else
        #2 - in human's hand
        self.size = 0
        cardName = imgName.split('.')[0].split('_')
        self.value = cardName[0]
        self.suit = cardName[1]
        self.sourceImage = pygame.image.load(f'assets/cards/{imgName}')
        self.image = pygame.transform.scale(self.sourceImage, (48, 64))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.coords

    def update(self, coords = None, size = None):
        if coords is not None:
            self.coords = coords
        if size is not None:
            self.size = size
            if self.size == 1:
                self.image = self.sourceImage
                self.rect = self.image.get_rect()
                self.rect.topleft = self.coords
            if self.size == 2:
                self.image = pygame.transform.scale(self.sourceImage, (100, 139))
                self.rect = self.image.get_rect()
                self.rect.topleft = self.coords
        self.rect.topleft = self.coords
        self.scr.blit(self.image, self.rect)