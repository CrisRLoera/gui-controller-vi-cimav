from src.network_module.NetworkGUI import NetworkGUI
from src.state_module.StateGUI import StateGUI
from src.state_module.StateController import ControlFlow
from src.program_module.ProgramGUI import ProgramGUI
from src.edit_module.EditorGUI import EditorGUI
from src.file_load_controller import FileLoadController
from src.RecoveryController import RecoveryController
from src.network_module.EmailController import EmailController
from src.config_module.ConfigurationGUI import ConfigurationGUI
import nmcli
from customtkinter import CTk, CTkLabel, CTkButton, CTkToplevel,CTkFrame
#import RPi.GPIO as GPIO
import datetime

class MainApp:
    def __init__(self):
        self.gui_app = CTk()
        self.gui_app.geometry("800x480")
#        self.gui_app.attributes("-fullscreen", True)
        self.gui_app.grid_columnconfigure((0), weight=1)
        self.gui_app.grid_rowconfigure((0,2,3,4), weight=0)
        self.gui_app.grid_rowconfigure((1), weight=1)
        self.current_screen = ''
        
        self.file_controller = FileLoadController()
        self.recovery_controller = RecoveryController(self)
        self.state_controller = ControlFlow(self)
        self.email_controller = EmailController(self)

        self.data_frame = CTkFrame(self.gui_app)
        self.data_frame.grid_columnconfigure((0,1),weight=1)
        self.data_frame.grid_rowconfigure((0),weight=1)

        self.nav_frame = CTkFrame(self.gui_app)
        self.nav_frame.grid_columnconfigure((0,1,2),weight=1)
        self.nav_frame.grid_rowconfigure((0),weight=1)

        self.notify_frame = CTkFrame(self.gui_app)
        self.notify_frame.grid_columnconfigure((0),weight=1)
        self.notify_frame.grid_rowconfigure((0),weight=1)

        self.conf_screen = ConfigurationGUI(self.data_frame,self.nav_frame,self)
        self.network_screen = NetworkGUI(self.data_frame, self.nav_frame, self.notify_frame,self)
        self.state_screen = StateGUI(self.data_frame,self.nav_frame,self.notify_frame,self)
        self.editor_screen = EditorGUI(self.data_frame,self.nav_frame, self.notify_frame,self)
        self.program_screen = ProgramGUI(self.data_frame,self.nav_frame,self.notify_frame,self,self.state_screen,self.editor_screen)
        

        self.wifi_status_icon = '󰖪'
        self.current_time = datetime.datetime.now()
        
        self.hub_frame = CTkFrame(self.gui_app)
        self.hub_frame.grid_columnconfigure((0,1,2,3),weight=1)
        self.hub_frame.grid_rowconfigure((0),weight=1)
        self.time_hub = CTkLabel(self.hub_frame,text=f"{self.current_time}")
        self.wifi_status_hub = CTkButton(self.hub_frame,text=f'{self.wifi_status_icon}', command=self.changeToNetworkScreen)
        self.conf_hub = CTkButton(self.hub_frame, text="configuration", command=self.change_conf)

        self.current_screen = 'state'

        # Start up rutine
        self.recovery_controller.checkRecovery()
        self.update_Screen()
        self.check_connection()
        self.check_main_flow()
        self.check_reminder()

    def changeToNetworkScreen(self):
        self.current_screen = 'network'
        self.update_Screen()

    def change_conf(self):
        self.current_screen = 'conf'
        self.update_Screen()

    def isConnected(self):
        nmcli.disable_use_sudo()
        dev_list = nmcli.device.status()
        for dev in dev_list:
            if dev.connection != None and dev.device_type == 'wifi':
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
        self.current_time = datetime.datetime.now()
        self.update_hub()
        self.gui_app.after(1000, self.check_main_flow)

    def check_reminder(self):
        try:
            for device in self.file_controller.conf_file['maintenance devices']:
                if (device['use limit']*60)>= device['output on time']:
                    if device['last reminder']==None:                                 
                        self.email_controller.send_maintenance_email(self.file_controller.conf_file['maintenance'],device['name'])
                    else:
                        if (device['last reminder']-(datetime.datetime.now())).days >=7:
                            self.email_controller.send_maintenance_email(self.file_controller.conf_file['maintenance'],device['name'])
                    device['last reminder']=datetime.datetime.now()
                    self.file_controller.updateConf()
                    self.file_controller.loadConf()
        except:
            print("Unset reciver")
        self.gui_app.after(300000,self.check_reminder)

    def update_Screen(self):
        self.refresh_main_screen()
        self.hub_frame.grid(row=0,column=0,sticky="we")
        self.data_frame.grid(row=1,column=0,sticky="nswe")
        self.nav_frame.grid(row=2,column=0,sticky="we")
        self.notify_frame.grid(row=3,column=0,sticky="we")

        self.wifi_status_hub.grid(row=0,column=0)
        self.conf_hub.grid(row=0, column=1)
        self.time_hub.grid(row=0, column=2, columnspan=2)

        
        if self.current_screen == 'state':
            self.state_screen.update()
        elif self.current_screen == 'program':
            self.program_screen.update()
        elif self.current_screen == 'network':
            self.network_screen.update()
        elif self.current_screen == 'editor':
            self.editor_screen.update()
        elif self.current_screen == 'conf':
            self.conf_screen.update()
        

    def refresh_main_screen(self):
        for widget in self.gui_app.winfo_children():
            if isinstance(widget, CTkToplevel):
                pass
            elif isinstance(widget, CTkFrame):
                self.clear_frame(widget)
            else:
                widget.grid_forget()

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            if isinstance(widget, CTkFrame):
                self.clear_frame(widget)
            else:
                widget.grid_forget()
        frame.grid_forget()

    def update_hub(self):
        self.wifi_status_hub.configure(text=self.wifi_status_icon)
        self.time_hub.configure(text=self.current_time)

if __name__ == "__main__":
    try:
        main = MainApp()
        main.update_Screen()
        main.gui_app.mainloop()
    except:
        #GPIO.cleanup()
        pass

