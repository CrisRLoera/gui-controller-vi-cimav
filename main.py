from sys import exec_prefix
from customtkinter.windows.widgets import font
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
from customtkinter import CTk, CTkLabel, CTkButton, CTkToplevel,CTkFrame,FontManager, CTkFont
#import RPi.GPIO as GPIO
import datetime

class MainApp:
    def __init__(self):
        self.gui_app = CTk()
        FontManager.load_font("./src/font/Inter.ttf")
        self.gui_app.geometry("800x480")
#        self.gui_app.attributes("-fullscreen", True)
        self.gui_app.grid_columnconfigure((0), weight=1)
        self.gui_app.grid_rowconfigure((0,2,3,4), weight=0)
        self.gui_app.grid_rowconfigure((1), weight=1)
        self.current_screen = ''
        self.def_font = CTkFont(family="Inter",size=20)
        
        self.file_controller = FileLoadController()
        self.recovery_controller = RecoveryController(self)
        self.state_controller = ControlFlow(self)
        self.email_controller = EmailController(self)

        self.data_frame = CTkFrame(self.gui_app)
        self.data_frame.grid_columnconfigure((0,1),weight=1)
        self.data_frame.grid_rowconfigure((0),weight=1)

        self.nav_frame = CTkFrame(self.gui_app,fg_color="#F5F5F9")
        self.nav_frame.grid_columnconfigure((0,1,2),weight=1)
        self.nav_frame.grid_rowconfigure((0),weight=1)

        self.notify_frame = CTkFrame(self.gui_app,fg_color="#F5F5F9")
        self.notify_frame.grid_columnconfigure((0),weight=1)
        self.notify_frame.grid_rowconfigure((0),weight=1)

        self.conf_screen = ConfigurationGUI(self.data_frame,self.nav_frame,self)
        self.network_screen = NetworkGUI(self.data_frame, self.nav_frame, self.notify_frame,self)
        self.state_screen = StateGUI(self.data_frame,self.nav_frame,self.notify_frame,self)
        self.editor_screen = EditorGUI(self.data_frame,self.nav_frame, self.notify_frame,self)
        self.program_screen = ProgramGUI(self.data_frame,self.nav_frame,self.notify_frame,self,self.state_screen,self.editor_screen)
        

        self.wifi_status_icon = self.file_controller.icons['wifi-problem']
        self.current_time = datetime.datetime.now()
        
        self.hub_frame = CTkFrame(self.gui_app,fg_color="#F5F5F9")
        self.hub_frame.grid_columnconfigure((0,1),weight=0)
        self.hub_frame.grid_columnconfigure((2,3),weight=1)
        self.hub_frame.grid_rowconfigure((0),weight=1)
        self.time_hub = CTkLabel(self.hub_frame,text=f"{self.current_time}",font=self.def_font)
        self.wifi_status_hub = CTkButton(self.hub_frame, command=self.changeToNetworkScreen, image=self.wifi_status_icon, text='', fg_color="#dad8e5", hover_color="#c1bed2",width=40,height=40)
        self.conf_hub = CTkButton(self.hub_frame, command=self.changeToConfScreen,image=self.file_controller.icons['configuration'],text='', fg_color="#dad8e5", hover_color="#c1bed2",width=40,height=40)

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

    def changeToConfScreen(self):
        self.current_screen = 'conf'
        self.conf_screen.get_devices()
        self.update_Screen()

    def isConnected(self):
        nmcli.disable_use_sudo()
        dev_list = nmcli.device.status()
        for dev in dev_list:
            if dev.connection != None and dev.device_type == 'wifi':
                self.wifi_status_icon = self.file_controller.icons['wifi-high']
                self.wifi_status_hub.configure(fg_color="#25f648", hover_color="#06f432")
                self.update_hub()
                return True
        self.wifi_status_icon = self.file_controller.icons['wifi-problem']
        self.wifi_status_hub.configure(fg_color="#f63d45", hover_color="#e01b24")
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
                if (device['use limit']*60)<= device['output on time']:
                    if device['last reminder']==None:                                 
                        self.email_controller.send_maintenance_email(self.file_controller.conf_file['maintenance'],device['name'])
                    else:
                        last_reminder = datetime.datetime.strptime(device['last reminder'], '%Y-%m-%d %H:%M:%S')
                        if (last_reminder-(datetime.datetime.now())).days >=7:
                            print("OK")
                            self.email_controller.send_maintenance_email(self.file_controller.conf_file['maintenance'],device['name'])
                    device['last reminder']=str(datetime.datetime.now().replace(microsecond=0))
                    self.file_controller.updateConf()
                    self.file_controller.loadConf()
                    print("Okeeeeey")
        except Exception as e:
            print(f"Error in Chech reminder{e}")

        self.gui_app.after(300000,self.check_reminder)

    def update_Screen(self):
        self.refresh_main_screen()
        self.hub_frame.grid(row=0,column=0,sticky="we")
        self.data_frame.grid(row=1,column=0,sticky="nswe")
        self.nav_frame.grid(row=2,column=0,sticky="we")
        self.notify_frame.grid(row=3,column=0,sticky="we")

        self.wifi_status_hub.grid(row=0,column=0,pady=(5,0),padx=(5,0),sticky="w")
        self.conf_hub.grid(row=0, column=1, pady=(5,0),padx=(5,0),sticky="w")
        self.time_hub.grid(row=0, column=2, columnspan=2, sticky="e",padx=(0,5))

        
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
        self.wifi_status_hub.configure(image=self.wifi_status_icon)
        self.time_hub.configure(text=self.current_time.strftime("%A %d-%m-%Y %H:%M"))

if __name__ == "__main__":
    try:
        main = MainApp()
        main.update_Screen()
        main.gui_app.mainloop()
    except:
        #GPIO.cleanup()
        pass

