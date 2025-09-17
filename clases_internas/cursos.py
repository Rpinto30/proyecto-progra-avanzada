# Clase cursos
import random
from data.data_base import data
from clases_internas.material import Homework

class Courses:
    def __init__(self, course_name, _id=''):
        if _id == '': self._course_id = self._create_code()
        else: self._course_id = _id
        self._course_name = course_name

    @property
    def course_id(self):
        return self._course_id

    @property
    def course_name(self):
        return self._course_name

    @property
    def teacher(self):
        return self.__teacher

    @property
    def student(self):
        return self._student


    def _create_code(self):
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

    def assign_homework(self, entry_tittle: str, entry_description: str, entry_points: str):
        homewor = Homework(entry_tittle, entry_description, self._course_id, entry_points)
        homeworkdict = {
            "tittle": entry_tittle,
            "description": entry_description,
            "points": entry_points,
            "course": self._course_id,
            "obtained_points" :0,
            "homework":''
        }
        data.courses[self._course_id]['material'][homewor.material_id] = homeworkdict
        data.save_data("courses")
        data.save_data("students")

        for student in data.courses[self._course_id]['students']:
            data.students[student]['material'][homewor.material_id] = homeworkdict
        data.save_data("students")

    def qualification(self, student_id, homework_id, points):
        if student_id in data.courses[self._course_id]['students']:
            data.students[student_id]['material'][homework_id]["obtained_points"] = int(points)
            data.save_data("students")


