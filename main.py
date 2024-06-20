from src.network_module.NetworkGUI import NetworkGUI
from src.menu.menu import Menu
import nmcli
from customtkinter import CTk, CTkButton

class MainApp:
    def __init__(self):
        self.gui_app = CTk()
        self.current_screen = ''
        
        self.network_screen = NetworkGUI(self.gui_app)
        self.menu_screen = Menu(self.gui_app)

        if self.isConnected():
            self.current_screen = 'menu'
        else:
            self.current_screen = 'network'


    def isConnected(self):
        nmcli.disable_use_sudo()
        dev_list = nmcli.device.status()
        for dev in dev_list:
            if dev.state == 'connected' and dev.device_type == 'wifi':
                print("Connect")
                return True
        return False

    def check_connection(self):
        if self.current_screen == 'network' and self.isConnected():
            self.current_screen = 'menu'
            for widget in self.gui_app.winfo_children():
                widget.pack_forget()
            self.menu_screen.update()
        elif self.current_screen == 'menu' and not self.isConnected():
            self.current_screen = 'network'
            for widget in self.gui_app.winfo_children():
                widget.pack_forget()
            self.network_screen.update()
        self.gui_app.after(5000, self.check_connection)

    def update_Screen(self):
        if self.current_screen == 'menu':
            self.menu_screen.update()
        elif self.current_screen == 'network':
            self.network_screen.update()
        self.check_connection()
        self.gui_app.mainloop()


if __name__ == "__main__":
    main = MainApp()
    main.update_Screen()
