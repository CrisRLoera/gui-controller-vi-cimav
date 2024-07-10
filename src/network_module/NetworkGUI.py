from customtkinter.windows.widgets import font
from .NetworkController import network_get_ssid_list, network_connect
from customtkinter import CTkLabel, CTkComboBox, CTkButton, CTkEntry, CTkFrame, CTkFont
from src.keyboard_module import VirtualKeyboard

class NetworkGUI:
    def __init__(self,data,nav,notify,host):
        self.host = host
        self.ssid_list = list(network_get_ssid_list())
        self.ssid = ''
        self.def_font = self.host.def_font
        self.drop_font =CTkFont(family="Inter",size=15)
        
        self.network_view = CTkFrame(data, fg_color="#F5F5F9")
        self.network_view.grid_rowconfigure((0,1,2,3,4,5),weight=1)
        self.network_view.grid_columnconfigure((0),weight=1)
        self.keyboard_frame = None
        self.err_network_label = CTkLabel(notify,text="Error: Can´t connect to the network", image=self.host.file_controller.icons['alert'],font=self.def_font, compound="left")
        self.err_net = False

    def selected_ssid(self,choice):
        self.ssid = choice

    def connect(self,pwd_entry):
        try:
            network_connect(self.ssid, pwd_entry.get())
            self.err_net = False
            self.host.current_screen="state"
            self.host.update_Screen()
        except:
            self.err_net = True
            self.update()

    def go_back(self):
        self.host.current_screen="state"
        self.host.update_Screen()

    def update(self):
        self.network_view.grid(row=0,column=0,columnspan=2, sticky="nswe")
        title = CTkLabel(self.network_view, text='Network',font=self.def_font)
        self.ssid_combo = CTkComboBox(self.network_view, values=self.ssid_list, command=self.selected_ssid,  width=200, height=40,fg_color="#dad8e5",button_color="#625875", button_hover_color="#50495f", text_color="black",dropdown_text_color="black", dropdown_font=self.drop_font)
        self.ssid_combo.set('')
        self.ssid_combo.bind("<Button-1>",self.show_kb_ssid)
        pwd_txt = CTkLabel(self.network_view,text="Password", font=self.def_font)
        self.pwd_entry = CTkEntry(self.network_view,show="*",font=self.def_font,height=40)
        self.pwd_entry.bind("<Button-1>",self.show_kb_psw)
        connect_button = CTkButton(self.network_view, text='Connect', command=lambda:self.connect(self.pwd_entry), font=self.def_font, width=100, height=40,fg_color="#06f432",hover_color="#25f648", border_color="#3d3846", border_width=2, text_color="black")
        back_button = CTkButton(self.network_view, text='Back', command=self.go_back, font=self.def_font, width=100, height=40,fg_color="#dad8e5", hover_color="#c1bed2", border_color="#3d3846", border_width=2, text_color="black")
        title.grid(row=0,column=0)
        self.ssid_combo.grid(row=1,column=0,pady=(0,10))
        pwd_txt.grid(row=2,column=0)
        self.pwd_entry.grid(row=3,column=0,pady=(0,10))
        connect_button.grid(row=4,column=0, pady=(0,5))
        back_button.grid(row=5,column=0)
        if self.err_net:
            self.err_network_label.grid(row=0,column=0)
        else:
            self.err_network_label.grid_forget()

    def show_kb_ssid(self,event):
        if self.keyboard_frame is not None:
            self.keyboard_frame.destroy()
        self.keyboard_frame = VirtualKeyboard(self.host.gui_app, self.ssid_combo, self.host)
        self.keyboard_frame.grid(row=4,column=0)

    def show_kb_psw(self,event):
        if self.keyboard_frame is not None:
            self.keyboard_frame.destroy()
        self.keyboard_frame = VirtualKeyboard(self.host.gui_app, self.pwd_entry, self.host)
        self.keyboard_frame.grid(row=4,column=0)
