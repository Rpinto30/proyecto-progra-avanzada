import random
from data.data_base import data


class User:
    def __init__(self, name,  password):
        self.__user_id = self._create_code()
        self.__name = name
        self.__password = password
        self.__courses = {}

    @property
    def user_id(self):
        return self.__user_id

    @property
    def password(self):
        return self.__password

    def _create_code(self):
        pass

    def mostrar_info(self):
        return f"ID de usuario: {self.__user_id} \n Cursos: {self.__courses}"

class Instructor(User):
    def __init__(self, name, password, students):
        super().__init__( name, password)
        self._students = students

    def create_course(self):
        name = input("Ingrese el nombre del curso: ")
        return f"El nombre del curso es {name}, el codigo es {"Poner id despues"}"

    def _create_code(self):
        final_code = ""
        while len(final_code) == 0:
            code = "IST"+"".join(str(random.randint(0, 9)) for _ in range(4))
            final_code = code
        return final_code


class Student(User):
    def __init__(self, name, password):
        super().__init__( name, password)
        self.__courses = {}

    def _create_code(self):
        final_code = ""
        while len(final_code) == 0:
            code = "STU"+"".join(str(random.randint(0, 9)) for _ in range(5))
            if code not in data.students:
                final_code = code
        return final_code
