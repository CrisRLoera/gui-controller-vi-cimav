from customtkinter import CTkLabel, CTkButton

class ProgramGUI:
    def __init__(self,app,host,state):
        self.host = host
        self.state = state
        self.menu = CTkLabel(app,text="Programas")
        self.program = CTkButton(app,text="1",command=self.update_program)

    def update(self):
        self.menu.pack()
        self.program.pack()

    def update_program(self):
        self.state.current_program = self.host.file_controller.getProgram(1)
        self.state.changeCurrentProgram()
        self.host.current_screen = 'state'
        self.host.update_Screen()
