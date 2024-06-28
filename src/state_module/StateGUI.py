from customtkinter import CTkLabel, CTkButton, CTkEntry

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
        self.program_jumps_left = None
        self.soak_time_left = None

        self.output_state1 = False
        self.output_state2 = False
        self.output_state3 = False

        self.time_left = None

        self.program_state_gui = CTkLabel(app, text=f'State: {self.program_state}')
        self.name_gui = CTkLabel(app, text=f"Program name: {self.program_name}")
        self.number_gui = CTkLabel(app, text=f"Program number: {self.program_number}")
        self.current_step_gui = CTkLabel(app, text=f"Current step: {self.current_step_number}")
        self.jumps_left_gui = CTkLabel(app)
        self.soak_time_left_gui = CTkLabel(app)

        self.out1_label = CTkLabel(app)
        self.out2_label = CTkLabel(app)
        self.out3_label = CTkLabel(app)

        self.run_program_button_gui = CTkButton(app, command=self.run_current_program)
        self.selec_program_button_gui = CTkButton(app, text='Program', command=self.changeProgramScreen)
        self.test = CTkEntry(app)

        self.err_no_current_program = False
        self.err_no_crnt_prg_text = CTkLabel(app, text='Error: No current program to run')


    def update(self):
        self.title.pack()
        self.name_gui.configure(text=f'Program name: {self.program_name}')
        self.number_gui.configure(text=f'Program number: {self.program_number}')
        self.current_step_gui.configure(text=f'Current step: {self.current_step_number}')
        if self.program_jumps_left != None:
            self.jumps_left_gui.configure(text=f"Jumps left: {self.program_jumps_left}")
            self.jumps_left_gui.pack()
        else:
            self.jumps_left_gui.pack_forget()
        if self.soak_time_left != None:
            self.soak_time_left_gui.configure(text=f"Soak time left: {self.soak_time_left}")
            self.soak_time_left_gui.pack()
        else:
            self.soak_time_left_gui.pack_forget()
        self.out1_label.configure(text=f"Output1: {'ON'if self.output_state1 else 'OFF'}")
        self.out2_label.configure(text=f"Output2: {'ON'if self.output_state2 else 'OFF'}")
        self.out3_label.configure(text=f"Output3: {'ON'if self.output_state3 else 'OFF'}")
        self.program_state_gui.pack()
        self.name_gui.pack()
        self.number_gui.pack()
        self.current_step_gui.pack()
        self.out1_label.pack()
        self.out2_label.pack()
        self.out3_label.pack()

        self.program_state_gui.configure(text=f"State: {'Running'if self.program_state else 'Stop'}")
        self.run_program_button_gui.configure(text='Stop'if self.program_state else 'Run')
        self.run_program_button_gui.pack()
        self.program_steps = self.current_program['steps']
        if self.program_state == False:
            self.selec_program_button_gui.pack()
        else:
            self.selec_program_button_gui.pack_forget()
        if self.err_no_current_program:
            self.err_no_crnt_prg_text.pack()
        else:
            self.err_no_crnt_prg_text.pack_forget()

    def run_current_program(self):
        if self.current_program == {'number': None, 'name': None, 'steps': None}:
            self.err_no_current_program = True
            self.update()
            return 0
        self.err_no_current_program = False
        if self.program_state == True:
            self.host.recovery_controller.gen_empty_recovery_file()
            self.program_state = False
            self.update()
        else:
            self.program_state = True
            self.update()
            self.host.recovery_controller.gen_recovery_file()

    def turnOff(self):
        self.host.recovery_controller.gen_empty_recovery_file()
        self.program_state = False
        self.update()


    def changeOutputs(self,out1,out2,out3):
        self.output_state1 = out1
        self.output_state2 = out2
        self.output_state3 = out3


    def changeProgramScreen(self):
        self.host.current_screen = 'program'
        self.host.update_Screen()

    def changeCurrentProgram(self):
        self.program_steps = self.current_program['steps']
        if self.current_program['steps'] != None:
            if self.current_step_number != None:
                self.current_step = self.current_program['steps'][self.current_step_number]
            else:
                self.current_step = self.current_program['steps'][0]
                self.current_step_number = self.program_steps.index(self.current_step)
        self.program_state = False
        self.program_number = self.current_program['number']
        self.program_name = self.current_program['name']
        if self.current_step['type']=='JUMP' and self.program_jumps_left == None:
            self.program_jumps_left = self.current_step['times']
            
