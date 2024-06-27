from customtkinter import CTkLabel, CTkButton, CTkOptionMenu, CTkToplevel, CTkEntry

class ProgramGUI:
    def __init__(self,app,host,state,editor):
        self.host = host
        self.app = app
        self.state = state
        self.editor = editor
        self.menu = CTkLabel(app,text="Programas")
        self.program_selector_gui = CTkOptionMenu(app, command=self.setSelection)
        self.program_selector_gui.set("")
        self.setProgramsList()
        self.load_program_gui = CTkButton(app,text="Load",command=self.update_program)
        self.edit_program_gui = CTkButton(app,text="Edit",command=self.mv_to_edit)
        self.cancel_program_gui = CTkButton(app,text='Cancel', command=self.cancel)
        self.selected = None
        self.flag_unselected = CTkLabel(app, text="Select a program to load")
        
        self.create_program_button = CTkButton(app, text="Crear", command=self.create_program)
        self.clone_program_button = CTkButton(app, text="Clone", command=self.clone_program) 
        self.delete_program_button = CTkButton(app, text="Del", command=self.delete_program)

        self.err_empty_steps = False
        self.err_empty_steps_msg = CTkLabel(app, text="Error: Can´t load the selected program is empty")

    def create_program(self):
        popup = CTkToplevel(self.app)
        popup.title("Program Name")
        popup.geometry("300x150")
        popup_label = CTkLabel(popup, text="New program name:")
        popup_label.pack()
        popup_entry = CTkEntry(popup)
        popup_entry.pack()
        close_button = CTkButton(popup, text="Create", command=lambda: self.create_event(popup_entry.get(),popup))
        close_button.pack()

    def clone_program(self):
        if self.selected != None:
            self.host.file_controller.cloneProgram(self.selected)
            self.program_selector_gui.set("")
            self.update()

    def create_event(self,name,popup):
        self.host.file_controller.createProgram(str(name))
        popup.destroy()
        self.program_selector_gui.set("")
        self.update()

    def delete_program(self):
        if self.selected != None:
            self.host.file_controller.deleteProgram(self.selected)
            self.program_selector_gui.set("")
            self.update()
            
    def update(self):
        self.setProgramsList()
        self.menu.pack()
        self.program_selector_gui.pack()
        self.create_program_button.pack()
        if self.selected == None:
            self.load_program_gui.pack_forget()
            self.edit_program_gui.pack_forget()
            self.delete_program_button.pack_forget()
            self.clone_program_button.pack_forget()
        else:
            self.load_program_gui.pack()
            self.edit_program_gui.pack()
            self.delete_program_button.pack()
            self.clone_program_button.pack()
        self.cancel_program_gui.pack()
        if self.selected != None:
            self.flag_unselected.pack_forget()
        else:
            self.flag_unselected.pack()
        if self.err_empty_steps:
            self.err_empty_steps_msg.pack()
        else:
            self.err_empty_steps_msg.pack_forget()


    def setSelection(self, choice):
        self.selected = choice
        self.update()

    def mv_to_edit(self):
        self.program_selector_gui.set("")
        if self.selected != None:
            self.editor.program = self.host.file_controller.getProgram(self.selected)
            self.editor.loadProgram()
            self.host.current_screen = 'editor'
            self.host.update_Screen()



    def update_program(self):
        if self.selected != None:
            temp = self.host.file_controller.getProgram(self.selected) 
            print(temp)
            if temp['steps']==[{}]:
                self.err_empty_steps = True
                self.update()
            else:
                self.err_empty_steps = False
                self.state.current_program = temp
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
