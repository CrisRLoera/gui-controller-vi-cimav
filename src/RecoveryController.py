import json
import datetime
import os

class RecoveryController:
    def __init__ (self,host):
       self.host = host
       self.file = None

    def gen_recovery_file(self):
        current_time = datetime.datetime.now()
        with open('./recovery.json', 'w') as file:
            schema = {
                    "compleated": False,
                    "date": str(datetime.datetime.now().replace(microsecond=0)),
                    "output1": self.host.state_screen.output_state1,
                    "output2": self.host.state_screen.output_state2,
                    "output3": self.host.state_screen.output_state3,
                    "jumps": self.host.state_screen.program_jumps_left,
                    "time left": self.host.state_screen.time_left,
                    "last program": self.host.state_screen.program_name,
                    "last step": self.host.state_screen.current_step_number,
                    "task num":self.host.state_controller.task_num,
                    "stack":self.host.state_controller.stack_save
            }
            json.dump(schema,file, indent=8)
            file.flush()
            os.fsync(file.fileno())
            #print(schema)
    def gen_empty_recovery_file(self):
        current_time = datetime.datetime.now()
        with open('./recovery.json', 'w') as file:
            schema = {
                    "compleated": True,
                    "date": str(datetime.datetime.now().replace(microsecond=0)),
                    "output1": None,
                    "output2": None,
                    "output3": None,
                    "jumps": None,
                    "time left": None,
                    "last program": None,
                    "last step": None,
                    "task num": None,
                    "stack": None
            }
            json.dump(schema,file, indent=8)
        self.get_recovery_file()
    def get_recovery_file(self):
        try:
            with open('./recovery.json', 'r') as file:
                self.file = json.load(file)
                print(self.file)
        except FileNotFoundError:
            self.gen_empty_recovery_file()

    def checkRecovery(self):
        limit_for_recovery = 5
        self.get_recovery_file()
        lastime = datetime.datetime.strptime(self.file['date'], "%Y-%m-%d %H:%M:%S")
        current_time = datetime.datetime.now()
        #print(f'last time: {(current_time-lastime).total_seconds()}')
        if (current_time - lastime).total_seconds() > limit_for_recovery:
            if self.file != None:
                if not self.file["compleated"] and self.file['last program']!=None:
                    print("Recovering")
                    self.host.state_screen.current_program = self.host.file_controller.getProgram(self.file['last program'])
                                            # Not implemented: Register or advice of non set responsible
                    self.host.state_screen.current_step_number = self.file['last step'] 
                    self.host.state_screen.output_state1 = self.file['output1']
                    self.host.state_screen.output_state2 = self.file['output2']
                    self.host.state_screen.output_state3 = self.file['output3']
                    self.host.state_screen.program_jumps_left = self.file['jumps']
                    self.host.state_screen.time_left = self.file['time left']
                    self.host.state_controller.task_num = self.file['task num']
                    self.host.state_controller.recoverTask(self.file['stack'])
                    self.host.state_controller.changeOutputs(self.file['output1'],self.file['output2'],self.file['output3'])
                    try:
                        self.host.state_screen.changeCurrentProgram()
                        self.host.state_screen.run_current_program()
                        self.host.state_controller.restart_flow()
                        if self.host.isConnected() and self.host.state_screen.current_program['interrupt']!= None:
                            if self.host.state_screen.current_program["interrupt"] == True and self.host.state_screen.current_program ["responsible"] != None:
                                self.host.email_controller.send_interruption_email(self.host.state_screen.current_program['name'],self.host.state_screen.current_program ["responsible"])
                    except:
                        print("Recovery is not posible")
                        self.host.state_screen.current_program = {'number': None, 'name': None, 'steps': None}
                        self.host.state_screen.current_step_number = None
                        self.host.state_screen.output_state1 = False
                        self.host.state_screen.output_state2 = False
                        self.host.state_screen.output_state3 = False
                        self.host.state_screen.program_jumps_left = None
                        self.host.state_screen.time_left = None
                        self.host.state_controller.task_num = 0 
                        self.state.current_step_number = 0
                        self.host.state_controller.output1_on_time=None
                        self.host.state_controller.output2_on_time=None
                        self.host.state_controller.output3_on_time=None

                        self.stack = [None]
                        self.host.update_Screen()

