from customtkinter import CTkToplevel, CTkLabel, CTkEntry, CTkButton, CTkOptionMenu, CTkScrollableFrame
from tkinter import StringVar

class Device:
    def __init__(self,app,host,name,limit,output,last):
        self.name = name
        self.limit = limit
        self.output = output
        self.host = host
        self.output_list = ["output1","output2","output3"]
        self.last = last
        self.name_label = CTkLabel(app,text=name)
        self.limit_label = CTkLabel(app,text=limit)
        self.assign_output_label = CTkLabel(app,text=output)

        self.m_e_name_label = CTkLabel(app,text="Name")
        self.name_entry = CTkEntry(app)
        self.name_entry.insert(0,name)
        self.m_e_limit_label = CTkLabel(app,text="Use limit")
        self.limit_entry = CTkEntry(app)
        self.limit_entry.insert(0,limit)
        self.m_e_assign_menu_label = CTkLabel(app,text="Output")
        self.assign_menu = CTkOptionMenu(app, values=self.output_list)
        self.assign_menu.set(output)
        self.delete_device = CTkButton(app,text="-", command=self.destroy)
        self.check_maintenance = CTkButton(app,text="Done", command=self.mainteined)
        self.onDeleted = False

    def update(self):
        self.name_label.pack()
        self.limit_label.pack()
        self.assign_output_label.pack()
        self.check_maintenance.pack()

    ## Modo edicion
    def update_edition_mode(self):
        self.m_e_name_label.pack()
        self.name_entry.pack()
        self.m_e_limit_label.pack()
        self.limit_entry.pack()
        self.m_e_assign_menu_label.pack()
        self.assign_menu.pack()
        self.delete_device.pack()
    
    
    def getValues(self):
        return self.name_entry.get(),self.limit_entry.get(),self.assign_menu.get()

    def destroy(self):
        self.onDeleted = True
        self.host.refresh()
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

class ConfigureGUI:
    def __init__ (self,app,host):
        self.app = app
        self.host = host
        self.conf_view = None
        self.edition_mode = False
        self.conf_file = self.host.file_controller.conf_file

    def update(self):
        self.main_app = CTkToplevel(self.app)
        self.conf_view = CTkScrollableFrame(self.main_app)
        self.smtp_label = CTkLabel(self.conf_view, text="SMTP Server")
        self.smtp_entry = CTkEntry(self.conf_view)
        self.smtp_entry.insert(0,self.conf_file['host'])
        self.port = CTkLabel(self.conf_view, text="Port")
        self.port_entry = CTkEntry(self.conf_view)
        self.port_entry.insert(0,self.conf_file['port'])
        self.sender_label = CTkLabel(self.conf_view, text="Sender")
        self.sender_entry = CTkEntry(self.conf_view)
        self.sender_entry.insert(0,self.conf_file['sender'])
        self.maintenance_label = CTkLabel(self.conf_view, text="Maintenance")
        self.maintenance_email_label = CTkLabel(self.conf_view, text="Maintenance email")
        self.maintenance_email_entry = CTkEntry(self.conf_view)
        self.maintenance_email_entry.insert(0,self.conf_file['maintenance'])
        self.devices_label = CTkLabel(self.conf_view, text="Devices")
        self.get_devices()
        self.edit_mode = CTkButton(self.conf_view,text="edit", command=self.enable_edit_mode)
        self.add_device = CTkButton(self.conf_view,text="add", command=self.add_device)
        self.exit_edit_mode = CTkButton(self.conf_view,text="cancel", command=self.disable_edit_mode)
        self.save_edit_mode = CTkButton(self.conf_view,text="save", command=self.save_edition)

        self.close_button = CTkButton(self.conf_view,text="Close",command=self.close_window)

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
        self.conf_view.pack(expand=True, fill="both", padx=20, pady=20)
        self.smtp_label.pack()
        self.smtp_entry.pack()
        self.port.pack()
        self.port_entry.pack()
        self.sender_label.pack()
        self.sender_entry.pack()
        self.maintenance_label.pack()
        self.maintenance_email_label.pack()
        self.maintenance_email_entry.pack()
        self.devices_label.pack()
        for device in self.devices:
            if self.edition_mode and not device.onDeleted:
                device.update_edition_mode()
            elif self.edition_mode == False and not device.onDeleted:
                device.update()
        if self.edition_mode:
            self.edit_mode.pack_forget()
            self.add_device.pack()
            self.exit_edit_mode.pack()
        else:
            self.edit_mode.pack()
            self.add_device.pack_forget()
            self.exit_edit_mode.pack_forget()
        self.save_edit_mode.pack()
        self.close_button.pack()

    def refresh(self):
        if self.conf_view == None:
            return -1
        for widget in self.conf_view.winfo_children():
            if isinstance(widget, CTkToplevel):
                pass
            else:
                widget.pack_forget()
