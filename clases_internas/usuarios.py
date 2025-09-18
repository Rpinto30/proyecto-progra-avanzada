import random
from data.data_base import data
from clases_internas.cursos import Courses
class User:
    def __init__(self, name,  password, id_=''):
        if id_ == '': self._user_id = self._create_code()
        else: self._user_id = id_
        self._name = name
        self._password = password
        self.__courses = {}

    @property
    def user_id(self):
        return self._user_id

    @property
    def password(self):
        return self._password

    @property
    def name(self): return self._name

    def _create_code(self):
        pass

    def mostrar_info(self):
        return f"ID de usuario: {self._user_id} \n Cursos: {self.__courses}"

class Instructor(User):
    def __init__(self, name, password, user_id=''):
        super().__init__(name, password, user_id)
        self.__courses = {}

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
                "password": self._password,
                "courses": []
            }
            data.save_data("instructors")
            return 0

    def create_course(self, entry_name:str):
        if entry_name.strip() != "":
            course = Courses(entry_name)
            coursedict = {
                "course_name": course.course_name,
                "teacher": self.user_id,
                "students": [],
                "material": {}
            }
            data.courses[course.course_id] = coursedict
            data.instructors[self.user_id]['courses'].append(course.course_id)
            data.save_data("instructors")
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
    def __init__(self, name, password,user_id=''):
        super().__init__( name, password, user_id)
        self.__courses = {}

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
            data.students[self._user_id] = {
                "name": self._name,
                "password": self._password,
                "material": {},
                "courses": []
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

    def course_register(self, course_id):
        if self.user_id not in data.courses[course_id]['students']:
            data.courses[course_id]['students'].append(self.user_id)
            data.students[self.user_id]['courses'].append(course_id)
            data.save_data("courses")
            data.save_data("students")
            for id_, values in data.courses[course_id]['material'].items():
                print(values)
                if id_ not in data.students[self.user_id]['material']:
                    homeworkdict = {
                        "tittle": values['tittle'],
                        "description": values['description'],
                        "points": values['points'],
                        "course": course_id,
                        "obtained_points": 0,
                        "homework": ''
                    }
                    data.students[self.user_id]['material'][id_] = homeworkdict
                    data.save_data("students")


    def send_homework(self, id_homework, entry_homework):
        data.students[self.user_id]['material'][id_homework]['homework'] = entry_homework
        data.save_data('students')

#tea1 = Instructor("Pepe", "123")
#tea1.create_instructor("Pepe", "123")
#tea1.create_course("CursoPrueba")


#student1 = Student("Rodrigo", "123")
#student1.create_student("Rodrigo", "123")
#student1.course_register("SUB7142")


#course1 = Courses("CursoPrueba", "IST3732", ["STU1198"], "", "SUB7142")
#course1.assign_homework("Tarea1", "Tarea casa", "20")
#course1.qualification("STU1198", "HOM8", "4")