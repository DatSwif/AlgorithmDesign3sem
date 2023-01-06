import Button
import TextBox

class Controls(object):
    """Вікно з правилами та поясненням як грати"""
    def __init__(self, scr, mouse):
        self.scr = scr
        self.mouse = mouse

        self.title = TextBox.TextBox(self.scr, 'Правила гри', (340, 40, 710, 140), (255, 255, 255), -1, 48)
        
        self.text = []
        self.text.append(TextBox.TextBox(self.scr, 'На початку гри кожному гравцеві дають 4 карти з колоди.',               (350, 150, 550, 190), (255, 255, 255), -1, 20))
        self.text.append(TextBox.TextBox(self.scr, 'У свій хід можна:',                                                     (150, 190, 350, 230), (255, 255, 255), -1, 20))
        self.text.append(TextBox.TextBox(self.scr, 'а) викласти карту на стіл (ЛКМ по карті в руці)',                       (315, 230, 500, 270), (255, 255, 255), -1, 20))
        self.text.append(TextBox.TextBox(self.scr, 'б) якщо на столі є 3 чи 4 карти одного значення, взяти їх собі,',       (390, 270, 560, 310), (255, 255, 255), -1, 20))
        self.text.append(TextBox.TextBox(self.scr, 'виклавши на стіл відповідно 3 чи 4 карти з руки,',                      (377, 310, 500, 350), (255, 255, 255), -1, 20))
        self.text.append(TextBox.TextBox(self.scr, 'старші за значенням (ЛКМ по карті бажаного значення на столі)',         (460, 350, 575, 390), (255, 255, 255), -1, 20))
        self.text.append(TextBox.TextBox(self.scr, 'У кінці ходу гравець добирає карти з колоди до чотирьох.',              (350, 390, 550, 430), (255, 255, 255), -1, 20))
        self.text.append(TextBox.TextBox(self.scr, 'Гра закінчується, коли в колоді та в руках гравців більше немає карт.', (413, 430, 600, 470), (255, 255, 255), -1, 20))
        self.text.append(TextBox.TextBox(self.scr, 'Бали нараховуються так:',                                               (155, 470, 425, 510), (255, 255, 255), -1, 20))
        self.text.append(TextBox.TextBox(self.scr, 'Кожен набір по 3 карти - 1 бал',                                        (218, 510, 420, 550), (255, 255, 255), -1, 20))
        self.text.append(TextBox.TextBox(self.scr, 'Кожен набір по 4 карти - 2 бали',                                       (225, 550, 425, 590), (255, 255, 255), -1, 20))
        self.text.append(TextBox.TextBox(self.scr, 'Виграє той, хто має більше балів.',                                     (233, 590, 430, 630), (255, 255, 255), -1, 20))

        self.closeButton = Button.Button(self.mouse, self.scr, 'Назад', (840, 660, 1015, 730), (255, 255, 255), 2, 28)

    def update(self):
        self.title.update()
        for line in self.text:
            line.update()
        self.closeButton.update()

        if self.closeButton.isPressed:
            return 1
        else:
            return 0