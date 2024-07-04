from customtkinter import CTkLabel, CTkButton, CTkOptionMenu, CTkToplevel, CTkEntry, CTkFrame

class ProgramGUI:
    def __init__(self,data,nav,notify,host,state,editor):
        self.host = host
        self.app = host.gui_app
        self.state = state
        self.editor = editor
        self.main_frame = CTkFrame(data)
        self.main_frame.grid_rowconfigure((0,1,2,3,4),weight=1)
        self.main_frame.grid_columnconfigure((0),weight=1)
        #self.menu = CTkLabel(app,text="Programas")
        self.selected = None
        self.flag_unselected = CTkLabel(notify, text="Select a program to load")
        
        self.create_program_button = CTkButton(nav, text="Crear", command=self.create_program)
        self.cancel_program_gui = CTkButton(nav,text='Cancel', command=self.cancel)

        self.program_selector_gui = CTkOptionMenu(self.main_frame, command=self.setSelection)
        self.load_program_gui = CTkButton(self.main_frame,text="Load",command=self.update_program)
        self.edit_program_gui = CTkButton(self.main_frame,text="Edit",command=self.mv_to_edit)
        self.delete_program_button = CTkButton(self.main_frame, text="Del", command=self.delete_program)
        self.clone_program_button = CTkButton(self.main_frame, text="Clone", command=self.clone_program) 
        
        self.program_selector_gui.set("")
        self.setProgramsList()

        self.err_empty_steps = False
        self.err_empty_steps_msg = CTkLabel(notify, text="Error: Can´t load the selected program is empty")

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
        self.main_frame.grid(row=0,column=0,columnspan=2,sticky="nswe")
        self.setProgramsList()
        #self.menu.pack()
        self.create_program_button.grid(row=0,column=0)
        self.cancel_program_gui.grid(row=0,column=2)

        self.program_selector_gui.grid(row=0,column=0)
        if self.selected == None:
            self.load_program_gui.grid_forget()
            self.edit_program_gui.grid_forget()
            self.delete_program_button.grid_forget()
            self.clone_program_button.grid_forget()
        else:
            self.load_program_gui.grid(row=1,column=0)
            self.edit_program_gui.grid(row=2,column=0)
            self.delete_program_button.grid(row=3,column=0)
            self.clone_program_button.grid(row=4,column=0)
        if self.selected != None:
            self.flag_unselected.grid_forget()
        else:
            self.flag_unselected.grid(row=0,column=0)
        if self.err_empty_steps:
            self.err_empty_steps_msg.grid(row=0,column=0)
        else:
            self.err_empty_steps_msg.grid_forget()


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
