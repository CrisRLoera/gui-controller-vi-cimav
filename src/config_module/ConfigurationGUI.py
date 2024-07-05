from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkButton, CTkOptionMenu, CTkFrame
from tkinter import StringVar

class Device:
    def __init__(self,app,host,name,limit,output,last):
        self.name = name
        self.limit = limit
        self.output = output
        self.host = host
        self.output_list = ["output1","output2","output3"]
        self.last = last

    def getValues(self):
        return self.name,self.limit,self.output

    def destroy(self):
        self.onDeleted = True
        self.host.gen_pack()

    def mainteined(self):
        try:
            for index,device in enumerate(self.host.devices):
                print(index,device)
                if self.name_label.cget("text") == device.name and self.limit_label.cget("text")== device.limit and self.assign_output_label.cget("text") == device.output:
                    print("get")
                    if device['output']=='output1':
                        self.host.host.file_controller.conf_file['output1 on time']:0
                    if device['output']=='output2':
                        self.host.host.file_controller.conf_file['output2 on time']:0
                    if device['output']=='output3':
                        self.host.host.file_controller.conf_file['output3 on time']:0
                    self.host.host.file_controller.conf_file['maintenance devices'][index]['last reminder'] = None
                    self.host.host.file_controller.updateConf()
                    self.host.host.file_controller.loadConf()
        except:
            print("Device not found")

class ConfigurationGUI:
    def __init__ (self,data,nav,host):
        self.host = host
        self.conf_view = None
        self.edition_mode = False
        self.output_list = ["output1","output2","output3"]
        self.conf_file = self.host.file_controller.conf_file
        self.main_app = CTkFrame(data)
        self.main_app.grid_columnconfigure((0,1),weight=1)
        self.main_app.grid_rowconfigure((0),weight=1)
        self.conf_view = CTkFrame(self.main_app)
        self.conf_view.grid_columnconfigure((0),weight=1)
        self.conf_view.grid_rowconfigure((0,1,2,3,4,5,6,7,8),weight=1)
        self.dev_view = CTkFrame(self.main_app)
        self.dev_view.grid_columnconfigure((0,1,2),weight=1)
        self.dev_view.grid_rowconfigure((0,1,2,3,4,5,6),weight=1)
        self.smtp_label = CTkLabel(self.conf_view, text="SMTP Server")
        self.smtp_entry = CTkEntry(self.conf_view)
        self.port = CTkLabel(self.conf_view, text="Port")
        self.port_entry = CTkEntry(self.conf_view)
        self.sender_label = CTkLabel(self.conf_view, text="Sender")
        self.sender_entry = CTkEntry(self.conf_view)
        self.maintenance_label = CTkLabel(self.conf_view, text="Maintenance")
        self.maintenance_email_label = CTkLabel(self.conf_view, text="Maintenance email")
        self.maintenance_email_entry = CTkEntry(self.conf_view)

        self.devices_label = CTkLabel(self.dev_view, text="Devices")
        self.edit_mode = CTkButton(self.dev_view,text="edit", command=self.enable_edit_mode)
        self.add_device = CTkButton(self.dev_view,text="add", command=self.add_device)
        self.exit_edit_mode = CTkButton(self.dev_view,text="cancel", command=self.disable_edit_mode)
        
        self.device_name_label=CTkLabel(self.dev_view,text="Device name:")
        self.device_name=CTkLabel(self.dev_view)
        self.device_name_entry = CTkEntry(self.dev_view)

        self.device_lT_label=CTkLabel(self.dev_view,text="Device limit:")
        self.device_lT=CTkLabel(self.dev_view)
        self.device_lT_entry= CTkEntry(self.dev_view)

        self.device_output_label=CTkLabel(self.dev_view,text="Device output:")
        self.device_output=CTkLabel(self.dev_view)
        self.device_output_option = CTkOptionMenu(self.dev_view,values=self.output_list) 

        self.save_device_button = CTkButton(self.dev_view,text="save this device", command=self.save_device)
        self.save_edit_mode = CTkButton(nav,text="save all changes", command=self.save_edition)
        self.close_button = CTkButton(nav,text="Close",command=self.close_window)


        self.current_device=0
    


    def update(self):
        self.smtp_entry.insert(0,self.conf_file['host'])
        self.port_entry.insert(0,self.conf_file['port']) 
        self.sender_entry.insert(0,self.conf_file['sender'])
        
        self.maintenance_email_entry.insert(0,self.conf_file['maintenance'])
        
        self.get_devices()
        

        self.gen_pack()

    def get_devices(self):
        self.devices = []
        for device in self.host.file_controller.conf_file["maintenance devices"]:
            self.devices.append(Device(self.conf_view,self,device['name'],device['use limit'],device['output'],device['last reminder']))

    def close_window(self):
        self.edition_mode = False
        self.main_app.destroy()

    def enable_edit_mode(self):
        self.edition_mode = True
        self.gen_pack()

    def disable_edit_mode(self):
        self.edition_mode = False
        self.get_devices()
        self.gen_pack()

    def save_device(self):
        self.devices[self.current_device].name=self.device_name_entry.get()
        self.devices[self.current_device].limit=self.device_lT_entry.get()
        self.devices[self.current_device].output=self.device_output_option.get()
        self.disable_edit_mode()

    
    def save_edition(self):
        dev_list = []
        for device in self.devices:
            value = device.getValues()
            if not device.onDeleted:
                if value[0]!='' or value[1]!='' or value[2]!='':
                    dev_list.append({"name":value[0],"use limit":int(value[1]),"output":value[2],'last reminder':device.last})
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

    def add_device(self):
        self.devices.append(Device(self.conf_view,self.host,'','','',None))
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
        self.maintenance_label.grid(row=6,column=0)
        self.maintenance_email_label.grid(row=7,column=0)
        self.maintenance_email_entry.grid(row=8,column=0)

        self.devices_label.grid(row=0,column=1)
        self.total_devices=CTkLabel(self.dev_view)
        self.total_devices.configure(text=f"Total devices: {len(self.devices)}")
        self.total_devices.grid(row=1,column=1)
        self.current_device_label=CTkLabel(self.dev_view)
        self.current_device_label.configure(text=f"Current device: {self.current_device}")
        self.current_device_label.grid(row=2,column=1)
        self.next_device_button = CTkButton(self.dev_view,text="next",command=self.next_device)
        self.next_device_button.grid(row=2,column=2)
        self.back_device_button = CTkButton(self.dev_view,text="back",command=self.back_device)
        self.back_device_button.grid(row=2,column=0)

        self.device_name_label.grid(row=3,column=0)
        
        
        self.device_lT_label.grid(row=4,column=0)
        self.device_output_label.grid(row=5,column=0)
        
        


        '''
        for device in self.devices:
            if self.edition_mode and not device.onDeleted:
                device.update_edition_mode()
            elif self.edition_mode == False and not device.onDeleted:
                device.update()
        
        '''
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
        self.edit_mode.grid_forget()
        self.device_name_entry.configure(textvariable=StringVar(value=''))
        self.device_name_entry.insert(0,self.devices[self.current_device].name)
        self.device_name_entry.grid(row=3,column=1)
        self.device_lT_entry.configure(textvariable=StringVar(value=''))
        self.device_lT_entry.insert(0,self.devices[self.current_device].limit)
        self.device_lT_entry.grid(row=4,column=1)        
        self.device_output_option.set(self.devices[self.current_device].output)
        self.device_output_option.grid(row=5,column=1)

        self.add_device.grid(row=6,column=0)
        self.exit_edit_mode.grid(row=6,column=2)
        self.save_device_button.grid(row=6,column=1)

    def n_view(self):
        self.device_name.configure(text=self.devices[self.current_device].name)
        self.device_name.grid(row=3,column=1)
        self.device_lT.configure(text=self.devices[self.current_device].limit)
        self.device_lT.grid(row=4,column=1)
        self.device_output.configure(text=self.devices[self.current_device].output)
        self.device_output.grid(row=5,column=1)

        self.save_device_button.grid_forget()
        self.edit_mode.grid(row=6,column=0)
        self.add_device.grid_forget()
        self.exit_edit_mode.grid_forget()
        

    def refresh(self):
        if self.main_app == None:
            return -1
        for widget in self.main_app.winfo_children():
            if isinstance(widget, CTkToplevel):
                pass
            else:
                widget.grid_forget()
