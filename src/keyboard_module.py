from re import I
from customtkinter import CTkFrame,CTkButton

class VirtualKeyboard(CTkFrame):
    def __init__(self, parent, entry_widget, host):
        super().__init__(parent)
        self.host = host
        self.entry_widget = entry_widget
        self.shift_pressed = False
        self.create_keyboard()

    def create_keyboard(self):
        self.keys_lower = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Backspace'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'Close'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '@', 'Space'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm', '.', '_', '-', 'Shift']
        ]
        self.keys_upper = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Backspace'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'Close'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', '@', 'Space'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '.', '_', '-', 'Shift']
        ]
        self.draw_keyboard()

    def draw_keyboard(self):
        # Limpiar el teclado existente

        # Seleccionar la lista de teclas basada en el estado de Shift
        keys = self.keys_upper if self.shift_pressed else self.keys_lower

        # Crear los botones del teclado
        for y, row in enumerate(keys):
            for x, key in enumerate(row):
                if key == 'Space':
                    button = CTkButton(self, text='',image=self.host.file_controller.icons['space'], command=lambda k=key: self.on_key_press(k), fg_color="#dad8e5", hover_color="#c1bed2",width=30,height=30, border_color="#3d3846", border_width=2, text_color="black")
                elif key == 'Shift':
                    button = CTkButton(self, text='',image=self.host.file_controller.icons['shift'], command=self.toggle_shift, fg_color="#dad8e5", hover_color="#c1bed2",width=30,height=30, border_color="#3d3846", border_width=2, text_color="black")
                elif key == 'Close':
                    button = CTkButton(self, text='',image=self.host.file_controller.icons['arrow-down'], command=lambda k=key: self.on_key_press(k), fg_color="#dad8e5", hover_color="#c1bed2",width=30,height=30, border_color="#3d3846", border_width=2, text_color="black")
                elif key == 'Backspace':
                    button = CTkButton(self, text='',image=self.host.file_controller.icons['backspace'], command=lambda k=key: self.on_key_press(k), fg_color="#dad8e5", hover_color="#c1bed2",width=30,height=30, border_color="#3d3846", border_width=2, text_color="black")
                else:
                    button = CTkButton(self, text=key, command=lambda k=key: self.on_key_press(k), fg_color="#dad8e5", hover_color="#c1bed2",width=30,height=30, border_color="#3d3846", border_width=2, text_color="black")
                button.grid(row=y, column=x, padx=2, pady=2)

    def on_key_press(self, key):
        current_text = self.entry_widget.get()
        if key == 'Backspace':
            self.entry_widget.delete(len(current_text) - 1, 'end')
        elif key == 'Space':
            self.entry_widget.insert('end', ' ')
        elif key == 'Close':
            self.destroy()
        else:
            self.entry_widget.insert('end', key)
        #if self.shift_pressed and key != 'Shift':
        #    self.toggle_shift()
    def toggle_shift(self):
        self.shift_pressed = not self.shift_pressed
        self.draw_keyboard()
    
class VirtualNumKeyboard(CTkFrame):
    def __init__(self, parent, entry_widget, host):
        super().__init__(parent)
        self.host = host
        self.entry_widget = entry_widget
        self.create_keyboard()

    def create_keyboard(self):
        keys = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['0', 'Close', 'Backspace' ]
        ]

        for y, row in enumerate(keys):
            for x, key in enumerate(row):
                if key == 'Close':
                    button = CTkButton(self, text='',image=self.host.file_controller.icons['arrow-down'], command=lambda k=key: self.on_key_press(k), fg_color="#dad8e5", hover_color="#c1bed2",width=30,height=30, border_color="#3d3846", border_width=2, text_color="black")
                elif key == 'Backspace':
                    button = CTkButton(self, text='',image=self.host.file_controller.icons['backspace'], command=lambda k=key: self.on_key_press(k), fg_color="#dad8e5", hover_color="#c1bed2",width=30,height=30, border_color="#3d3846", border_width=2, text_color="black")
                else:
                    button = CTkButton(self, text=key, command=lambda k=key: self.on_key_press(k), fg_color="#dad8e5", hover_color="#c1bed2",width=30,height=30, border_color="#3d3846", border_width=2, text_color="black")
                button.grid(row=y, column=x, padx=2, pady=2)

    def on_key_press(self, key):
        current_text = self.entry_widget.get()
        if key == 'Backspace':
            self.entry_widget.delete(len(current_text) - 1, 'end')
        elif key == 'Close':
            self.destroy()
        else:
            self.entry_widget.insert('end', key)
