import collections
from re import S
from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkButton, CTkOptionMenu, CTkFrame, CTkFont
from src.keyboard_module import VirtualKeyboard, VirtualNumKeyboard
from tkinter import StringVar

class Device:
    def __init__(self,app,host,name,limit,output,last,time):
        self.name = name
        self.limit = limit
        self.output = output
        self.host = host
        self.time = time
        self.output_list = ["output1","output2","output3"]
        self.last = last
        self.onDeleted = False
        

    def getValues(self):
        return self.name,self.limit,self.output

    def destroy(self):
        self.onDeleted = True
        self.host.gen_pack()

    def mainteined(self,i):
        try:
            for index,device in enumerate(self.host.devices):
                print(index,device)
                if index == i:
                    print("get")
                    self.host.host.file_controller.conf_file['maintenance devices'][index]["output on time"]=0
                    self.host.host.file_controller.conf_file['maintenance devices'][index]['last reminder'] = None
                    self.host.host.file_controller.updateConf()
                    self.host.host.file_controller.loadConf()
                    self.host.get_devices()
        except:
            print("Device not found")

class ConfigurationGUI:
    def __init__ (self,data,nav,host):
        self.host = host
        self.edition_mode = False
        self.output_list = ["output1","output2","output3"]
        self.conf_file = self.host.file_controller.conf_file
        self.main_app = CTkFrame(data, fg_color="#F5F5F9")
        self.def_font = self.host.def_font
        self.drop_font = CTkFont(family="Inter", size=15)
        self.main_app.grid_columnconfigure((0,1),weight=1)
        self.main_app.grid_rowconfigure((0),weight=1)
        self.conf_view = CTkFrame(self.main_app,fg_color="#F5F5F9")
        self.conf_view.grid_columnconfigure((0),weight=1)
        self.conf_view.grid_rowconfigure((0,1,2,3,4,5,6,7,8),weight=1)
        self.dev_view = CTkFrame(self.main_app, fg_color="#F5F5F9")
        self.dev_view.grid_columnconfigure((0,1,2),weight=1)
        self.dev_view.grid_rowconfigure((0,1,2,3,4,5,6),weight=1)
        self.smtp_label = CTkLabel(self.conf_view, text="SMTP Server", font=self.def_font)
        self.smtp_entry = CTkEntry(self.conf_view, font=self.def_font,  height=40, width=300)
        self.smtp_entry.bind("<Button-1>",self.show_kb_smtp)
        self.port = CTkLabel(self.conf_view, text="Port", font=self.def_font)
        self.port_entry = CTkEntry(self.conf_view, font=self.def_font, height=40)
        self.port_entry.bind("<Button-1>",self.show_nkb_port)
        self.sender_label = CTkLabel(self.conf_view, text="Sender", font=self.def_font)
        self.sender_entry = CTkEntry(self.conf_view, font=self.def_font,height=40, width=300)
        self.sender_entry.bind("<Button-1>",command=self.show_kb_sender)
        self.maintenance_email_label = CTkLabel(self.conf_view, text="Maintenance email", font=self.def_font)
        self.maintenance_email_entry = CTkEntry(self.conf_view, font=self.def_font, height=40, width=300)
        self.maintenance_email_entry.bind("<Button-1>",self.show_kb_ma_email)

        self.devices_label = CTkLabel(self.dev_view, text="Devices", font=self.def_font)

        self.edit_mode = CTkButton(self.dev_view,text="",image=self.host.file_controller.icons['edit'], command=self.enable_edit_mode, font=self.def_font, fg_color="#dad8e5", hover_color="#c1bed2",width=40,height=40, border_color="#3d3846", border_width=2, text_color="black")
        self.add_device_button = CTkButton(self.dev_view,text="",image=self.host.file_controller.icons['add'], command=self.add_device, font=self.def_font, fg_color="#dad8e5", hover_color="#c1bed2",width=40,height=40, border_color="#3d3846", border_width=2, text_color="black")
        self.exit_edit_mode = CTkButton(self.dev_view,text="",image=self.host.file_controller.icons['cancel'], command=self.disable_edit_mode, font=self.def_font, fg_color="#dad8e5", hover_color="#c1bed2",width=40,height=40, border_color="#3d3846", border_width=2, text_color="black")
        
        self.device_name_label=CTkLabel(self.dev_view,text="Device name:", font=self.def_font)
        self.device_name=CTkLabel(self.dev_view, font=self.def_font)
        self.device_name_entry = CTkEntry(self.dev_view, font=self.def_font, height=40)
        self.device_name_entry.bind("<Button-1>",self.show_kb_dev_name)

        self.device_lT_label=CTkLabel(self.dev_view,text="Device limit:", font=self.def_font)
        self.device_lT=CTkLabel(self.dev_view, font=self.def_font)
        self.device_lT_entry= CTkEntry(self.dev_view, font=self.def_font)
        self.device_lT_entry.bind("<Button-1>",self.show_kb_dev_it)

        self.device_output_label=CTkLabel(self.dev_view,text="Device output:", font=self.def_font)
        self.device_output=CTkLabel(self.dev_view, font=self.def_font)

        self.device_output_option = CTkOptionMenu(self.dev_view,values=self.output_list, font=self.def_font, width=200, height=40,fg_color="#dad8e5",button_color="#625875", button_hover_color="#50495f", text_color="black",dropdown_text_color="black", dropdown_font=self.drop_font) 

        self.save_device_button = CTkButton(self.dev_view,text="",image=self.host.file_controller.icons['confirm'], command=self.save_device, font=self.def_font, fg_color="#dad8e5", hover_color="#c1bed2",width=40,height=40, border_color="#3d3846", border_width=2, text_color="black")
        self.delete_device_button = CTkButton(self.dev_view,text="",image=self.host.file_controller.icons['delete'], command=self.delete_device, font=self.def_font, fg_color="#dad8e5", hover_color="#c1bed2",width=40,height=40, border_color="#3d3846", border_width=2, text_color="black")
        self.maintenance_button = CTkButton(self.dev_view,text="Done",command=self.maintenance, font=self.def_font, width=100, height=40,fg_color="#dad8e5", hover_color="#c1bed2", border_color="#3d3846", border_width=2, text_color="black")
        self.save_edit_mode = CTkButton(nav,text="save all changes", command=self.save_edition, font=self.def_font, width=100, height=40,fg_color="#dad8e5", hover_color="#c1bed2", border_color="#3d3846", border_width=2, text_color="black")
        self.close_button = CTkButton(nav,text="Close",command=self.close_window, font=self.def_font, width=100, height=40,fg_color="#dad8e5", hover_color="#c1bed2", border_color="#3d3846", border_width=2, text_color="black")

        self.err_save = CTkLabel(self.host.notify_frame,text="Error: Can't save the configuration",image=host.file_controller.icons['alert'],compound="left")

        self.current_device=0
        
        self.get_devices()
        self.keyboard_frame = None
    

    def maintenance(self):
        self.devices[self.current_device].mainteined(self.current_device)

    def update(self):
        self.smtp_entry.configure(textvariable=StringVar(value=''))
        self.smtp_entry.insert(0,self.conf_file['host'])
        self.port_entry.configure(textvariable=StringVar(value=''))
        self.port_entry.insert(0,self.conf_file['port']) 
        self.sender_entry.configure(textvariable=StringVar(value=''))
        self.sender_entry.insert(0,self.conf_file['sender'])
        self.maintenance_email_entry.configure(textvariable=StringVar(value=''))
        self.maintenance_email_entry.insert(0,self.conf_file['maintenance'])
        
        

        self.gen_pack()

    def get_devices(self):
        self.devices = []
        try:
            for device in self.host.file_controller.conf_file["maintenance devices"]:
                self.devices.append(Device(self.conf_view,self,device['name'],device['use limit'],device['output'],device['last reminder'],device['output on time']))
        except:
            self.devices.append(Device(self.conf_view,self,"",0,"",None,0))
            print("No devices available")
    def close_window(self):
        self.edition_mode = False
        self.get_devices()
        self.host.current_screen = "state"
        self.host.update_Screen()

    def enable_edit_mode(self):
        self.edition_mode = True
        self.host.update_Screen()
        #self.gen_pack()

    def disable_edit_mode(self):
        self.edition_mode = False
        self.host.update_Screen()
        #self.gen_pack()

    def save_device(self):
        try:
            self.devices[self.current_device].name=self.device_name_entry.get()
            self.devices[self.current_device].limit=int(self.device_lT_entry.get())
            self.devices[self.current_device].output=self.device_output_option.get()
            self.disable_edit_mode()
            self.host.update_Screen()
        except:
            print("ERR: save device aborted")
    def delete_device(self):
        if self.devices[self.current_device].onDeleted:
            self.devices[self.current_device].onDeleted = False
        else:
            self.devices[self.current_device].onDeleted = True
        self.host.update_Screen()
    
    def save_edition(self):
        try:
            dev_list = []
            for device in self.devices:
                value = device.getValues()
                if not device.onDeleted:
                    dev_list.append({"name":device.name,"use limit":int(device.limit),"output":device.output,'last reminder':device.last,'output on time':device.time})
            self.host.file_controller.conf_file["host"]=self.smtp_entry.get()
            self.host.file_controller.conf_file["port"]=self.port_entry.get()
            self.host.file_controller.conf_file["sender"]=self.sender_entry.get()
            self.host.file_controller.conf_file["maintenance"]=self.maintenance_email_entry.get()
            self.host.file_controller.conf_file["maintenance devices"] = dev_list
            self.host.file_controller.updateConf()
            self.host.file_controller.loadConf()
            self.disable_edit_mode()
            self.get_devices()
            self.gen_pack()
            self.err_save.grid_forget()
        except:
            self.err_save.grid(row=0, column=0)
            print("ERR: save edition configuration")

    def add_device(self):
        self.devices.append(Device(self.conf_view,self.host,'','','',None,0))
        self.gen_pack()

    def gen_pack(self):
        self.refresh()
        self.main_app.grid(row=0,column=0,columnspan=2,sticky="nswe")
        self.conf_view.grid(row=0,column=0,sticky="nswe")
        self.dev_view.grid(row=0,column=1,sticky="nswe")
        self.smtp_label.grid(row=0,column=0)
        self.smtp_entry.grid(row=1,column=0)
        self.port.grid(row=2,column=0)
        self.port_entry.grid(row=3,column=0)
        self.sender_label.grid(row=4,column=0)
        self.sender_entry.grid(row=5,column=0)
        self.maintenance_email_label.grid(row=7,column=0)
        self.maintenance_email_entry.grid(row=8,column=0)

        self.devices_label.grid(row=0,column=1)
        self.total_devices=CTkLabel(self.dev_view, font=self.def_font)
        self.total_devices.configure(text=f"Total devices: {len(self.devices)}")
        self.total_devices.grid(row=1,column=1)
        self.current_device_label=CTkLabel(self.dev_view, font=self.def_font)
        self.current_device_label.configure(text=f"Current device: {self.current_device+1}")
        self.current_device_label.grid(row=2,column=1)
        self.next_device_button = CTkButton(self.dev_view,command=self.next_device, image=self.host.file_controller.icons['right'],text='', fg_color="#dad8e5", hover_color="#c1bed2",width=40,height=40)
        self.next_device_button.grid(row=2,column=2,sticky="w")
        self.back_device_button = CTkButton(self.dev_view,command=self.back_device, image=self.host.file_controller.icons['left'],text='', fg_color="#dad8e5", hover_color="#c1bed2",width=40,height=40)
        self.back_device_button.grid(row=2,column=0, sticky="e")

        self.device_name_label.grid(row=3,column=0)
        
        self.device_lT_label.grid(row=4,column=0)
        self.device_output_label.grid(row=5,column=0)
        
        if self.edition_mode:
            self.e_view()
        else:
            self.n_view()
        self.save_edit_mode.grid(row=0,column=0)
        self.close_button.grid(row=0,column=2)

    def next_device(self):
        if self.current_device < len(self.devices)-1:
            self.current_device +=1
            self.gen_pack()

    def back_device(self):
        if self.current_device > 0:
            self.current_device -=1
            self.gen_pack()

    def e_view(self):
        print("On edition view")
        self.edit_mode.grid_forget()
        self.maintenance_button.grid_forget()
        self.device_name_entry.configure(textvariable=StringVar(value=''))
        print(self.devices)
        self.device_name_entry.insert(0,self.devices[self.current_device].name)
        self.device_name_entry.grid(row=3,column=1)
        self.device_lT_entry.configure(textvariable=StringVar(value=''))
        self.device_lT_entry.insert(0,self.devices[self.current_device].limit)
        self.device_lT_entry.grid(row=4,column=1)
        self.device_output_option.set(self.devices[self.current_device].output)
        self.device_output_option.grid(row=5,column=1)
        if self.devices[self.current_device].onDeleted:
            self.delete_device_button.configure(fg_color="#f63d45", hover_color="#e01b24")
        else:
            self.delete_device_button.configure(fg_color="#dad8e5", hover_color="#c1bed2") 
        self.delete_device_button.grid(row=5,column=2)

        self.add_device_button.grid(row=6,column=0)
        self.exit_edit_mode.grid(row=6,column=2)
        self.save_device_button.grid(row=6,column=1)

    def n_view(self):
        print(f"On normal view {self.current_device}")
        print(self.devices)
        self.device_name.configure(text=self.devices[self.current_device].name)
        self.device_name.grid(row=3,column=1)
        self.device_lT.configure(text=self.devices[self.current_device].limit)
        self.device_lT.grid(row=4,column=1)
        self.device_output.configure(text=self.devices[self.current_device].output)
        self.device_output.grid(row=5,column=1)

        self.save_device_button.grid_forget()
        self.edit_mode.grid(row=6,column=0)
        self.maintenance_button.grid(row=6,column=1)
        if self.devices[self.current_device].onDeleted:
            self.edit_mode.configure(fg_color="#f63d45", hover_color="#e01b24")
            self.maintenance_button.configure(fg_color="#f63d45", hover_color="#e01b24")
        else:
            self.edit_mode.configure(fg_color="#dad8e5", hover_color="#c1bed2") 
            self.maintenance_button.configure(fg_color="#dad8e5", hover_color="#c1bed2")
        self.add_device_button.grid_forget()
        self.exit_edit_mode.grid_forget()
        

    def refresh(self):
        if self.main_app == None:
            return -1
        for widget in self.main_app.winfo_children():
            if isinstance(widget, CTkToplevel):
                pass
            else:
                widget.grid_forget()

    def show_kb_smtp(self,event):
        if self.keyboard_frame is not None:
            self.keyboard_frame.destroy()
        self.keyboard_frame = VirtualKeyboard(self.host.gui_app, self.smtp_entry, self.host)
        self.keyboard_frame.grid(row=4,column=0)

    def show_kb_sender(self, event):
        if self.keyboard_frame is not None:
            self.keyboard_frame.destroy()
        self.keyboard_frame = VirtualKeyboard(self.host.gui_app, self.sender_entry, self.host)
        self.keyboard_frame.grid(row=4,column=0)

    def show_kb_ma_email(self, event):
        if self.keyboard_frame is not None:
            self.keyboard_frame.destroy()
        self.keyboard_frame = VirtualKeyboard(self.host.gui_app, self.maintenance_email_entry, self.host)
        self.keyboard_frame.grid(row=4,column=0)

    def show_kb_dev_name(self,device):
        if self.keyboard_frame is not None:
            self.keyboard_frame.destroy()
        self.keyboard_frame = VirtualKeyboard(self.host.gui_app, self.device_name_entry, self.host)
        self.keyboard_frame.grid(row=4,column=0)

    def show_kb_dev_it(self,device):
        if self.keyboard_frame is not None:
            self.keyboard_frame.destroy()
        self.keyboard_frame = VirtualNumKeyboard(self.host.gui_app, self.device_lT_entry, self.host)
        self.keyboard_frame.grid(row=4,column=0)

    def show_nkb_port(self,event):
        if self.keyboard_frame is not None:
            self.keyboard_frame.destroy()
        self.keyboard_frame = VirtualNumKeyboard(self.host.gui_app, self.port_entry, self.host)
        self.keyboard_frame.grid(row=4,column=0)

