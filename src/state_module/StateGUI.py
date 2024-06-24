from customtkinter import CTkLabel, CTkButton

class StateGUI:
    def __init__(self,app,host):
        self.title = CTkLabel(app, text='Menu')
        self.host = host
        self.current_program = {'number': None, 'name': None, 'steps': None}
        self.current_step = None
        self.current_step_number = None
        self.program_state = False
        self.program_number = self.current_program['number']
        self.program_name = self.current_program['name']
        self.program_steps = self.current_program['steps']
        self.program_jumps_left = 0

        self.program_state_gui = CTkLabel(app, text=f'State: {self.program_state}')
        self.name_gui = CTkLabel(app, text=f"Program name: {self.program_name}")
        self.number_gui = CTkLabel(app, text=f"Program number: {self.program_number}")
        self.current_step_gui = CTkLabel(app, text=f"Current step: {self.current_step_number}")
        self.jumpls_left_gui = CTkLabel(app)
        
        self.run_program_button_gui = CTkButton(app, command=self.run_current_program)
        self.selec_program_button_gui = CTkButton(app, text='Program', command=self.changeProgramScreen)

    def update(self):
        self.title.pack()
        self.name_gui.configure(text=f'Program name: {self.program_name}')
        self.number_gui.configure(text=f'Program number: {self.program_number}')
        self.current_step_gui.configure(text=f'Current step: {self.current_step_number}')
        self.program_state_gui.pack()
        self.name_gui.pack()
        self.number_gui.pack()
        self.current_step_gui.pack()

        self.program_state_gui.configure(text=f'State: {'Running'if self.program_state else 'Stop'}')
        self.run_program_button_gui.configure(text='Stop'if self.program_state else 'Run')
        self.run_program_button_gui.pack()
        self.program_steps = self.current_program['steps']
        if self.program_state == False:
            self.selec_program_button_gui.pack()
        else:
            self.selec_program_button_gui.pack_forget()
        print(self.program_state)

    def run_current_program(self):
        print("Press")
        if self.program_state == True:
            self.program_state = False
            self.update()
        else:
            self.program_state = True
            self.update()

#    def updateStateData(self):


    def changeProgramScreen(self):
        self.host.current_screen = 'program'
        self.host.update_Screen()

    def changeCurrentProgram(self):
        self.program_steps = self.current_program['steps']
        if self.current_program['steps'] != None:
            self.current_step = self.current_program['steps'][0]
            print(type(self.program_steps))
            self.current_step_number = self.program_steps.index(self.current_step)
        self.program_state = False
        self.program_number = self.current_program['number']
        self.program_name = self.current_program['name']
        if self.current_step['type']=='JUMP':
            self.program_jumps_left = self.current_step['times']
            
