import json
import datetime

class RecoveryController:
    def __init__ (self,host):
       self.host = host
       self.file = None

    def checkClock(self,time):
        flag = None
        self.get_recovery_file()
        lastime = datetime.datetime.strptime(self.file['date'], "%Y-%m-%d %H:%M:%S")
        current_time = datetime.datetime.now()
        #print((current_time-lastime).total_seconds())
        self.gen_recovery_file()

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
                    "last step": self.host.state_screen.current_step_number
            }
            json.dump(schema,file, indent=8)
            #print(schema)

    def get_recovery_file(self):
        with open('./recovery.json', 'r') as file:
            self.file = json.load(file)

    def checkRecovery(self):
        limit_for_recovery = 5
        self.get_recovery_file()
        lastime = datetime.datetime.strptime(self.file['date'], "%Y-%m-%d %H:%M:%S")
        current_time = datetime.datetime.now()
        print(f'last time: {(current_time-lastime).total_seconds()}')
        if (current_time - lastime).total_seconds() > limit_for_recovery:
            if self.file != None:
                if not self.file["compleated"] and self.file['last program']!=None:
                    print("Recovering")
                    self.host.state_screen.current_program = self.host.file_controller.getProgram(self.file['last program'])
                    self.host.state_screen.current_step_number = self.file['last step']
    
                    self.host.state_screen.output_state1 = self.file['output1']
                    self.host.state_screen.output_state2 = self.file['output2']
                    self.host.state_screen.output_state3 = self.file['output3']
    
                    self.host.state_screen.program_jumps_left = self.file['jumps']
                    self.host.state_screen.time_left = self.file['time left']
    
                    self.host.state_screen.changeCurrentProgram()
                    self.host.state_screen.run_current_program()
