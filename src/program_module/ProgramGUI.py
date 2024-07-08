from customtkinter import CTkLabel, CTkButton, CTkOptionMenu, CTkToplevel, CTkEntry, CTkFrame
from src.keyboard_module import VirtualKeyboard

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
        
        self.create_program_button = CTkButton(nav, text="Create", command=self.create_program)
        self.cancel_program_gui = CTkButton(nav,text='Cancel', command=self.cancel)

        self.program_selector_gui = CTkOptionMenu(self.main_frame, command=self.setSelection)
        self.load_program_gui = CTkButton(self.main_frame,text="Load",command=self.update_program)
        self.edit_program_gui = CTkButton(self.main_frame,text="Edit",command=self.mv_to_edit)
        self.delete_program_button = CTkButton(self.main_frame, text="Del", command=self.delete_program)
        self.clone_program_button = CTkButton(self.main_frame, text="Clone", command=self.clone_program)
        self.popup_label = CTkLabel(self.main_frame, text="New program name:")
        self.popup_entry = CTkEntry(self.main_frame)
        self.popup_entry.bind("<Button-1>",self.show_keyboard)
        self.create_button = CTkButton(self.main_frame, text="Confirm", command=lambda: self.create_event(self.popup_entry.get()))
        self.cancel_creation_button = CTkButton(self.main_frame, text="Cancel", command=self.cancel_creation)
        
        self.program_selector_gui.set("")
        self.setProgramsList()

        self.err_empty_steps = False
        self.err_empty_steps_msg = CTkLabel(notify, text="Error: Can´t load the selected program is empty")
        self.onCreation= False
        self.keyboard_frame = None

    def create_program(self):
        self.onCreation = True
        self.host.update_Screen()
    
    def show_keyboard(self,event):
        if self.keyboard_frame is not None:
            self.keyboard_frame.destroy()
        self.keyboard_frame = VirtualKeyboard(self.host.gui_app, self.popup_entry)
        self.keyboard_frame.grid(row=4,column=0)

    def cancel_creation(self):
        self.onCreation= False
        self.host.update_Screen()

    def clone_program(self):
        if self.selected != None:
            self.host.file_controller.cloneProgram(self.selected)
            self.program_selector_gui.set("")
            self.host.update_Screen()

    def create_event(self,name):
        self.host.file_controller.createProgram(str(name))
        self.program_selector_gui.set("")
        self.onCreation= False
        self.update()

    def delete_program(self):
        if self.selected != None:
            self.host.file_controller.deleteProgram(self.selected)
            self.program_selector_gui.set("")
            self.update()
            
    def update(self):
        self.main_frame.grid(row=0,column=0,columnspan=2,sticky="nswe")

        self.setProgramsList()

        self.cancel_program_gui.grid(row=0,column=2)
        if not self.onCreation:
            self.popup_label.grid_forget()
            self.popup_entry.grid_forget()
            self.create_button.grid_forget()
            self.cancel_creation_button.grid_forget()

            self.create_program_button.grid(row=0,column=0)
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
        else:
            self.popup_label.grid(row=0, column=0)
            self.popup_entry.grid(row=1,column=0)
            self.create_button.grid(row=2,column=0)
            self.cancel_creation_button.grid(row=3,column=0)

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
        self.onCreation= False
        self.host.update_Screen()

    def setProgramsList(self):
        self.program_selector_gui.configure(values=[name['name'] for name in self.host.file_controller.programs_list])
