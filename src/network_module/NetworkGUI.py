from .NetworkController import network_get_ssid_list, network_connect
from customtkinter import CTkLabel, CTkComboBox, CTkButton, CTkEntry

class NetworkGUI:
    def __init__(self,app):
       self.title = CTkLabel(app, text='Net')
       self.ssid_list = list(network_get_ssid_list())
       self.ssid = ''
       self.ssid_combo = CTkComboBox(app, values=self.ssid_list, command=self.selected_ssid)
       self.ssid_combo.set('')
       self.pwd_entry = CTkEntry(app)
       self.connect_button = CTkButton(app, text='Connect', command=self.connect)

    def selected_ssid(self,choice):
        self.ssid = choice

    def connect(self):
       network_connect(self.ssid, self.pwd_entry.get()) 

    def update(self):
        self.title.pack()
        self.ssid_combo.pack()
        self.pwd_entry.pack()
        self.connect_button.pack()
    def send(self):
        send_email()
