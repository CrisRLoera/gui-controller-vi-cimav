import datetime
class SOAK:
    def __init__(self,time):
        print("Created")
        self.type = "SOAK"
        self.created_time = datetime.datetime.now()
        self.time = None
        if time <= 0:
            self.time = 0
        else:
            self.time = time

    def decrease(self):
        set_seconds = 5
        current_time = datetime.datetime.now()
        if (current_time - self.created_time).total_seconds() > set_seconds:
            self.time -=1
            self.created_time = datetime.datetime.now()


class JUMP:
    def __init__(self, times,step,step_id):
        self.type = "JUMP"
        self.times = times
        self.step = step
        self.step_id = step_id
    def decrease(self):
        self.times -= 1
        print(self.times)


class SET:
    def __init__(self,output1,output2,output3,host):
        self.type = "SET"
        self.output1 = output1
        self.output2 = output2
        self.output3 = output3
        self.host = host

    # Definir funcion para comunicar con las salidas GPIO
    def change(self):
        self.host.state_screen.changeOutputs(self.output1,self.output2,self.output3)
        

class END:
    def __init__(self,action,prog):
        self.type = "END"
        self.action = action
        self.program = prog
    	


class ControlFlow:
    def __init__(self,host):
        self.stack = [None]
        self.host = host
        self.current = None
        self.task_num = 0
        self.stack_save = [None]

    def checkCurrentFlow(self, step):
            if self.host.state_screen.program_steps[step]== None:
                return 0
            self.current = self.host.state_screen.program_steps[step]
            self.step = step
            if self.current["type"] == "SET":
                if self.stack[self.task_num] == None:
                    self.stack[self.task_num] = SET(self.current["output1"],self.current["output2"],self.current["output3"],self.host)
                    self.stack[self.task_num].change()
                    self.host.state_screen.current_step_number += 1
                    self.stack[self.task_num] = None
                    if self.host.isConnected() and self.host.state_screen.current_program["step change notify"] == 1:
                        self.host.email_controller.send_interruption_email(self.host.state_screen.current_program ["responsible"])
            elif self.current["type"] == "SOAK":
                isOver = False
                if self.stack[self.task_num] == None:
                    self.stack[self.task_num] = SOAK(self.current["time"])
                else:
                    self.stack[self.task_num].decrease()
                if self.stack[self.task_num].time == 0:
                    isOver = True
                else:
                    isOver = False
                if isOver:
                    self.host.state_screen.current_step_number += 1
                    self.stack[self.task_num] = None
            elif self.current["type"] == "JUMP":
                if (self.task_num - 1)>=0:
                    if self.stack[self.task_num-1].step_id == step:
                        self.task_num -=1
                        if self.stack[self.task_num].times == 0:
                            self.host.state_screen.current_step_number += 1
                            self.stack[self.task_num]=None
                        else:
                            self.stack[self.task_num].decrease()
                            self.host.state_screen.current_step_number = self.stack[self.task_num].step
                            self.stack.append(None)
                            self.task_num += 1
                    else:
                        if self.stack[self.task_num] == None:
                            self.stack.append(None)
                            self.stack[self.task_num]=JUMP(self.current["times"],self.current["step"],step)
                            self.stack[self.task_num].decrease()
                            self.host.state_screen.current_step_number = self.stack[self.task_num].step
                            self.task_num += 1
                else:
                    if self.stack[self.task_num] == None:
                        self.stack.append(None)
                        self.stack[self.task_num]=JUMP(self.current["times"],self.current["step"],step)
                        self.stack[self.task_num].decrease()
                        self.host.state_screen.current_step_number = self.stack[self.task_num].step
                        self.task_num += 1

            elif self.current["type"] == "END":
                print(self.task_num)
                if self.stack[self.task_num] == None:
                    self.stack[self.task_num] = END(self.current['action'],self.current['program'])
                elif self.stack[self.task_num].action == 'PowerOFF':
                    print("apagando")
                    self.host.state_screen.turnOff()
                elif self.stack[self.task_num].action == 'Restart':
                    self.host.state_screen.current_step_number = 0
                    self.stack = [None]
                    self.current = None
                    self.task_num = 0
                    self.stack_save = [None]
                elif self.stack[self.task_num].action == 'SwitchProgram':
                    self.host.state_screen.current_program = self.host.file_controller.getProgram(self.current['program'])
                    self.host.state_screen.current_step_number = 0
                    self.host.state_screen.changeCurrentProgram()
                    self.stack = [None]
                    self.current = None
                    self.task_num = 0
                    self.stack_save = [None]
            if self.stack == []:
                self.stack = [None]
            if self.stack != None and self.stack != [None]: 
                #print([name.type for name in self.stack if name != None])
                #print(self.stack)
                if len(self.stack)>1:
                    if self.stack[self.task_num-1]!= None:
                        if self.stack[self.task_num-1].type=="JUMP":
                            self.host.state_screen.program_jumps_left = self.stack[self.task_num-1].times
                if self.stack[self.task_num] == None:
                    pass
                else:
                    if self.stack[self.task_num].type=="SOAK":
                        self.host.state_screen.soak_time_left = self.stack[self.task_num].time
            self.stack_save = self.transformJSON()

    def transformJSON(self):
        temp_stack = []
        if self.stack != [None] and self.stack != None:
            for stack_element in self.stack:
                if stack_element == None:
                    continue
                if stack_element.type == "SET":
                    temp_stack.append({
                        "type":"SET",
                        "output1":stack_element.output1,
                        "output2":stack_element.output2,
                        "output3":stack_element.output3})
                elif stack_element.type == "SOAK":
                    temp_stack.append({
                        "type":"SOAK",
                        "time":stack_element.time})
                elif stack_element.type == "JUMP":
                    temp_stack.append({
                        "type":"JUMP",
                        "times":stack_element.times,
                        "step":stack_element.step,
                        "step_id":stack_element.step_id})
                elif stack_element.type == "END":
                    temp_stack.append({
                        "type":"END",
                        "action":stack_element.action,
                        "program":stack_element.program})
        return temp_stack


    def recoverTask(self,stack):
        self.stack = []
        for stk_elm in stack:
            if stk_elm == {} or stk_elm == None:
                self.stack.append(None)
            elif stk_elm["type"] == "SET":
                self.stack.append(SET(stk_elm["output1"],stk_elm["output2"],stk_elm["output3"],self.host))
            elif stk_elm["type"] == "SOAK":
                self.stack.append(SOAK(stk_elm["time"]))
            elif stk_elm["type"] == "JUMP":
                self.stack.append(JUMP(stk_elm["times"],stk_elm["step"],stk_elm["step_id"]))
            elif stk_elm["type"] == "END":
                self.stack.append(END(stk_elm["action"],stk_elm["program"]))
 
