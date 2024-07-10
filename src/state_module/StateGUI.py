from os import pardir
from customtkinter import CTkLabel, CTkButton, CTkEntry, CTkFrame, CTkFont

class StateGUI:
    def __init__(self,data,nav,notify,host):
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

        self.def_font = CTkFont(family="Inter",size=20)
        self.dark_gray = "#3d3846"
        
        self.left_frame = CTkFrame(data,fg_color="#F5F5F9")
        self.left_frame.grid_rowconfigure((0,1,2,3,4,5),weight=1)
        self.left_frame.grid_columnconfigure((0),weight=1)
        self.right_frame = CTkFrame(data,fg_color="#F5F5F9")
        self.right_frame.grid_rowconfigure((0),weight=1)
        self.right_frame.grid_columnconfigure((0),weight=1)
        #self.title = CTkLabel(app, text='Menu')
        self.program_state_gui = CTkLabel(self.left_frame, text=f'State: {self.program_state}', font=self.def_font)
        self.name_gui = CTkLabel(self.left_frame, text=f"Program name: {self.program_name}", font=self.def_font)
        self.number_gui = CTkLabel(self.left_frame, text=f"Program number: {self.program_number}", font=self.def_font)

        self.current_step_gui = CTkLabel(self.right_frame, text=f"Current step: {self.current_step_number}", font=self.def_font)
        self.jumps_left_gui = CTkLabel(self.right_frame, font=self.def_font)
        self.soak_time_left_gui = CTkLabel(self.right_frame, font=self.def_font)

        self.out1_label = CTkLabel(self.left_frame,font=self.def_font)
        self.out2_label = CTkLabel(self.left_frame,font=self.def_font)
        self.out3_label = CTkLabel(self.left_frame,font=self.def_font)

        self.run_program_button_gui = CTkButton(nav, command=self.run_current_program, font=self.def_font, width=80,height=40, border_color="#3d3846", border_width=2, text_color="black")
        self.selec_program_button_gui = CTkButton(nav, text='Program', command=self.changeProgramScreen, font=self.def_font, width=100, height=40,fg_color="#dad8e5", hover_color="#c1bed2", border_color="#3d3846", border_width=2, text_color="black")

        self.err_no_current_program = False
        self.err_no_crnt_prg_text = CTkLabel(notify,image=self.host.file_controller.icons['alert'], text='Error: No current program to run', compound="left")
        self.empty = CTkLabel(notify, text=" ")

    def update(self):
        self.right_frame.grid(row=0,column=1,sticky="nswe")
        self.left_frame.grid(row=0,column=0,sticky="nswe")
        self.name_gui.configure(text=f'Program name: {self.program_name}')
        self.number_gui.configure(text=f'Program number: {self.program_number}')
        self.current_step_gui.configure(text=f'Current step: {self.current_step_number}')
        if self.program_jumps_left != None:
            self.jumps_left_gui.configure(text=f"Jumps left: {self.program_jumps_left}")
            self.jumps_left_gui.grid(row=1,column=0)
        else:
            self.jumps_left_gui.pack_forget()
        if self.soak_time_left != None:
            self.soak_time_left_gui.configure(text=f"Soak time left: {self.soak_time_left}")
            self.soak_time_left_gui.grid(row=2,column=0)
        else:
            self.soak_time_left_gui.pack_forget()
        self.out1_label.configure(text=f"Output1: {'ON'if self.output_state1 else 'OFF'}")
        self.out2_label.configure(text=f"Output2: {'ON'if self.output_state2 else 'OFF'}")
        self.out3_label.configure(text=f"Output3: {'ON'if self.output_state3 else 'OFF'}")
        
        self.program_state_gui.grid(row=0,column=0)
        self.name_gui.grid(row=1,column=0)
        self.number_gui.grid(row=2,column=0)
        self.out1_label.grid(row=3,column=0)
        self.out2_label.grid(row=4,column=0)
        self.out3_label.grid(row=5,column=0)

        self.current_step_gui.grid(row=0,column=0)

        self.program_state_gui.configure(text=f"State: {'Running'if self.program_state else 'Stop'}")
        self.run_program_button_gui.configure(text='Stop'if self.program_state else 'Run')
        self.run_program_button_gui.grid(row=0,column=0, sticky="s",padx=3, pady=3)
        self.program_steps = self.current_program['steps']
        if self.program_state == False:
            self.selec_program_button_gui.grid(row=0,column=2, sticky="s")
            self.run_program_button_gui.configure(fg_color="#06f432",hover_color="#25f648")
        else:
            self.selec_program_button_gui.grid_forget()
            self.run_program_button_gui.configure(fg_color="#e01b24",hover_color="#f63d45")
        if self.err_no_current_program:
            self.err_no_crnt_prg_text.grid(row=0,column=0)
            self.empty.grid_forget()
        else:
            self.empty.grid(row=0,column=0)
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
            self.host.update_Screen()
        else:
            self.program_state = True
            self.host.update_Screen()
            self.host.recovery_controller.gen_recovery_file()

    def turnOff(self):
        self.host.recovery_controller.gen_empty_recovery_file()
        self.program_jumps_left = None
        self.soak_time_left = None
        self.program_state = False
        self.current_step_number = 0
        self.host.update_Screen()


    def changeOutputs(self,out1,out2,out3):
        self.output_state1 = out1
        self.output_state2 = out2
        self.output_state3 = out3


    def changeProgramScreen(self):
        self.host.current_screen = 'program'
        self.host.update_Screen()

    def changeCurrentProgram(self):
        print("Current program")
        print(self.current_program)
        if self.current_program != None:
            if self.current_program['steps'] != None:
                self.program_steps = self.current_program['steps']
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
            
