class Reserva:
    def __init__(self,idReserva,idCliente,idespecialista,idservicio,fecha,hora):
        self.idReserva = idReserva
        self.idCliente = idCliente
        self.idespecialista = idespecialista
        self.idservicio = idservicio
        self.fecha = fecha
        self.hora = hora
    
    def imprimir(self):
        return [self.idReserva,self.idespecialista,self.idservicio,self.fecha,self.hora]

    def get_idReserva(self):
        return self.idReserva

    def get_idCliente(self):
        return self.idCliente

    def get_fecha(self):
        return self.fecha
    
    def get_hora(self):
        return self.hora
    
    def get_idespecialista(self):
        return self.idespecialista
    
    def get_idservicio(self):
        return self.idservicio
    
    