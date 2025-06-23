class Cliente:
    def __init__(self,cedula,nombre,apellido,telefono,email):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email

    def __str__(self):
        return self.cedula + " " + self.nombre + " " + self.apellido
    
    def get_cedula(self):
        return self.cedula
    
    def get_nombre(self):
        return self.nombre