from Cliente import Cliente
from Empleado import Empleado
from Servicio import Servicio
from Reserva import Reserva
from tabulate import tabulate #Instalar tabulate (pip install tabulate)

class DAO():
    def __init__(self,clientes,servicios,empleados,reservas = []):
        self.clientes = clientes
        self.servicios = servicios
        self.empleados = empleados
        self.reservas = reservas

    def get_codigos(self,lista):
        temp = []
        for i in lista:
            temp.append(i.get_cedula())
        return temp

    def verificar_Empleado_sin_Reservas(self,xcedula):
        test = True
        for r in self.reservas:
            if(r.get_idespecialista() == xcedula):
                test = False
        return test
    
    def crear_Empleado(self):
        print("Bienvenido a la seccion crear empleado, por favor digite:")
        xcedula = input("Cedula: ")
        xnombre = input("Primer nombre: ")
        xapellido = input("Apellido: ")
        xtelefono = input("Numero telefónico: ")
        xemail = input("Email: ")
        xservicio = input("Servicio: ")
        test = True
        idsServicios = []
        for s in self.servicios:
            idsServicios.append(s.get_codigo())
        for e in self.empleados:
            if(e.get_cedula() == xcedula or xservicio not in idsServicios):
                test = False
        if(test):
            empleado = Empleado(xcedula,xnombre,xapellido,xtelefono,xemail,xservicio)
            self.empleados.append(empleado)        
            print("Operacion exitosa :)\n")
        else:
            print("Error: Duplicidad en id de empleado/No existe codigo de servicio")

    def borrar_Empleado(self):
        print("Bienvenido a la seccion borrar empleado, por favor digite:")
        xcedula = input("Cedula del empleado: ")
        test = False
        for e in self.empleados:
            if(e.get_cedula() == xcedula):
                test = True
                break
        if(test):
            if(self.verificar_Empleado_sin_Reservas(xcedula)):
                self.empleados.remove(e)
                print("Operacion exitosa :)")
            else:
                print(f"No se puede borrar al empleado de cedula: {xcedula}\nYa tiene una reserva asignada :(")
        else:
            print(f"No existe un empleado con cedula: {xcedula}")
    
    def validar_idReserva(self,idReserva):
        test = True
        listaidReservas = []
        for r in self.reservas:
            listaidReservas.append(r.get_idReserva())
        if(idReserva in listaidReservas):
            test = False
        return test

    def validar_disponibilidad_Reserva(self,idEspecialista,idServicio,fecha,hora):
        test = True
        temp = 0
        for e in self.empleados:
            if(e.get_cedula() == idEspecialista):
                temp = e
        if(idServicio in temp.get_servicio()):
            for r in self.reservas:
                if(r.get_fecha() == fecha and r.get_hora() == hora and r.get_idespecialista() == idEspecialista and r.get_idservicio() == idServicio):
                    test = False
                    print(f"El especialista: {temp.get_nombre()} ya tiene una cita para\nFecha: {fecha} y hora: {hora}")
                    break
        else:
            test = False
            print(f"El especialista: {temp.get_nombre()} no provee el servicio de codigo: {idServicio} :(")
        return test

    def validar_agenda_Cliente(self,idCliente,fecha,hora):
        test = True
        for r in self.reservas:
            if(r.get_idCliente() == idCliente and r.get_fecha() == fecha and r.get_hora() == hora):
                    test = False
        return test

    def validar_agenda_Empleado(self,idEspecialista,fecha,hora):
        test = True
        for r in self.reservas:
            if(r.get_idespecialista() == idEspecialista and r.get_fecha() == fecha and r.get_hora() == hora):
                test = False
        return test
    
    def crear_Reserva(self,xcedula):
        print("Modulo Cliente/Agendar_cita Digite:")
        xidReserva = input("Añada un id para la reserva: ")
        test = self.validar_idReserva(xidReserva)
        if(not test):
            print("Este id de la reserva ya existe")
        else:
            xidespecialista = input("Cedula del especialista: ")
            if(xidespecialista in self.get_codigos(self.empleados) and test):
                xidservicio = input("Codigo del servicio: ")
                xfecha = input("Fecha(DD/MM/YYYY): ")
                xhora = input("Hora(8-18): ")
                if(self.validar_agenda_Empleado(xidespecialista,xfecha,xhora)):
                    if(self.validar_agenda_Cliente(xcedula,xfecha,xhora)):
                        if(self.validar_disponibilidad_Reserva(xidespecialista,xidservicio,xfecha,xhora)):
                            reserva = Reserva(xidReserva,xcedula,xidespecialista,xidservicio,xfecha,xhora)
                            self.reservas.append(reserva)
                            print("Operacion exitosa :)\n",f"Recuerde su cita para: {xfecha} a las {xhora}")
                            print(len(self.reservas))
                    else:
                        print(f"Ya tienes un cita agendada para la fecha: {xfecha} y la hora: {xhora}")        
                else:
                    print(f"El especialista con id: {xidespecialista} ya esta ocupado para\nFecha: {xfecha} y hora: {xhora}")
            else:
                print(f"No existe un especialista de id: {xidespecialista} :(")

    def consultar_Reservas(self,xcedula):
        listaReservas = []
        for r in self.reservas:
            if(r.get_idCliente() == xcedula):
                listaReservas.append(r)
        return listaReservas

    def cancelar_Reserva(self,xcedula,xidReserva):
        listaRservas = self.consultar_Reservas(xcedula)
        temp = 0
        for r in listaRservas:
            if(r.get_idReserva() == xidReserva):
                temp = r
                break
        else:
            print(f"No se encontro reserva con codigo {xidReserva} :(")
        if(temp != 0):    
            self.reservas.remove(temp)
            print(f"Se ha borrado la reserva con id: {xidReserva}")

    def acceder_cliente(self):
        xcedula = input("Digite su cedula--> ")
        test = True
        temp = 0
        for c in self.clientes:
            if(c.get_cedula() == xcedula):
                temp = c
                break
        else:
            print("No se ha encontrado su cedula en la base de datos :(")
            test = False
        if(test):
            while(True):
                print(f"Hola! {temp.get_nombre()} Presione:\n1: Agendar cita\n2: Cancelar cita\n3: Consultar citas\n4: Salir")
                tramiteCliente = input("--> ")
                if(tramiteCliente == "1"):
                    self.crear_Reserva(temp.get_cedula())
                elif(tramiteCliente == "2"):
                    idReserva = input("Ingrese el id de la reserva--> ")
                    self.cancelar_Reserva(xcedula,idReserva)
                elif(tramiteCliente == "3"):
                    temp1 = []
                    for r in self.consultar_Reservas(xcedula):
                        temp1.append(r.imprimir())
                    print(f"Cita: {xcedula}\n")
                    print(tabulate(temp1,headers=["Id Reserva","Id Especialista","Id Servicio","Fecha","Hora"]))   
                elif(tramiteCliente == "4"):
                    break
                else:
                    print("Opcion incorrecta :(")

    def crear_cliente(self):
        print("Bienvenido a crear una cuenta, por favor: ")
        test = True
        xcedula = input("Ingrese su cedula: ")
        for c in self.empleados:
            if(c.get_cedula() == xcedula):
                test = False
        if(test):
            xnombre = input("Ingrese su primer nombre: ")
            xapellido = input("Ingrese su apellido: ")
            xtelefono = input("Ingrese su número telefónico: ")
            xemail = input("Ingrese su email: ")
            cliente = Cliente(cedula=xcedula,nombre=xnombre,apellido=xapellido,telefono=xtelefono,email=xemail)
            self.clientes.append(cliente)
            print("Operacion exitosa :)")
            for c in self.clientes:
                print(c)
        else:
            print("Este usuario ya existe :(")

    def crear_servicio(self):
        print("Modulo crear servicio, por favor digite:")
        xcodigo = input("Codigo: ")
        test = True
        for s in self.servicios:
            if(s.get_codigo() == xcodigo):
                test = False
        if(test):
            xnombre = input("Nombre: ")
            xduracion = 60
            xcosto = int(input("Costo: "))
            xlistaEspecialistas = list(input("Cedulas de especialistas: ").split(","))
            test2 = True
            for i in xlistaEspecialistas:
                if(i not in self.get_codigos(self.empleados)):
                    test2 = False
            if(test2):
                servicio = Servicio(xcodigo,xnombre,xduracion,xcosto,xlistaEspecialistas)
                self.servicios.append(servicio)        
                print("Operacion exitosa :)")
            else:
                print("Verifique la cedula de los especialistas que ingreso")
        else:
            print("Este servicio ya existe :(")
    
    def verificar_Servicio_sin_Reservas(self,codigo):
        test = True
        for r in self.reservas:
            if(r.get_idservicio() == codigo):
                test = False
        return test

    def borrar_servicio(self,codigo):
        temp = 0
        for s in self.servicios:
            if(codigo == s.get_codigo()):
                temp = s
                break
        if(temp != 0):
            if(self.verificar_Servicio_sin_Reservas(codigo)):
                self.servicios.remove(temp)
                print(f"Se ha eliminado el servicio de codigo: {codigo} exitosamente :)")
            else:
                print(f"El servicio de codigo: {codigo} tiene una reserva pendiente :(")
        else:
            print(f"No se ha encontrado un servicio con codigo: {codigo} :(")
        

    def run(self):
        salir = True
        while(salir):
            print("Bienvenido al spa \"Dolorcito Quito\"")
            tramite = input("Ingrese:\n1: Ingresar como cliente\n2: Ingresar como admin\n3: Salir\n--> ")
            if(tramite == "1"):
                print("Presione:\n1: Acceder a su cuenta\n2: Crear una cuenta")
                tramiteCliente = input("--> ")
                if(tramiteCliente == "1"):
                    self.acceder_cliente()
                elif(tramiteCliente == "2"):
                    self.crear_cliente()
            
            elif(tramite == "2"):
                while(True):
                    print("Modulo de Administracion\n1: Modulo empleados\n2: Modulo servicios\n3: Salir")
                    tramiteAdmin = input("-->")
                    if(tramiteAdmin == "1"):
                        while(True):
                            print("Modulo Administracion/Empleados\nPresione:\n1: Agregar un nuevo empleado\n2: Eliminar un empleado\n3: Salir")
                            tramiteAdminEmpleado = input("-->")
                            if(tramiteAdminEmpleado == "1"):
                                self.crear_Empleado()
                            elif(tramiteAdminEmpleado == "2"):
                                self.borrar_Empleado()
                            elif(tramiteAdminEmpleado == "3"):
                                break
                            else:
                                print("Opcion incorrecta")
                    elif(tramiteAdmin == "2"):
                        while(True):
                            print("Modulo de Administacion/Servicios\nPresione:\n1: Ingresar un servicio\n2: Borrar un servicio\n3: salir")
                            tramiteAdminServicios = input("-->")
                            if(tramiteAdminServicios == "1"):
                                self.crear_servicio()
                            elif(tramiteAdminServicios == "2"):
                                codigo = input("Ingrese el codigo del servicio--> ")
                                self.borrar_servicio(codigo)
                            elif(tramiteAdminServicios == "3"):
                                break
                            else:
                                print("Opcion incorrecta")
                    elif(tramiteAdmin == "3"):
                        break
                    else:
                        print("Opcion incorrecta")
                    
            elif(tramite == "3"):
                print("Vuelva pronto! :)")
                break

            else:
                print("Opcion incorrecta :(")