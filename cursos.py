# Clase cursos
import random
from usuarios import Teacher, Student

class Courses:
    def __init__(self, course_name, teacher):
        self.__course_id = self.__create_code({})
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

    def __create_code(self, courses):
        final_code = ""
        while len(final_code) == 0:
            code = "SUB"+"".join(str(random.randint(0, 9)) for _ in range(4))
            final_code = code
        return final_code



stu = Student("Est123","Rodrigo", "234", "Hola@gmail.com")
stu2 = Student("Est345", "Are", "123", "roro")
stu3 = Student("Est444","Masha", "555", "Tortilla")
tea = Teacher("Cat122", "Cabra", "223", "Docente", {})
tea2 = Teacher("Cat123","Tello",  "67", "Inges", {})
tea3 = Teacher("Cat124","cocacola", "1111", "pepe", {})
cour = Courses( "tonchan", tea)
cour2 = Courses("Lenguaje",tea2 )
cour3 = Courses("Magis", tea3)
curs = {cour.course_id: cour, cour2.course_id: cour2, cour3.course_id: cour3 }
print(curs[cour.course_id].teacher)


