class Servicio:
    def __init__(self,codigo,nombre,duracion,costo,listaEspecialistas):
        self.codigo = codigo
        self.nombre = nombre
        self.duracion = duracion
        self.costo = costo
        self.listaEspecialistas = listaEspecialistas

    def get_codigo(self):
        return self.codigo

    def get_nombre(self):
        return self.nombre
    
    def get_duracion(self):
        return self.duracion
    
    def get_costo(self):
        return self.costo
    
    def get_especialistas(self):
        return self.listaEspecialistas
    
    def add_especialista(self,empleado):
        if(empleado not in self.listaEspecialistas):
            self.listaEspecialistas.append(empleado)
    
    def remove_especialista(self,empleado):
        if(empleado in self.listaEspecialistas):
            self.listaEspecialistas.remove(empleado)
        