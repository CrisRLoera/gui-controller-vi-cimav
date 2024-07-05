from .NetworkController import network_get_ssid_list, network_connect
from customtkinter import CTkLabel, CTkComboBox, CTkButton, CTkEntry, CTkFrame

class NetworkGUI:
    def __init__(self,data,nav,host):
        self.host = host
        self.network_view = None
        self.ssid_list = list(network_get_ssid_list())
        self.ssid = ''
        
        self.network_view = CTkFrame(data)
        self.network_view.grid_rowconfigure((0,1,2,3,4,5),weight=1)
        self.network_view.grid_columnconfigure((0),weight=1)

    def selected_ssid(self,choice):
        self.ssid = choice

    def connect(self,pwd_entry):
        try:
            network_connect(self.ssid, pwd_entry.get())
        except:
            print("Network err")
        self.host.current_screen="state"
        self.host.update_Screen()

    def go_back(self):
        self.host.current_screen="state"
        self.host.update_Screen()

    def update(self):
        self.network_view.grid(row=0,column=0,columnspan=2)
        title = CTkLabel(self.network_view, text='Network')
        ssid_combo = CTkComboBox(self.network_view, values=self.ssid_list, command=self.selected_ssid)
        ssid_combo.set('')
        pwd_txt = CTkLabel(self.network_view,text="Password")
        pwd_entry = CTkEntry(self.network_view,show="*")
        connect_button = CTkButton(self.network_view, text='Connect', command=lambda:self.connect(pwd_entry))
        back_button = CTkButton(self.network_view, text='Back', command=self.go_back)
        title.grid(row=0,column=0)
        ssid_combo.grid(row=1,column=0)
        pwd_txt.grid(row=2,column=0)
        pwd_entry.grid(row=3,column=0)
        connect_button.grid(row=4,column=0)
        back_button.grid(row=5,column=0)
