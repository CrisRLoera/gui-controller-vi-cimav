from .NetworkController import network_get_ssid_list, network_connect
from customtkinter import CTkLabel, CTkComboBox, CTkButton, CTkEntry, CTkFrame
from src.keyboard_module import VirtualKeyboard

class NetworkGUI:
    def __init__(self,data,nav,host):
        self.host = host
        self.network_view = None
        self.ssid_list = list(network_get_ssid_list())
        self.ssid = ''
        
        self.network_view = CTkFrame(data)
        self.network_view.grid_rowconfigure((0,1,2,3,4,5),weight=1)
        self.network_view.grid_columnconfigure((0),weight=1)
        self.keyboard_frame = None

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
        self.ssid_combo = CTkComboBox(self.network_view, values=self.ssid_list, command=self.selected_ssid)
        self.ssid_combo.set('')
        self.ssid_combo.bind("<Button-1>",self.show_kb_ssid)
        pwd_txt = CTkLabel(self.network_view,text="Password")
        self.pwd_entry = CTkEntry(self.network_view,show="*")
        self.pwd_entry.bind("<Button-1>",self.show_kb_psw)
        connect_button = CTkButton(self.network_view, text='Connect', command=lambda:self.connect(self.pwd_entry))
        back_button = CTkButton(self.network_view, text='Back', command=self.go_back)
        title.grid(row=0,column=0)
        self.ssid_combo.grid(row=1,column=0)
        pwd_txt.grid(row=2,column=0)
        self.pwd_entry.grid(row=3,column=0)
        connect_button.grid(row=4,column=0)
        back_button.grid(row=5,column=0)

    def show_kb_ssid(self,event):
        if self.keyboard_frame is not None:
            self.keyboard_frame.destroy()
        self.keyboard_frame = VirtualKeyboard(self.host.gui_app, self.ssid_combo)
        self.keyboard_frame.grid(row=4,column=0)

    def show_kb_psw(self,event):
        if self.keyboard_frame is not None:
            self.keyboard_frame.destroy()
        self.keyboard_frame = VirtualKeyboard(self.host.gui_app, self.pwd_entry)
        self.keyboard_frame.grid(row=4,column=0)
