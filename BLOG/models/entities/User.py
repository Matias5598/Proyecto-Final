from werkzeug.security import check_password_hash

class User():

    def __init__(self, id, nombre, email, password, pais) -> None:
        self.id=id
        self.nombre=nombre
        self.email=email
        self.password=password
        self.pais=pais

    @classmethod
    def check_password(self,hashed_password,password):
        check_password_hash(hashed_password,password)