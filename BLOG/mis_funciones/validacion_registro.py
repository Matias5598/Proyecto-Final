
def validacion_formulario_registro(password1,password2):
    contraseña=password1
    re_contraseña=password2

    if len(password1) >= 8:
        if contraseña == re_contraseña:
            return True
        else:
            return False
    else:
        return False

    