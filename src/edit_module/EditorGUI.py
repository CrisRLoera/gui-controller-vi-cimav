from customtkinter import CTkLabel, CTkEntry, CTkCheckBox, CTkOptionMenu, CTkButton, CTkToplevel, CTkFrame
from tkinter import StringVar, BooleanVar
class EditorGUI:
    def __init__(self, data,nav,notify,host):
        #self.title = CTkLabel(app,text="Editor")
        self.program = None
        self.steps_list = None
        self.app = host.gui_app
        self.number = None
        self.main_frame=CTkFrame(data)
        self.main_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9),weight=1)
        self.main_frame.grid_columnconfigure((0,1,2),weight=1)
        
        self.name_entry_gui = CTkEntry(self.main_frame)
        self.host = host
        self.current_step = 0
        self.current_type = None
        self.responsible_email = None
        self.interupt_preference = None
        self.step_change_notify = None
        self.end_preference = None
        self.types = ["SET","SOAK","JUMP","END"]
        self.end_options = ["PowerOFF","Restart","SwitchProgram"]

        self.name_gui = CTkLabel(self.main_frame,text='Program Name: ')
        self.err_name = False
        self.err_name_exist = CTkLabel(notify, text="Error: Program name already exist")

        self.type_selector = CTkOptionMenu(self.main_frame,values=self.types, command=self.select_type)
        self.type_selector.set(self.types[0])

        self.outputCheck1 = BooleanVar()
        self.outputCheck2 = BooleanVar()
        self.outputCheck3 = BooleanVar()

        self.set_email_enable = BooleanVar()
        self.advance_button = CTkButton(nav, text="Advanced", command=self.open_advance)

        self.output1 = CTkCheckBox(self.main_frame,text="Output1", variable=self.outputCheck1)
        self.output2 = CTkCheckBox(self.main_frame,text="Output2", variable=self.outputCheck2)
        self.output3 = CTkCheckBox(self.main_frame,text="Output3", variable=self.outputCheck3)

        # Falta texto
        self.soak_time_txt_gui = CTkLabel(self.main_frame, text="Soak duration in minutes")
        self.soak_entry = CTkEntry(self.main_frame)
        
        
        self.jump_err1 = False
        self.err_jump_previus_n_al = CTkLabel(notify, text="Error: Step selection not allowed, the current step has to be larger than the selected step")
        # Falta texto
        self.jump_times_txt_gui = CTkLabel(self.main_frame, text="Repetition number")
        self.jump_times = CTkEntry(self.main_frame)
        self.jump_step_txt_gui = CTkLabel(self.main_frame, text="Step to jump")
        self.jump_step = CTkEntry(self.main_frame)
       
        self.current_step_text = CTkLabel(self.main_frame)

        self.end_options_gui = CTkOptionMenu(self.main_frame, values=self.end_options, command=self.end_program_select)
        self.end_switch_prog = CTkOptionMenu(self.main_frame, command=self.end_program_select)

        self.next_step_button = CTkButton(self.main_frame,text="Next", command=self.next_step)
        self.back_step_button = CTkButton(self.main_frame,text="Back", command=self.back_step)
        self.add_step_button = CTkButton(self.main_frame, text="Add Step", command=self.add_step)
        self.delete_step_button = CTkButton(self.main_frame, text="Delete Step", command=self.delete_current_step)
        self.save_button = CTkButton(nav,text="Save Program", command=self.save_program)
        self.cancel_button = CTkButton(nav,text="Cancel Edition", command=self.cancel_edition)
        self.err_delet_first_step = CTkLabel(notify, text="Error: Can´t delete first step")
        # Preferences Widgets
        self.onAdvance = False
        self.advance_email = CTkLabel(self.main_frame, text="Responsible email")
        self.advance_email_entry = CTkEntry(self.main_frame)
        self.step_change = CTkCheckBox(self.main_frame,text="Let me know every step change")
        self.interruption = CTkCheckBox(self.main_frame,text="Notify me of interruptions")
        self.end_notify = CTkCheckBox(self.main_frame,text="Notify at the end of the program")
        self.send_me = CTkCheckBox(self.main_frame,text="Send me and email", variable=self.set_email_enable, command=self.host.update_Screen)

        self.confirm_button = CTkButton(self.main_frame, text="Confirm", command=lambda: self.confirm(self.advance_email_entry.get(),self.step_change.get(),self.interruption.get(),self.end_notify.get()))
        self.cancel_a_button = CTkButton(self.main_frame, text="Back", command=self.close_advance)


    def open_advance(self):
        self.onAdvance = True
        self.host.update_Screen()

    def confirm(self,email, pref1,pref2,pref3):  
        if self.set_email_enable.get():
            self.responsible_email = email
            self.interupt_preference = pref1
            self.step_change_notify = pref2
            self.end_preference = pref3
            print(self.interupt_preference)
            print(self.step_change_notify)
            print(self.responsible_email)
            print(self.end_preference)
            self.close_advance()
        else:
            self.reset_preferences()

    def close_advance(self):
        self.onAdvance = False
        self.host.update_Screen()

       

    def reset_preferences(self):
        self.responsible_email = None
        self.interupt_preference = None
        self.step_cahnge_notify = None
        self.end_preference = None

    def update(self):
        self.main_frame.grid(row=0,column=0,columnspan=2,sticky="nswe")
        # Data GUI
        if not self.onAdvance:
            self.advance_email.grid_forget()
            self.advance_email_entry.grid_forget()
            self.step_change.grid_forget()
            self.interruption.grid_forget()
            self.end_notify.grid_forget()
            self.confirm_button.grid_forget()
            self.name_gui.grid(row=0,column=1)
            self.name_entry_gui.grid(row=1,column=1)
            self.current_step_text.configure(text=f'Current step: {self.current_step}')
            self.current_step_text.grid(row=2,column=1)
            self.type_selector.grid(row=3,column=1)
            if self.current_type == 'SET':
                self.showSET()
            elif self.current_type == 'SOAK':
                self.showSOAK()
            elif self.current_type == 'JUMP':
                self.showJUMP()
            elif self.current_type == 'END':
                self.showEND()
            self.next_step_button.grid(row=2,column=2)
            self.back_step_button.grid(row=2,column=0)
            self.add_step_button.grid(row=8,column=1)
            self.delete_step_button.grid(row=9,column=1)
            self.advance_button.grid(row=0,column=1)
        else:
            self.send_me.grid(row=0,column=1)
            if self.set_email_enable.get():
                self.advance_email.grid(row=1,column=1)
                self.advance_email_entry.grid(row=2,column=1)
                self.step_change.grid(row=3,column=1)
                self.interruption.grid(row=4,column=1)
                self.end_notify.grid(row=5,column=1)
            else:
                self.advance_email.grid_forget()
                self.advance_email_entry.grid_forget()
                self.step_change.grid_forget()
                self.interruption.grid_forget()
                self.end_notify.grid_forget()
            self.confirm_button.grid(row=6,column=1)
            self.cancel_a_button.grid(row=7,column=1)
        # Nav buttons
        self.save_button.grid(row=0,column=0)
        self.cancel_button.grid(row=0,column=2)
        # Errors and notifications in GUI
        if self.err_name:
            self.err_name_exist.grid(row=0,column=0)
        else:
            self.err_name_exist.grid_forget()

    def add_step(self):
        self.steps_list.append({})

    def delete_current_step(self):
        if self.current_step > 0:
            del self.steps_list[self.current_step]
            self.current_step -=1
            if self.steps_list[self.current_step]!= {}:
                self.current_type = self.steps_list[self.current_step]['type']
            self.refresh()
            self.err_delet_first_step.grid_forget()
        else:
            self.err_delet_first_step.grid(row=0,column=0)
            print("No hay elemetos suficientes")


    def back_step(self):
        old_step = self.current_step
        if self.current_step >0:
            self.oldStep(old_step)
            self.current_step -= 1
            if self.steps_list[self.current_step]!= {}:
                self.current_type = self.steps_list[self.current_step]['type']
            self.refresh()
            print(self.current_step)

    def next_step(self):
        old_step = self.current_step
        if self.current_step < len(self.steps_list)-1:
            self.oldStep(old_step)
            self.current_step += 1
            if self.steps_list[self.current_step]!= {}:
                self.current_type = self.steps_list[self.current_step]['type']
            else:
                self.current_type = None
            self.refresh()
            print(self.current_step)

    def save_program(self):
        self.oldStep(self.current_step)
        program={""}
        if self.host.file_controller.diffName(self.number,self.name_entry_gui.get()):
            self.program['name']=self.name_entry_gui.get()
            self.program['steps']=self.steps_list
            self.program['responsible']= self.responsible_email
            self.program['interrupt'] = self.interupt_preference
            self.program['end notify'] = self.end_preference
            self.program['step change notify'] = self.step_change_notify
            self.host.file_controller.saveProgram(self.program['number'],self.program)
            self.program = None
            self.reset_preferences()
            self.steps_list = None
            self.number = None
            self.current_step = 0
            self.current_type = None
            self.host.program_screen.selected = None
            self.host.current_screen = 'program'
            self.host.update_Screen()
            self.err_name = False
        else:
            self.err_name = True
            self.update()
        
    def cancel_edition(self):
        self.current_type = None
        self.program = None
        self.number = None
        self.current_step = 0
        self.steps_list = None
        self.err_name = False
        self.reset_preferences()
        self.host.file_controller.reload()
        self.host.current_screen = 'program'
        self.host.update_Screen()


    def select_type(self,choice):
        self.current_type = choice
        self.steps_list[self.current_step]['type'] = self.current_type
        if self.current_type == 'SET':
            self.type_selector.set(self.steps_list[self.current_step]['type'])
            self.steps_list[self.current_step]['output1']=False
            self.steps_list[self.current_step]['output2']=False
            self.steps_list[self.current_step]['output3']=False
            self.outputCheck1.set(self.steps_list[self.current_step]['output1'])
            self.outputCheck2.set(self.steps_list[self.current_step]['output2'])
            self.outputCheck3.set(self.steps_list[self.current_step]['output3'])
        elif self.current_type == 'SOAK':
            self.type_selector.set(self.steps_list[self.current_step]['type'])
            self.soak_entry.configure(textvariable=StringVar(value='0'))
        elif self.current_type == 'JUMP':
            self.type_selector.set(self.steps_list[self.current_step]['type'])
            self.jump_step.configure(textvariable=StringVar(value='0'))
            self.jump_times.configure(textvariable=StringVar(value='0'))
        elif self.current_type == 'END':
            self.type_selector.set(self.steps_list[self.current_step]['type'])
            self.end_switch_prog.set(None)
        self.oldStep(self.current_step)
        # Posible bug por funcion oldStep
        self.host.update_Screen()
               
    def end_program_select(self,choice):
        self.steps_list[self.current_step]['action']=choice
        self.oldStep(self.current_step)
            # Posible bug por funcion oldStep
        self.host.update_Screen()

    def refresh(self):
        self.loadStepConf()
        self.host.update_Screen()


    def oldStep(self,old):
        # Save previus step
        self.steps_list[old].clear()
        if self.current_type == 'SET':
            self.steps_list[old]['type']='SET'
            self.steps_list[old]['output1']=self.outputCheck1.get()
            self.steps_list[old]['output2']=self.outputCheck2.get()
            self.steps_list[old]['output3']=self.outputCheck3.get()
        elif self.current_type == 'SOAK':
            self.steps_list[old]['type']='SOAK'
            self.steps_list[old]['time']=int(self.soak_entry.get())
        elif self.current_type == 'JUMP':
            self.steps_list[old]['type']='JUMP'
            if int(self.jump_step.get())>self.current_step:
                self.jump_err1 = True
            else:
                self.steps_list[old]['step']=int(self.jump_step.get())
                self.jump_err1 = False
            self.steps_list[old]['times']=int(self.jump_times.get())
        elif self.current_type == 'END':
            self.steps_list[old]['type']='END'
            self.steps_list[old]['action']=self.end_options_gui.get()
            if self.steps_list[old]['action']=='SwitchProgram':
                self.steps_list[old]['program']=self.end_switch_prog.get()
            else:
                self.steps_list[old]['program']=self.name_entry_gui.get()
        elif self.current_type == None:
            pass

    def loadStepConf(self):
        if self.current_type == 'SET':
            self.type_selector.set(self.steps_list[self.current_step]['type'])
            self.outputCheck1.set(self.steps_list[self.current_step]['output1'])
            self.outputCheck2.set(self.steps_list[self.current_step]['output2'])
            self.outputCheck3.set(self.steps_list[self.current_step]['output3'])
        elif self.current_type == 'SOAK':
            self.type_selector.set(self.steps_list[self.current_step]['type'])
            self.soak_entry.configure(textvariable=StringVar(value=''))
            self.soak_entry.insert(0,self.steps_list[self.current_step]['time'])
        elif self.current_type == 'JUMP':
            self.type_selector.set(self.steps_list[self.current_step]['type'])
            self.jump_step.configure(textvariable=StringVar(value=''))
            self.jump_step.insert(0,self.steps_list[self.current_step]['step'])
            self.jump_times.configure(textvariable=StringVar(value=''))
            self.jump_times.insert(0,self.steps_list[self.current_step]['times'])
        elif self.current_type == 'END':
            self.type_selector.set(self.steps_list[self.current_step]['type'])
            self.steps_list[self.current_step]['type']='END'
            self.end_options_gui.set(self.steps_list[self.current_step]['action'])
            self.end_switch_prog.set(self.steps_list[self.current_step]['program'])
        else:
            self.type_selector.set("")
        

    def loadProgram(self):
        if self.program != None:
            self.name_entry_gui.configure(textvariable=StringVar(value=''))
            self.name_entry_gui.insert(0,self.program['name'])
            self.number = self.program['number']
        if self.program['steps']!=None:
            self.steps_list = self.program['steps']
            if self.steps_list[0]== {}:
                self.steps_list=[{}]
                self.type_selector.set("")
            else:
                self.type_selector.set(self.steps_list[0]['type'])
                self.current_type = self.steps_list[self.current_step]['type']
                self.loadStepConf()

    def showSET(self):
        self.output1.grid(row=4,column=1)
        self.output2.grid(row=5,column=1)
        self.output3.grid(row=6,column=1)

    def showSOAK(self):
        self.soak_time_txt_gui.grid(row=4,column=1)
        self.soak_entry.grid(row=5,column=1)

    def showJUMP(self):
        self.jump_times_txt_gui.grid(row=4,column=1)
        self.jump_times.grid(row=5,column=1)
        self.jump_step_txt_gui.grid(row=6,column=1)
        self.jump_step.grid(row=7,column=1)
        if self.jump_err1:
            self.err_jump_previus_n_al.grid(row=0,column=0)
        else:
            self.err_jump_previus_n_al.grid_forget()

    def showEND(self):
        self.end_options_gui.grid(row=4,column=1)
        if self.steps_list[self.current_step]['action']=='SwitchProgram':
            self.end_switch_prog.configure(values=[name['name'] for name in self.host.file_controller.programs_list])
            self.end_switch_prog.grid(row=5,column=1)
        else:
            self.end_switch_prog.grid_forget()
