from src.network_module.NetworkGUI import NetworkGUI
from src.state_module.StateGUI import StateGUI
from src.state_module.StateController import ControlFlow
from src.program_module.ProgramGUI import ProgramGUI
from src.edit_module.EditorGUI import EditorGUI
from src.file_load_controller import FileLoadController
from src.RecoveryController import RecoveryController
import nmcli
from customtkinter import CTk, CTkLabel, CTkButton, CTkToplevel
import datetime

class MainApp:
    def __init__(self):
        self.gui_app = CTk()
        self.current_screen = ''
        
        self.file_controller = FileLoadController()
        self.recovery_controller = RecoveryController(self)

        self.network_screen = NetworkGUI(self.gui_app)
        self.state_screen = StateGUI(self.gui_app,self)
        self.state_controller = ControlFlow(self)
        self.editor_screen = EditorGUI(self.gui_app,self)
        self.program_screen = ProgramGUI(self.gui_app,self,self.state_screen,self.editor_screen)
        

        self.wifi_status_icon = '󰖪'
        self.current_time = datetime.datetime.now()
        self.time_hub = CTkLabel(self.gui_app,text=f"{self.current_time}")
        self.wifi_status_hub = CTkLabel(self.gui_app,text=f'{self.wifi_status_icon}')


        if self.isConnected():
            self.current_screen = 'state'
        else:
            self.current_screen = 'network'
        
        self.recovery_controller.checkRecovery()

    def isConnected(self):
        nmcli.disable_use_sudo()
        dev_list = nmcli.device.status()
        for dev in dev_list:
            if dev.state == 'connected' and dev.device_type == 'wifi':
                print("Connect")
                self.wifi_status_icon = '󰖩'
                self.update_hub()
                return True
        self.wifi_status_icon = '󰖪'
        self.update_hub()
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

    def check_time(self):
        if self.state_screen.program_state:
            #print(self.current_time)
            self.recovery_controller.checkClock(self.current_time)
            self.state_controller.checkCurrentFlow(self.state_screen.current_step_number)
            self.state_screen.update()
        self.current_time = datetime.datetime.now()
        self.update_hub()
        self.gui_app.after(1000, self.check_time)

    def update_Screen(self):
        self.refresh_main_screen()
        self.wifi_status_hub.pack()
        self.time_hub.pack()
        if self.current_screen == 'state':
            self.state_screen.update()
        elif self.current_screen == 'network':
            self.network_screen.update()
        elif self.current_screen == 'program':
            self.program_screen.update()
        elif self.current_screen == 'editor':
            self.editor_screen.update()
        self.check_connection()
        self.check_time()
        self.gui_app.mainloop()

    def refresh_main_screen(self):
        for widget in self.gui_app.winfo_children():
            if isinstance(widget, CTkToplevel):
                pass
            else:
                widget.pack_forget()

    def update_hub(self):
        self.wifi_status_hub.configure(text=self.wifi_status_icon)
        self.time_hub.configure(text=self.current_time)

if __name__ == "__main__":
    main = MainApp()
    main.update_Screen()
