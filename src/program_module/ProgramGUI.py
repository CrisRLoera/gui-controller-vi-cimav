from customtkinter import CTkLabel, CTkButton, CTkOptionMenu

class ProgramGUI:
    def __init__(self,app,host,state):
        self.host = host
        self.state = state
        self.menu = CTkLabel(app,text="Programas")
        self.program_selector_gui = CTkOptionMenu(app, command=self.setSelection)
        self.program_selector_gui.set("")
        self.setProgramsList()
        self.load_program_gui = CTkButton(app,text="Load",command=self.update_program)
        self.cancel_program_gui = CTkButton(app,text='Cancel', command=self.cancel)
        self.selected = None
        self.flag_unselected = CTkLabel(app, text="Select a program to load")

    def update(self):
        self.menu.pack()
        self.program_selector_gui.pack()
        self.load_program_gui.pack()
        self.cancel_program_gui.pack()
        if self.selected != None:
            self.flag_unselected.pack_forget()
        else:
            self.flag_unselected.pack()

    def setSelection(self, choice):
        self.selected = choice
        self.update()


    def update_program(self):
        if self.selected != None:
            self.state.current_program = self.host.file_controller.getProgram(self.selected)
            self.state.changeCurrentProgram()
            self.host.current_screen = 'state'
            self.host.update_Screen()

    def cancel(self):
        self.program_selector_gui.set("")
        self.selected = None
        self.host.current_screen = 'state'
        self.host.update_Screen()

    def setProgramsList(self):
        self.program_selector_gui.configure(values=[name['name'] for name in self.host.file_controller.programs_list])
