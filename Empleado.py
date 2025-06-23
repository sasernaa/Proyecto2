class Empleado:
    def __init__(self,cedula,nombre,apellido,telefono,email,servicio):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email
        self.servicio = servicio
        self.contador = 0

    def __str__(self):
        return self.cedula + " " + self.nombre + " " + self.apellido

    def get_cedula(self):
        return self.cedula
    
    def get_nombre(self):
        return self.nombre + " " + self.apellido
    
    def get_servicio(self):
        return self.servicio
    
    def set_servicio(self,nuevoServicio):
        self.servicio = nuevoServicio
    
    def aumentar_reserva(self):
        self.contador += 1
    
    def quitar_reserva(self):
        if(self.contador > 0):
            self.contador -= 1
    
    