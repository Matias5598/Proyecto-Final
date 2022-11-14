from .entities.Articulo import Articulo
from .entities.User import User
from datetime import datetime

class ModelArticulo:

    @classmethod
    def obtener_autor(self,db):
        cursor=db.connection.cursor()
        sql=f"SELECT * FROM usuario"
        cursor.execute(sql)
        autor=cursor.fetchall()
        return autor

    @classmethod
    def obtener_articulos(self,db):
        cursor=db.connection.cursor()
        sql="SELECT * from articulo"
        cursor.execute(sql)
        articulos=cursor.fetchall()

        return articulos
        

    @classmethod
    def publicar(self,db,articulo):
        cursor=db.connection.cursor()
        sql=f'INSERT INTO articulo VALUES ("","{articulo.titulo}","{articulo.contenido}",{articulo.autor},"{datetime.today().strftime("%Y-%m-%d")}","{datetime.today().strftime("%Y-%m-%d")}","{articulo.imagen}")'
        cursor.execute(sql)
        db.connection.commit()

    @classmethod
    def editar(self,db,articulo):
        cursor=db.connection.cursor()
        sql=f'UPDATE articulo SET titulo="{articulo.titulo}",contenido="{articulo.contenido}",updated="{datetime.today().strftime("%Y-%m-%d")}",imagen="{articulo.imagen}",destacado={articulo.destacado} WHERE idArticulo={articulo.idArticulo}'
        cursor.execute(sql)
        db.connection.commit()
    
    @classmethod
    def eliminar(self,db,id):
        try:
            cursor=db.connection.cursor()
            sql=f'DELETE FROM articulo WHERE idArticulo={id}'
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    ##Busca articulos de acuerdo a su id...
    def buscar_articulos(self,db,ids):
        for id in ids:
            cursor=db.connection.cursor()
            sql= f'SELECT * FROM articulo WHERE idArticulo = {id[0]}'
            cursor.execute(sql)
            articulos=cursor.fetchall()
        return articulos
    
    @classmethod
    def buscar_articulo(self,db,id):
        cursor=db.connection.cursor()
        sql= f'SELECT * FROM articulo WHERE idArticulo={id}'
        cursor.execute(sql)
        articulo=cursor.fetchone()
        return articulo
