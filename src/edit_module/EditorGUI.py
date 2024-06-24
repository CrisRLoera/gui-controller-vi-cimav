from customtkinter import CTkLabel, CTkEntry, CTkCheckBox, CTkOptionMenu, CTkButton
from tkinter import StringVar, BooleanVar
class EditorGUI:
    def __init__(self, app,host):
        self.title = CTkLabel(app,text="Editor")
        self.program = None
        self.steps_list = None
        self.name_gui = CTkLabel(app,text='Program Name: ')
        self.name_entry_gui = CTkEntry(app)
        self.host = host
        self.current_step = 0
        self.current_type = None
        self.types = ["SET","SOAK","JUMP","END"]
        self.end_options = ["PowerOFF","Restart","SwitchProgram"]

        self.type_selector = CTkOptionMenu(app,values=self.types, command=self.select_type)
        self.type_selector.set(self.types[0])

        self.outputCheck1 = BooleanVar()
        self.outputCheck2 = BooleanVar()
        self.outputCheck3 = BooleanVar()

        self.output1 = CTkCheckBox(app,text="Output1", variable=self.outputCheck1)
        self.output2 = CTkCheckBox(app,text="Output2", variable=self.outputCheck2)
        self.output3 = CTkCheckBox(app,text="Output3", variable=self.outputCheck3)

        self.soak_entry = CTkEntry(app)

        self.jump_times = CTkEntry(app)
        self.jump_step = CTkEntry(app)
        
        self.end_options_gui = CTkOptionMenu(app, values=self.end_options, command=self.end_program_select)
        self.end_switch_prog = CTkOptionMenu(app, command=self.end_program_select)

        self.next_step_button = CTkButton(app,text="Next", command=self.next_step)
        self.back_step_button = CTkButton(app,text="Back", command=self.back_step)

    def update(self):
        self.title.pack()
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
       

    def back_step(self):
        old_step = self.current_step
        if self.current_step >0:
            self.oldStep(old_step)
            self.current_step -= 1
            self.current_type = self.steps_list[self.current_step]['type']
            self.refresh()
            print(self.current_step)

    def next_step(self):
        old_step = self.current_step
        print(len(self.steps_list))
        if self.current_step < len(self.steps_list)-1:
            self.oldStep(old_step)
            self.current_step += 1
            self.current_type = self.steps_list[self.current_step]['type']
            self.refresh()
            print(self.current_step)

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
            self.steps_list[old]['step']=int(self.jump_step.get())
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
        print(self.steps_list)

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
        

    def loadProgram(self):
        if self.program != None:
            self.name_entry_gui.insert(0,self.program['name'])
        if self.program['steps']!=None:
            self.steps_list = self.program['steps']
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

    def showEND(self):
        self.end_options_gui.pack()
        if self.steps_list[self.current_step]['action']=='SwitchProgram':
            self.end_switch_prog.configure(values=[name['name'] for name in self.host.file_controller.programs_list])
            self.end_switch_prog.set(self.end_switch_prog._values[0])
            self.end_switch_prog.pack()
        else:
            self.end_switch_prog.pack_forget()
