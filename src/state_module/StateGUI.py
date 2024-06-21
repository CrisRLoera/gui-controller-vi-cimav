from customtkinter import CTkLabel

class StateGUI:
    def __init__(self,app):
        self.title = CTkLabel(app, text='Menu')
        self.current_program = {'number': None, 'name': None, 'steps': None}
        self.current_step = None
        self.program_number = self.current_program['number']
        self.program_name = self.current_program['name']
        self.program_steps = self.current_program['steps']
        self.name_gui = CTkLabel(app, text=f"Program name:{self.program_name}")
        self.number_gui = CTkLabel(app, text=f"Program number:{self.program_number}")
        self.current_step_gui = CTkLabel(app, text=f"Current step:{self.current_step}")
        

    def update(self):
        self.title.pack()
        self.name_gui.pack()
        self.number_gui.pack()
        self.current_step_gui.pack()

#    def updateStateData(self):


#    def changeCurrentProgram(self):

