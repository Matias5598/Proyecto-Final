## <-- IMPORTACIONES -->
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL
from mis_funciones.validacion_registro import validacion_formulario_registro
from config import config

## Models...
from models.ModelUsuario import ModelUser
from models.ModelArticulo import ModelArticulo
from models.ModelCategorias import ModelCategoria

##Entities...
from models.entities.User import User
from models.entities.Articulo import Articulo
from models.entities.Categoria import Categoria

##app.secret_key='3075293597833f5a764239540298ceffc4e1d07cbce93a213d13527db8913c9a'
app= Flask(__name__)

## <-- CONEXION A BASE DE DATOS --> 
conexion=MySQL(app)

## <-- VISTAS -->

## VISTA DE PAGINA DE INICIO...
@app.route('/')
def index():
    try:
        articulos=ModelArticulo.obtener_articulos(conexion)
        autores=ModelArticulo.obtener_autor(conexion)
    except Exception as ex:
        return ex

    return render_template('index.html',articulos=articulos,autores=autores)

## VISTA DE CATEGORIAS...
@app.route('/categorias')
def categorias():
    try:
        csr=conexion.connection.cursor()
        sql='SELECT * FROM categoria'
        csr.execute(sql)
        categorias=csr.fetchall()
    except:
        return 'Error'

    return render_template('categorias.html',categorias=categorias)

## VISTA DE ALGUNA CATEGORIA EN PARTICULAR...

@app.route('/categorias/<int:id_categoria>')
def categoria(id_categoria):
    try:
        csr=conexion.connection.cursor()
        sql=f'SELECT nombre FROM categoria WHERE idCategoria = {id_categoria}'
        csr.execute(sql)
        categoria=csr.fetchone()
        idArticulos=ModelCategoria.BuscarArticulos(conexion,id_categoria)
        articulos=ModelArticulo.buscar_articulos(conexion,idArticulos)
        autores=ModelArticulo.obtener_autor(conexion)
    except:
        return 'No hay articulos en esta categoria.'

    return render_template('categoria_selected.html',articulos=articulos,categoria=categoria,autores=autores)

## VISTA DE LOGIN...
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        usuario=User(0,0,email,password,0)
        logged_user=ModelUser.login(conexion,usuario)

        if logged_user != None:
            if logged_user.password:
                return redirect(url_for('admin'))
            else:
                flash('Contraseña incorrecta. Reingrese.')
                return render_template('login.html')
                
        else:
            flash("El usuario no existe. Reintente.")
            return render_template('login.html')
    else:
        return render_template('login.html')

## VISTA DE REGISTRARSE...
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre=request.form['nombre']
        email=request.form['email']
        contraseña=request.form['password']
        re_contraseña=request.form['password2']
        pais=request.form['pais']
        usuario=User('',nombre,email,contraseña,pais)

        if validacion_formulario_registro(contraseña,re_contraseña):
            ModelUser.register(conexion,usuario)
            return redirect(url_for('login'))
        else:
            flash('Error al registrarse. Compruebe los datos ingresados.')
            return render_template('register.html')
    else:
        return render_template('register.html')

## VISTA DE CONTACTO...
@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

## VISTA DE ADMIN...
@app.route('/admin')
def admin():
    return render_template('admin_tablas.html')

## VISTA QUE LISTA LOS REGISTROS EN DETERMINADA TABLA PASADA POR LA URL...
@app.route('/admin/list/<variable>')
def listar(variable):
    if variable == 'users':
        usuarios=ModelUser.listar_usuarios(conexion)
        return render_template('admin_lista.html',registros=usuarios,variable=variable)
    elif variable == 'articles':
        articulos=ModelArticulo.obtener_articulos(conexion)
        return render_template('admin_lista.html',registros=articulos,variable=variable)
    elif variable == 'categories':
        categorias=ModelCategoria.listar_categorias(conexion)
        return render_template('admin_lista.html',registros=categorias,variable=variable)
    else:
        return 'La lista no existe.'

## VISTA  DE MODIFICACION DE REGISTROS...
@app.route('/admin/list/<lista>/modify/<int:id>',methods=['GET','POST'])
def modificar(lista,id):
    if lista == 'users':
        if request.method == 'POST':
            nombre=request.form['nombre']
            email=request.form['email']
            pais=request.form['pais']            
            usuario=User('',nombre,email,'',pais)
            ModelUser.editar_usuario(conexion,id,usuario)
            return redirect(url_for('admin'))

        else:
            registros=ModelUser.buscar_usuario(conexion,id)
            datos=[id,lista]
            campos=['','nombre','email','','pais']
            indices=[1,2,4]
            return render_template('admin_modify.html',campos=campos, datos=datos, indices=indices,registros=registros)
        
    elif lista == 'articles': 
        if request.method == 'POST':
            titulo=request.form['titulo']
            contenido=request.form['contenido']
            imagen=request.form['imagen']
            destacado=request.form['destacado']            
            articulo=Articulo(id,titulo,contenido,'','','',imagen,destacado)
            ModelArticulo.editar(conexion,articulo)
            flash('Articulo modificado correctamente.')
            return redirect(url_for('admin'))

        else:
            registros=ModelArticulo.buscar_articulo(conexion,id)
            datos=[id,lista]
            campos=['','titulo','contenido','','','','imagen','destacado']
            indices=[1,2,6,7]
            return render_template('admin_modify.html',campos=campos,registros=registros,indices=indices,datos=datos)

    elif lista == 'categories':
        if request.method == 'POST':
            nombre=request.form['nombre']            
            categoria=Categoria('',nombre)
            ModelCategoria.editar(conexion,categoria)
            return redirect(url_for('admin'))

        else:
            registros=ModelCategoria.buscar_categoria(conexion,id)
            datos=[id,lista]
            campos=['','nombre']
            indices=[1]
            return render_template('admin_modify.html',campos=campos, datos=datos, registros=registros,indices=indices)
    else:
        return 'Error. La tabla no existe.'

##VISTA AGREGAR NUEVOS REGISTROS...
@app.route('/admin/list/<lista>/add',methods=['GET','POST'])
def agregar(lista):
    if lista == 'users':
        if request.method == 'POST':
            nombre=request.form['nombre']
            email=request.form['email']
            pais=request.form['pais']
            contraseña=request.form['password']            
            usuario=User('',nombre,email,contraseña,pais)
            ModelUser.register(conexion,usuario)
            flash('Usuario creado correctamente.')
            return redirect(url_for('admin'))

        else:
            datos=lista
            campos=['','nombre','email','password','pais']
            indices=[1,2,3,4]
            return render_template('admin_add.html',campos=campos, datos=datos, indices=indices)
        
    elif lista == 'articles': 
        if request.method == 'POST':
            titulo=request.form['titulo']
            contenido=request.form['contenido']
            autor=request.form['autor']
            imagen=request.form['imagen']     
            destacado=request.form['destacado']       
            articulo=Articulo('',titulo,contenido,autor,'','',imagen,destacado)
            ModelArticulo.publicar(conexion,articulo)
            flash('Articulo agregado correctamente.')
            return redirect(url_for('admin'))

        else:
            datos=lista
            campos=['','titulo','contenido','autor','','','imagen','destacado']
            indices=[1,2,3,6,7]
            return render_template('admin_add.html',campos=campos,indices=indices,datos=datos)

    elif lista == 'categories':
        if request.method == 'POST':
            nombre=request.form['nombre']            
            categoria=Categoria('',nombre)
            ModelCategoria.agregar_categoria(conexion,categoria)
            flash('Categoria creada correctamente.')
            return redirect(url_for('admin'))

        else:
            datos=lista
            campos=['','nombre']
            indices=[1]
            return render_template('admin_add.html',campos=campos, datos=datos,indices=indices)
    else:
        return 'Error. La tabla no existe.'

##VISTA DE BORRAR REGISTRO...
@app.route('/admin/list/<lista>/delete/<int:id>',methods=['GET','POST'])
def borrar(lista,id):
    if lista == 'users':
        if request.method == 'POST':
            ModelUser.eliminar_usuario(conexion,id,)
            flash('Usuario borrado correctamente.')
            return redirect(url_for('admin'))
        else:
            registro=ModelUser.buscar_usuario(conexion,id)
            datos=[id,lista]
            campos=['id','nombre','email','','pais']
            indices=[0,1,2,4]
            return render_template('admin_delete.html',registro=registro,datos=datos,campos=campos,indices=indices)
        
    elif lista == 'articles': 
        if request.method == 'POST':
            ModelArticulo.eliminar(conexion,id)
            flash('Articulo borrado correctamente.')
            return redirect(url_for('admin'))
        else:
            registro=ModelArticulo.buscar_articulo(conexion,id)
            datos=[id,lista]
            campos=['id','titulo','contenido','autor','created','upadated','imagen']
            indices=[0,1,2,3,4,5,6]
            return render_template('admin_delete.html',registro=registro,datos=datos,campos=campos,indices=indices)
            

    elif lista == 'categories':
        if request.method == 'POST':
            ModelCategoria.editar(conexion,id)
            flash('Categoria borrada correctamente.')
            return redirect(url_for('admin'))

        else:
            registro=ModelCategoria.buscar_categoria(conexion,id)
            datos=[id,lista]
            campos=['id','nombre']
            indices=[0,1]
            return render_template('admin_delete.html',registro=registro,datos=datos,campos=campos,indices=indices)
    else:
        return 'Error. La tabla no existe.'

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()