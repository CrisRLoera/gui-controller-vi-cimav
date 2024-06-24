from src.network_module.NetworkGUI import NetworkGUI
from src.state_module.StateGUI import StateGUI
from src.program_module.ProgramGUI import ProgramGUI
from src.file_load_controller import FileLoadController
import nmcli
from customtkinter import CTk, CTkButton

class MainApp:
    def __init__(self):
        self.gui_app = CTk()
        self.current_screen = ''
        
        self.file_controller = FileLoadController()

        self.network_screen = NetworkGUI(self.gui_app)
        self.state_screen = StateGUI(self.gui_app,self)
        self.program_screen = ProgramGUI(self.gui_app,self,self.state_screen)
        


        if self.isConnected():
            self.current_screen = 'state'
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
            self.current_screen = 'state'
            self.refresh_main_screen()
            self.state_screen.update()
        elif self.current_screen == 'state' and not self.isConnected():
            self.current_screen = 'network'
            self.refresh_main_screen()
            self.network_screen.update()
        self.gui_app.after(5000, self.check_connection)

    def update_Screen(self):
        self.refresh_main_screen()
        if self.current_screen == 'state':
            self.state_screen.update()
            print("Hi")
        elif self.current_screen == 'network':
            self.network_screen.update()
        elif self.current_screen == 'program':
            self.program_screen.update()
            
        self.check_connection()
        self.gui_app.mainloop()

    def refresh_main_screen(self):
        for widget in self.gui_app.winfo_children():
            widget.pack_forget()

if __name__ == "__main__":
    main = MainApp()
    main.update_Screen()
