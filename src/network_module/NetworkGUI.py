from .NetworkController import network_get_ssid_list, network_connect
from customtkinter import CTkLabel, CTkComboBox, CTkButton, CTkEntry, CTkToplevel

class NetworkGUI:
    def __init__(self,app):
        self.app = app
        self.network_view = None
        self.ssid_list = list(network_get_ssid_list())
        self.ssid = ''

    def selected_ssid(self,choice):
        self.ssid = choice

    def connect(self,pwd_entry):
        try:
            network_connect(self.ssid, pwd_entry.get())
        except:
            print("Network err")
        self.network_view.destroy()

    def update(self):
        self.network_view = CTkToplevel(self.app)
        title = CTkLabel(self.network_view, text='Network')
        ssid_combo = CTkComboBox(self.network_view, values=self.ssid_list, command=self.selected_ssid)
        ssid_combo.set('')
        pwd_txt = CTkLabel(self.network_view,text="Password")
        pwd_entry = CTkEntry(self.network_view,show="*")
        connect_button = CTkButton(self.network_view, text='Connect', command=lambda:self.connect(pwd_entry))
        title.pack()
        ssid_combo.pack()
        pwd_txt.pack()
        pwd_entry.pack()
        connect_button.pack()
