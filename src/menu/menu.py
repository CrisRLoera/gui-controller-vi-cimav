from customtkinter import CTkLabel

class Menu:
    def __init__(self,app):
       self.title = CTkLabel(app, text='Menu')

    def update(self):
        self.title.pack()
