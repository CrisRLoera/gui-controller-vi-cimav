import datetime
class SOAK:
    def __init__(self,time):
        self.type = "SOAK"
        self.created_time = datetime.datetime.now()
        self.time = None
        if time <= 0:
            self.time = 0
        else:
            self.time = time

    def decrease(self):
        current_time = datetime.datetime.now()
        if (current_time - self.created_time).total_seconds() > 5:
            self.time -=1


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
        print("cambie las salidas")
        self.host.state_screen.changeOutputs(self.output1,self.output2,self.output3)
        

class END:
    def __init__(self,action):
        self.type = "END"
        self.action = action
    	


class ControlFlow:
    def __init__(self,host):
        self.stack = [None]
        self.host = host
        self.current = None
        self.task_num = 0

    def checkCurrentFlow(self, step):
            print(f"Step: {step}")
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
                if self.stack[self.task_num] == None:
                    self.stack[self.task_num] = END(self.current['action'])
                elif self.stack[self.task_num].action == 'PowerOFF':
                    print("apagando")
            if self.stack == []:
                self.stack = [None]
            if self.stack != None or self.stack != [None]: 
                print([name.type for name in self.stack if name != None])
                #print(self.stack)
            else:
                print("None!")

    def transforJSON():
        pass
