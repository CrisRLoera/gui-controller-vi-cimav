import datetime
#import RPi.GPIO as GPIO

class SOAK:
    def __init__(self,time):
        print("Created")
        self.type = "SOAK"
        self.created_time = datetime.datetime.now()
        if time <= 0:
            self.time = 0
        else:
            self.time = time

    def decrease(self):
        set_seconds = 60
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
        self.host.host.state_screen.changeOutputs(self.output1,self.output2,self.output3)
        self.host.changeOutputs(self.output1,self.output2, self.output3)
        
        



class END:
    def __init__(self,action,prog):
        self.type = "END"
        self.action = action
        self.program = prog
    	


class ControlFlow:
    def __init__(self,host):
        self.output1_pin=16
        self.output2_pin=20
        self.output3_pin=21
        
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(self.output1_pin, GPIO.OUT, initial=GPIO.HIGH)
        #GPIO.setup(self.output2_pin, GPIO.OUT, initial=GPIO.HIGH)
        #GPIO.setup(self.output3_pin, GPIO.OUT, initial=GPIO.HIGH)
        self.stack = [None]
        self.host = host
        self.current = None
        self.task_num = 0
        self.stack_save = [None]


        self.output1 = False
        self.output1_on_time = None
        self.output2 = False
        self.output2_on_time = None
        self.output3 = False
        self.output3_on_time = None

        self.conf_file = self.host.file_controller.conf_file

    def checkCurrentFlow(self, step):
            if self.host.state_screen.program_steps[step]== None:
                return 0
            self.current = self.host.state_screen.program_steps[step]
            self.step = step
            if self.stack == []:
                self.stack = [None]
            if self.current["type"] == "SET":
                if self.stack[self.task_num] == None:
                    self.stack[self.task_num] = SET(self.current["output1"],self.current["output2"],self.current["output3"],self)
                    self.stack[self.task_num].change()
                    '''
                    if self.output1:
                        GPIO.output(self.output1_pin,GPIO.HIGH)
                    else:
                        GPIO.output(self.output1_pin,GPIO.LOW)
                    if self.output2:
                        GPIO.output(self.output2_pin,GPIO.HIGH)
                    else:
                        GPIO.output(self.output2_pin,GPIO.LOW)
                    if self.output3:
                        GPIO.output(self.output3_pin,GPIO.HIGH)
                    else:
                        GPIO.output(self.output3_pin,GPIO.LOW)
                    '''
                    self.host.state_screen.current_step_number += 1
                    self.stack[self.task_num] = None
                    if self.host.isConnected() and self.host.state_screen.current_program['step change notify']!= None:
                        if self.host.state_screen.current_program["step change notify"] == True and self.host.state_screen.current_program ["responsible"] != None:
                            self.host.email_controller.send_step_change_email(self.host.state_screen.current_program["responsible"],"SET",step)
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
                    if self.host.isConnected() and self.host.state_screen.current_program['step change notify']!= None:
                        if self.host.state_screen.current_program["step change notify"] == True and self.host.state_screen.current_program ["responsible"] != None:
                            self.host.email_controller.send_step_change_email(self.host.state_screen.current_program["responsible"],"SOAK",step)

            elif self.current["type"] == "JUMP":
                if (self.task_num - 1)>=0:
                    if self.stack[self.task_num-1].step_id == step:
                        self.task_num -=1
                        if self.stack[self.task_num].times == 0:
                            self.host.state_screen.current_step_number += 1
                            self.stack[self.task_num]=None
                            if self.host.isConnected() and self.host.state_screen.current_program['step change notify']!= None:
                                if self.host.state_screen.current_program["step change notify"] == True and self.host.state_screen.current_program ["responsible"] != None:
                                    self.host.email_controller.send_step_change_email(self.host.state_screen.current_program["responsible"],"JUMP",step)
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
                    self.stack[self.task_num] = END(self.current['action'],self.current['program'])
                elif self.stack[self.task_num].action == 'PowerOFF':
                    print("apagando")
                    self.host.state_screen.turnOff()
                    self.host.state_screen.current_program = self.host.file_controller.getProgram(self.current['program'])
                    self.host.state_screen.current_step_number = 0
                    self.host.state_screen.changeCurrentProgram()
                    self.stack = [None]
                    self.current = None
                    self.task_num = 0
                    self.stack_save = [None]
                    self.host.state_screen.program_state = False
                    if self.host.isConnected() and self.host.state_screen.current_program['end notify']!= None:
                        if self.host.state_screen.current_program["end notify"] == True and self.host.state_screen.current_program ["responsible"] != None:
                            self.host.email_controller.send_program_finalize_email(self.host.state_screen.current_program ["responsible"],"PowerOFF")
                elif self.stack[self.task_num].action == 'Restart':
                    self.host.state_screen.current_step_number = 0
                    self.stack = [None]
                    self.current = None
                    self.task_num = 0
                    self.stack_save = [None]
                    if self.host.isConnected() and self.host.state_screen.current_program['end notify']!= None:
                        if self.host.state_screen.current_program["end notify"] == True and self.host.state_screen.current_program ["responsible"] != None:
                            self.host.email_controller.send_program_finalize_email(self.host.state_screen.current_program ["responsible"],"Restart")
                elif self.stack[self.task_num].action == 'SwitchProgram':
                    self.host.state_screen.current_program = self.host.file_controller.getProgram(self.current['program'])
                    self.host.state_screen.current_step_number = 0
                    self.host.state_screen.changeCurrentProgram()
                    self.stack = [None]
                    self.current = None
                    self.task_num = 0
                    self.stack_save = [None]
                    self.host.state_screen.program_state = True
                    if self.host.isConnected() and self.host.state_screen.current_program['end notify']!= None:
                        if self.host.state_screen.current_program["end notify"] == True and self.host.state_screen.current_program ["responsible"] != None:
                            end_msg = "Switch Program to {self.current['program']}"
                            self.host.email_controller.send_program_finalize_email(self.host.state_screen.current_program ["responsible"],end_msg)
            
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
            self.host.state_screen.update()

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

    def changeOutputs(self, out1,out2,out3):
        self.output1 = out1
        self.output2 = out2
        self.output3 = out3

    def trackOutputs(self):
        set_seconds = 60
        current_time = datetime.datetime.now()
        if self.output1 and self.output1_on_time !=None:
            if (current_time - self.output1_on_time).total_seconds() > set_seconds:
                for device in self.conf_file['maintenance devices']:
                    if device['output']=="output1":
                        device['output on time'] += 1
        elif self.output1 and self.output1_on_time == None:
            self.output1_on_time = datetime.datetime.now()
        elif self.output1 == False:
            self.output1_on_time = None

        if self.output2 and self.output2_on_time !=None:
            if (current_time - self.output2_on_time).total_seconds() > set_seconds:
                if (current_time - self.output2_on_time).total_seconds() > set_seconds:
                    for device in self.conf_file['maintenance devices']:
                        if device['output']=="output2":
                            device['output on time'] += 1
        elif self.output2 and self.output2_on_time == None:
            self.output2_on_time = datetime.datetime.now()
        elif self.output2 == False:
            self.output2_on_time = None

        if self.output3 and self.output3_on_time !=None:
            if (current_time - self.output3_on_time).total_seconds() > set_seconds:
                if (current_time - self.output3_on_time).total_seconds() > set_seconds:
                    for device in self.conf_file['maintenance devices']:
                        if device['output']=="output3":
                            device['output on time'] += 1
        elif self.output3 and self.output3_on_time == None:
            self.output3_on_time = datetime.datetime.now()
        elif self.output3 == False:
            self.output3_on_time = None
        self.host.file_controller.updateConf()
        self.host.file_controller.loadConf()

