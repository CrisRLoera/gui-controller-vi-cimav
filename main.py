from src.network_module.NetworkGUI import NetworkGUI
from src.state_module.StateGUI import StateGUI
from src.state_module.StateController import ControlFlow
from src.program_module.ProgramGUI import ProgramGUI
from src.edit_module.EditorGUI import EditorGUI
from src.file_load_controller import FileLoadController
from src.RecoveryController import RecoveryController
from src.network_module.EmailController import EmailController
from src.config_module.ConfigureGUI import ConfigureGUI
import nmcli
from customtkinter import CTk, CTkLabel, CTkButton, CTkToplevel
import datetime

class MainApp:
    def __init__(self):
        self.gui_app = CTk()
        self.gui_app.geometry("800x480")
#        self.gui_app.attributes("-fullscreen", True)
        self.current_screen = ''
        
        self.file_controller = FileLoadController()
        self.recovery_controller = RecoveryController(self)

        self.network_screen = NetworkGUI(self.gui_app)
        self.email_controller = EmailController(self)
        self.state_screen = StateGUI(self.gui_app,self)
        self.state_controller = ControlFlow(self)
        self.editor_screen = EditorGUI(self.gui_app,self)
        self.program_screen = ProgramGUI(self.gui_app,self,self.state_screen,self.editor_screen)
        

        self.wifi_status_icon = '󰖪'
        self.current_time = datetime.datetime.now()
        self.time_hub = CTkLabel(self.gui_app,text=f"{self.current_time}")
        self.wifi_status_hub = CTkButton(self.gui_app,text=f'{self.wifi_status_icon}', command=self.network_screen.update)
        self.conf_screen = ConfigureGUI(self.gui_app,self)
        self.conf_hub = CTkButton(self.gui_app, text="configuration", command=self.conf_screen.update)

        self.current_screen = 'state'

        self.recovery_controller.checkRecovery()
        self.update_Screen()
        self.check_connection()
        self.check_main_flow()
        self.check_reminder()

    def isConnected(self):
        nmcli.disable_use_sudo()
        dev_list = nmcli.device.status()
        for dev in dev_list:
            if dev.state == 'connected' and dev.device_type == 'wifi':
                print("Connect")
                self.wifi_status_icon = 'connect'
                self.update_hub()
                return True
        self.wifi_status_icon = 'disconnected'
        self.update_hub()
        return False

    def check_connection(self):
        self.isConnected()
        self.gui_app.after(5000, self.check_connection)

    def check_main_flow(self):
        if self.state_screen.program_state:
            self.recovery_controller.checkClock(self.current_time)
            self.state_controller.checkCurrentFlow(self.state_screen.current_step_number)
            self.state_controller.trackOutputs()
            self.refresh_main_screen()
            self.state_screen.update()
        self.current_time = datetime.datetime.now()
        self.update_hub()
        self.gui_app.after(1000, self.check_main_flow)

    def check_reminder(self):
        try:
            for device in self.file_controller.conf_file['maintenance devices']:
                if (device['use limit']*60)>= self.file_controller.conf_file['output1 on time']:
                    if device['last reminder']==None:                                 
                        self.email_controller.send_maintenance_email(self.file_controller.conf_file['maintenance'],device['name'])
                    else:
                        if (device['last reminder']-(datetime.datetime.now())).days >=7:
                            self.email_controller.send_maintenance_email(self.file_controller.conf_file['maintenance'],device['name'])
                    device['last reminder']=datetime.datetime.now()
                    self.file_controller.updateConf()
                    self.file_controller.loadConf()
        except:
            print("Un set reciver")
        self.gui_app.after(300000,self.check_reminder)

    def update_Screen(self):
        self.refresh_main_screen()
        self.wifi_status_hub.pack()
        self.conf_hub.pack()
        self.time_hub.pack()
        if self.current_screen == 'state':
            self.state_screen.update()
        elif self.current_screen == 'program':
            self.program_screen.update()
        elif self.current_screen == 'editor':
            self.editor_screen.update()
        

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
    main.gui_app.mainloop()
