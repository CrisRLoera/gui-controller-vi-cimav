import os
import json

class FileLoadController:
    def __init__(self):
        self.path_programs_list = self.getProgramsPaths()
        self.programs_list = self.getProgramsList()
    
    def getProgramsPaths(self):
        programs_path = '../programs'
        base_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(base_path, programs_path)
        files = os.listdir(path)
        program_files = [file for file in files if file.endswith('.json')]
        return files

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
                return program

