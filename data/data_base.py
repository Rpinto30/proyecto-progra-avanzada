import json
from os import path

class DataBase:
    def __init__(self):
        self.__students = {}
        self.__instructors = {}
        self.__courses = {}

        self.__students = self.load_data('students')
        self.__instructors = self.load_data('instructors')
        self.__courses = self.load_data('courses')

    @property
    def students(self): return self.__students
    @students.setter
    def students(self, st): self.__students = st
    @property
    def instructors(self): return self.__instructors
    @property
    def courses(self): return self.__courses

    #Reutilizando parte de la lógica del parcial
    #https://github.com/Rpinto30/Parcial-Progra-avanzada/blob/main/save_data.py
    def save_data(self, name_file:str):
        path_data = path.join('data', f"{name_file}.json")
        with open(path_data, mode="w", encoding="utf-8") as write_file:
            if name_file == 'students':
                json.dump(self.__students, write_file)
            elif name_file == 'instructors':
                json.dump(self.__instructors, write_file)
            elif name_file == 'courses':
                json.dump(self.__courses, write_file)

    def load_data(self, name_file):
        try:
            path_data = path.join('data', f"{name_file}.json")
            with open(path_data, mode="r", encoding="utf-8") as read_file:
                return json.load(read_file)
        except FileNotFoundError:
            self.save_data(name_file)
            return {}

