# Clase cursos
import random
from data.data_base import data

class Courses:
    def __init__(self, course_name, teacher):
        self.__course_id = self.__create_code()
        self._course_name = course_name
        self.__teacher = teacher
        self.__student = {}
        self.__material = []

    @property
    def course_id(self):
        return self.__course_id

    @property
    def course_name(self):
        return self._course_name

    @property
    def teacher(self):
        return self.__teacher

    @property
    def student(self):
        return self.__student

    @property
    def material(self):
        return self.__material

    def __create_code(self):
        final_code = ""
        repeat_times = 0
        digits = 4
        while len(final_code) == 0:
            code = "SUB" + "".join(str(random.randint(0, 9)) for _ in range(digits))
            if code not in data.courses:
                final_code = code
            else:
                repeat_times += 1
                if repeat_times > 10 ** digits: digits += 1
        return final_code




