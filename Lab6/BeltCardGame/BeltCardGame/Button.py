import TextBox

class Button(TextBox.TextBox):
    """Кнопка в меню, яку можна натиснути"""
    def __init__(self, mouse, scr, text, coords, color, borderWidth, textSize):
        super().__init__(scr, text, coords, color, borderWidth, textSize)
        self.isPressed = False
        self.isHovered = False
        self.mouse = mouse

    def update(self, isSelected = False):
        if self.mouse.intersects(self.coords):
            if self.mouse.isDown:
                self.isPressed = True
                self.isHovered = False
            else:
                self.isPressed = False
                self.isHovered = True
        else:
            self.isPressed = False
            self.isHovered = False

        if self.isPressed:
            super().update((140, 255, 251))
        elif self.isHovered:
            super().update((161, 209, 210))
        elif isSelected:
            super().update((255, 248, 125))
        else:
            super().update()