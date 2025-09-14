import random
from data.data_base import data
from .cursos import Courses #IMPORT RELATIVO (Por eso el __init en la carpeta, para especificar que esta carpeta es un paquete)
#https://realpython-com.translate.goog/absolute-vs-relative-python-imports/?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=tc

class User:
    def __init__(self, name,  password):
        self._user_id = self._create_code()
        self._name = name
        self._password = password
        self.__courses = {}

    @property
    def user_id(self):
        return self._user_id

    @property
    def password(self):
        return self._password

    def _create_code(self):
        pass

    def mostrar_info(self):
        return f"ID de usuario: {self._user_id} \n Cursos: {self.__courses}"

class Instructor(User):
    def __init__(self, name, password):
        super().__init__( name, password)
        self.__courses = {}
        self.create_instructor(name, password)

    def create_instructor(self, entry_name, entry_password):
        if entry_name.strip() == "" or entry_password.strip() == "":
            if entry_name.strip() == "" and entry_password.strip() == "":
                return -3
            elif entry_name.strip() == "":
                return -1
            elif entry_password.strip() == "":
                return -2
            else:
                return -4
        else:
            data.instructors[self.user_id] = {
                "name": self._name,
                "password": self._password
            }
            data.save_data("instructors")
            return 0

    def create_course(self, entry_name:str):
        if entry_name.strip() != "":
            course = Courses(entry_name, self)
            data.courses[course.course_id] = {
                "corse_name": course.course_name,
                "course_id": course.course_id,
                "teacher": data.instructors[self.user_id]
            }
            data.save_data("courses")


    def _create_code(self):
        final_code = ""
        repeat_times = 0
        digits = 4
        while len(final_code) == 0:
            code = "IST" + "".join(str(random.randint(0, 9)) for _ in range(digits))
            if code not in data.instructors:final_code = code
            else:
                repeat_times += 1
                if repeat_times > 10 ** digits: digits += 1
        return final_code


class Student(User):
    def __init__(self, name, password):
        super().__init__( name, password)
        self.__courses = {}
        self.create_student(name, password)

    def create_student(self, entry_name:str, entry_password:str):
        if entry_name.strip() == "" or entry_password.strip() == "":
            if entry_name.strip() == "" and entry_password.strip() == "":
                return -3
            elif entry_name.strip() == "":
                return -1
            elif entry_password.strip() == "":
                return -2
            else:
                return -4
        else:
            data.students[self.user_id] = {
                "name": self._name,
                "password": self._password
            }
            data.save_data("students")
            return 0

    def _create_code(self):
        final_code = ""
        repeat_times = 0
        digits = 4
        while len(final_code) == 0:
            code = "STU" + "".join(str(random.randint(0, 9)) for _ in range(digits))
            if code not in data.students:final_code = code
            else:
                repeat_times += 1
                if repeat_times > 10 **digits: digits+=1
        return final_code


tea1 = Instructor("Tilin ", "123")
#tea1.create_course("skibidi")
#student1 = Student("Rodrigo", "1234")
print([_ for _ in data.students])