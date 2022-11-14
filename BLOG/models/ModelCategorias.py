class ModelCategoria:

    @classmethod
    def BuscarArticulos(self,db,categoria):
        try:
            csr=db.connection.cursor()
            sql=f'SELECT idArticulo FROM tiene WHERE idCategoria = {categoria}'
            csr.execute(sql)
            articulos=csr.fetchall()
            if articulos!=None:
                return articulos
            else:
                return None

        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def listar_categorias(self,db):
        cursor=db.connection.cursor()
        sql=f'SELECT * FROM categoria'
        cursor.execute(sql)
        usuarios=cursor.fetchall()
        return usuarios

    @classmethod
    def editar(self,db,categoria):
        cursor=db.connection.cursor()
        sql=f'UPDATE categoria SET nombre={categoria.nombre}'
        cursor.execute(sql)
        db.connection.commit()

    @classmethod
    def eliminar(self):
        pass

    @classmethod
    def buscar_categoria(self,db,id):
        cursor=db.connection.cursor()
        sql= f'SELECT * FROM categoria WHERE idCategoria={id}'
        cursor.execute(sql)
        categoria=cursor.fetchone()
        return categoria

    @classmethod
    def agregar_categoria(self,db,categoria):
        cursor=db.connection.cursor()
        sql=f'INSERT INTO categoria VALUES ("","{categoria.nombre}")'
        cursor.execute(sql)
        db.connection.commit()