from .entities.User import User
from werkzeug.security import generate_password_hash

class ModelUser():

    @classmethod
    def login(self,db,user):
        try:
            cursor=db.connection.cursor()
            sql= f'SELECT * FROM usuario WHERE email = "{user.email}"'
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                usuario = User(row[0],row[1],User.check_password(row[2],user.password),row[3],row[4])
                return usuario
            else:
                None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def register(self,db,user):
        try:
            cursor=db.connection.cursor()
            sql=f'INSERT INTO usuario VALUES ("","{user.nombre}","{user.email}","{generate_password_hash(user.password)}","{user.pais}")'
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def listar_usuarios(self,db):
        try:
            cursor=db.connection.cursor()
            sql=f'SELECT * FROM usuario'
            cursor.execute(sql)
            usuarios=cursor.fetchall()
            return usuarios
        
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def editar_usuario(self,db,user):
        try:
            cursor=db.connection.cursor()
            sql=f'UPDATE usuario SET nombre="{user.nombre}",email="{user.email}",pais="{user.pais}" WHERE idUsuario={user.idUsuario}'
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def eliminar_usuario(self,db,id):
        try:
            cursor=db.connection.cursor()
            sql=f'DELETE FROM usuario WHERE idUsuario={id}'
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def buscar_usuario(self,db,id):
        cursor=db.connection.cursor()
        sql= f'SELECT * FROM usuario WHERE idUsuario={id}'
        cursor.execute(sql)
        usuario=cursor.fetchone()
        return usuario