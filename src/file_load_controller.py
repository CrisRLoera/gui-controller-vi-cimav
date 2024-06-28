import os
import json

class FileLoadController:
    def __init__(self):
        self.path_programs_list = self.getProgramsPaths()
        self.programs_list = self.getProgramsList()
        self.conf_file = self.loadConf()
        self.current_created_id = self.conf_file["creation_id"]

    def loadConf(self):
        with open ("./conf.json") as file:
            conf_file = json.load(file)
            return conf_file

    def updateConf(self):
        with open ("./conf.json", "w") as file:
            json.dump(self.conf_file,file, indent=8)

    def reload(self):
        self.path_programs_list = self.getProgramsPaths()
        self.programs_list = self.getProgramsList()
        self.conf_file = self.loadConf()

    def getProgramsPaths(self):
        programs_path = '../programs'
        base_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(base_path, programs_path)
        files = os.listdir(path)
        program_files = [file for file in files if file.endswith('.json')]
        return program_files

    def getProgramsList(self):
        programs_list = []
        for program_path in self.path_programs_list:
            base_path = os.path.abspath(os.path.dirname(__file__))
            path = os.path.join(base_path,'../programs/'+ program_path)
            with open (path) as file:
                programs_list.append(json.load(file))

        return programs_list

    def getProgram(self,name):
        for program in self.programs_list:
            if name == program['name']:
                print(program)
                return program

    def getProgramByNum(self,name):
        for program in self.programs_list:
            if name == program['number']:
                return program

    def diffName(self,num,name):
        for program in self.programs_list:
            if program['number']==num:
                pass
            else:
                if program['name']==name:
                    return False
        return True

    def saveProgram(self,num,schema):
        prog = self.getProgramByNum(num)
        programs_path = '../programs/'+prog['file_name']
        base_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(base_path, programs_path)
        with open (path,'w') as file:
            json.dump(schema,file, indent=8)

    def createProgram(self,name):
        schema = {
            "number": int(self.conf_file['creation_id']),
            "name": f"{name}",
            "steps": [{}],
            "file_name": f"{name}.json"}
        print(schema["file_name"])
        programs_path = '../programs/'+schema['file_name']
        base_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(base_path, programs_path)
        with open (path,'w') as file:
            json.dump(schema,file, indent=8)
        self.conf_file["creation_id"]+=1
        self.updateConf()
        self.reload()

    def cloneProgram(self,name):
        prog = self.getProgram(name)
        schema = {
            "number": int(self.conf_file['creation_id']),
            "name": f"{name}-copy",
            "steps": prog['steps'],
            "file_name": f"{name}-copy.json"}
        programs_path = '../programs/'+schema['file_name']
        base_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(base_path, programs_path)
        with open (path,'w') as file:
            json.dump(schema,file, indent=8)
        self.conf_file["creation_id"]+=1
        self.updateConf()
        self.reload()


    def deleteProgram(self,name):
        prog = self.getProgram(name)
        programs_path = '../programs/'+prog['file_name']
        base_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(base_path, programs_path)
        os.remove(path)
        self.reload()

    def changeMaintenanceResponsible(self,email):
        self.conf_file["maintenance"]=email
        self.updateConf()
        self.reload()
