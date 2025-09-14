
class User:
    def __init__(self, user_id, name,  password, mail):
        self.__user_id = user_id
        self.__name = name
        self.__password = password
        self._mail = mail
        self.__mail = mail
        self.__courses = {}

    @property
    def user_id(self):
        return self.__user_id

    @property
    def password(self):
        return self.__password

    @property
    def correo(self):
        return self._mail

    @property
    def cursos(self):
        return self.__mail

    def mostrar_info(self):
        return f"ID de usuario: {self.__user_id} \n Correo: {self._mail} \n Cursos: {self.__courses}"

class Teacher(User):
    def __init__(self, user_id, name, password, mail, students):
        super().__init__(user_id, name, password, mail)
        self._students = students

    def create_course(self):
        name = input("Ingrese el nombre del curso: ")
        return f"El nombre del curso es {name}, el codigo es {"Poner id despues"}"



class Student(User):
    def __init__(self, user_id, name, password, mail):
        super().__init__(user_id, name, password, mail)


