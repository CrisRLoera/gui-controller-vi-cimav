from customtkinter import CTkLabel, CTkEntry, CTkCheckBox, CTkOptionMenu, CTkButton, CTkToplevel
from tkinter import StringVar, BooleanVar
class EditorGUI:
    def __init__(self, app,host):
        self.title = CTkLabel(app,text="Editor")
        self.program = None
        self.steps_list = None
        self.app = app
        self.name_gui = CTkLabel(app,text='Program Name: ')
        self.number = None
        self.name_entry_gui = CTkEntry(app)
        self.host = host
        self.current_step = 0
        self.current_type = None
        self.responsible_email = None
        self.interupt_preference = None
        self.step_change_notify = None
        self.types = ["SET","SOAK","JUMP","END"]
        self.end_options = ["PowerOFF","Restart","SwitchProgram"]

        self.err_name = False
        self.err_name_exist = CTkLabel(app, text="Error: Program name already exist")

        self.type_selector = CTkOptionMenu(app,values=self.types, command=self.select_type)
        self.type_selector.set(self.types[0])

        self.outputCheck1 = BooleanVar()
        self.outputCheck2 = BooleanVar()
        self.outputCheck3 = BooleanVar()

        self.set_email_enable = BooleanVar()
        self.advance_button = CTkButton(app, text="Advance", command=self.open_advance)

        self.output1 = CTkCheckBox(app,text="Output1", variable=self.outputCheck1)
        self.output2 = CTkCheckBox(app,text="Output2", variable=self.outputCheck2)
        self.output3 = CTkCheckBox(app,text="Output3", variable=self.outputCheck3)

        self.soak_entry = CTkEntry(app)

        self.jump_err1 = False
        self.err_jump_previus_n_al = CTkLabel(app, text="Error: Step selection not allowed, the current step has to be larger than the selected step")
        self.jump_times = CTkEntry(app)
        self.jump_step = CTkEntry(app)
       
        self.current_step_text = CTkLabel(app)

        self.end_options_gui = CTkOptionMenu(app, values=self.end_options, command=self.end_program_select)
        self.end_switch_prog = CTkOptionMenu(app, command=self.end_program_select)

        self.next_step_button = CTkButton(app,text="Next", command=self.next_step)
        self.back_step_button = CTkButton(app,text="Back", command=self.back_step)
        self.add_step_button = CTkButton(app, text="Add Step", command=self.add_step)
        self.delete_step_button = CTkButton(app, text="Delete Step", command=self.delete_current_step)
        self.save_button = CTkButton(app,text="Save Program", command=self.save_program)
        self.cancel_button = CTkButton(app,text="Cancel Edition", command=self.cancel_edition)
        self.err_delet_first_step = CTkLabel(app, text="Error: Can´t delete first step")

    def open_advance(self):
        advance = CTkToplevel(self.app)
        advance_email = CTkLabel(advance, text="Responsible email")
        advance_email_entry = CTkEntry(advance)
        step_change = CTkCheckBox(advance,text="Let me know every step change")
        interruption = CTkCheckBox(advance,text="Notify me of interruptions")

        def update_email():
            if self.set_email_enable.get():
                advance_email.pack()
                advance_email_entry.pack()
                step_change.pack()
                interruption.pack()
                confirm_button.pack_forget()
                confirm_button.pack()
            else:
                advance_email.pack_forget()
                advance_email_entry.pack_forget()
                step_change.pack_forget()
                interruption.pack_forget()
                confirm_button.pack_forget()
                confirm_button.pack()
        send_me = CTkCheckBox(advance,text="Send me and email", variable=self.set_email_enable, command=update_email)
        send_me.pack()

        def confirm(email, pref1,pref2):  
            if self.set_email_enable.get():
                self.responsible_email = email
                self.interupt_preference = pref1
                self.step_change_notify = pref2
                print(self.interupt_preference)
                print(self.step_change_notify)
                print(self.responsible_email)
            else:
                self.reset_preferences()
            advance.destroy()

        confirm_button = CTkButton(advance, text="Confirm", command=lambda: confirm(advance_email_entry.get(),step_change.get(),interruption.get()))
        confirm_button.pack()
    def reset_preferences(self):
        self.responsible_email = None
        self.interupt_preference = None
        self.step_cahnge_notify = None

    def update(self):
        self.title.pack()
        self.current_step_text.configure(text=f'Current step: {self.current_step}')
        self.current_step_text.pack()
        self.name_gui.pack()
        self.name_entry_gui.pack()
        self.type_selector.pack()
        if self.current_type == 'SET':
            self.showSET()
        elif self.current_type == 'SOAK':
            self.showSOAK()
        elif self.current_type == 'JUMP':
            self.showJUMP()
        elif self.current_type == 'END':
            self.showEND()
        self.next_step_button.pack()
        self.back_step_button.pack()
        self.add_step_button.pack()
        self.delete_step_button.pack()
        self.advance_button.pack()
        self.save_button.pack()
        self.cancel_button.pack()
        if self.err_name:
            self.err_name_exist.pack()
        else:
            self.err_name_exist.pack_forget()

    def add_step(self):
        self.steps_list.append({})

    def delete_current_step(self):
        if self.current_step > 0:
            del self.steps_list[self.current_step]
            self.current_step -=1
            if self.steps_list[self.current_step]!= {}:
                self.current_type = self.steps_list[self.current_step]['type']
            self.refresh()
            self.err_delet_first_step.pack_forget()
        else:
            self.err_delet_first_step.pack()
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
                self.steps_list[old]['program']=None
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
        self.output1.pack()
        self.output2.pack()
        self.output3.pack()

    def showSOAK(self):
        self.soak_entry.pack()

    def showJUMP(self):
        self.jump_times.pack()
        self.jump_step.pack()
        if self.jump_err1:
            self.err_jump_previus_n_al.pack()
        else:
            self.err_jump_previus_n_al.pack_forget()

    def showEND(self):
        self.end_options_gui.pack()
        if self.steps_list[self.current_step]['action']=='SwitchProgram':
            self.end_switch_prog.configure(values=[name['name'] for name in self.host.file_controller.programs_list])
            self.end_switch_prog.pack()
        else:
            self.end_switch_prog.pack_forget()
