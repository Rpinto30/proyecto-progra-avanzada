import json
import os

class DataBase:
    def __init__(self):
        self.__data_base_path = os.path.dirname(os.path.abspath(__file__)) #Ruta relativa del archivo
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
    @instructors.setter
    def instructors(self, ist): self.__instructors = ist
    @property
    def courses(self): return self.__courses



    #Reutilizando parte de la lógica del parcial
    #https://github.com/Rpinto30/Parcial-Progra-avanzada/blob/main/save_data.py
    def save_data(self, name_file:str):
        path_data = os.path.join(self.__data_base_path, f"{name_file}.json")
        with open(path_data, mode="w", encoding="utf-8") as write_file:
            if name_file == 'students':
                json.dump(self.__students, write_file)
            elif name_file == 'instructors':
                json.dump(self.__instructors, write_file)
            elif name_file == 'courses':
                json.dump(self.__courses, write_file)

    def load_data(self, name_file):
        path_data = os.path.join(self.__data_base_path, f"{name_file}.json")
        try:
            with open(path_data, mode="r", encoding="utf-8") as read_file:
                return json.load(read_file)
        except FileNotFoundError:
            with open(path_data, mode="w", encoding="utf-8") as read_file:
                json.dump({}, read_file)
            return {}


data = DataBase()
