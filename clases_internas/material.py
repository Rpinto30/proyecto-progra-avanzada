import random
from data.data_base import data

class DidacticMaterial:
    def __init__(self, description,  course_id, _id = ""):
        self._description = description
        self._course_id = course_id
        if _id == '': self._material_id = self._create_code()
        else: self._material_id = _id

    @property
    def material_id(self):
        return self._material_id

    def _create_code(self)->str:
        pass


class Publish(DidacticMaterial):
    def __init__(self, tittle, description, course_id, _material_id = ""):
        super().__init__(description, course_id, _material_id)
        self._tittle = tittle

    def _create_code(self)->str:
        final_code = ""
        repeat_times = 0
        digits = 1
        while len(final_code) == 0:
            code = "PLH" + "".join(str(random.randint(0, 9)) for _ in range(digits))
            if code not in data.courses[self._course_id]['material']:
                final_code = code
            else:
                repeat_times += 1
                if repeat_times > 10 ** digits: digits += 1
        return final_code

class Homework(DidacticMaterial):
    def __init__(self, tittle, description, course_id, max_points, _material_id = ""):
        super().__init__(description, course_id, _material_id)
        self._max_points = max_points
        self._obteined_points = 0
        self._tittle = tittle


    def _create_code(self)->str:
        final_code = ""
        repeat_times = 0
        digits = 1
        while len(final_code) == 0:
            code = "HOM" + "".join(str(random.randint(0, 9)) for _ in range(digits))
            if code not in data.courses[self._course_id]['material']:
                final_code = code
            else:
                repeat_times += 1
                if repeat_times > 10 ** digits: digits += 1
        return final_code


class Exam(DidacticMaterial):
    def __init__(self, tittle, description, course_id, questions, correct_questions, _material_id = ""):
        super().__init__(description, course_id, _material_id)
        self._questions = questions
        self._questions = correct_questions
        self._obteined_points = 0
        self._tittle = tittle


    def _create_code(self)->str:
        final_code = ""
        repeat_times = 0
        digits = 1
        while len(final_code) == 0:
            code = "HOM" + "".join(str(random.randint(0, 9)) for _ in range(digits))
            if code not in data.courses[self._course_id]['material']:
                final_code = code
            else:
                repeat_times += 1
                if repeat_times > 10 ** digits: digits += 1
        return final_code
